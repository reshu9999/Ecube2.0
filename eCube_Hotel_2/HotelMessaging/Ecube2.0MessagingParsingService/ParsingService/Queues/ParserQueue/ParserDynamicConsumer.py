import pika
import datetime
import  time
from pymongo import  MongoClient
import pymysql
import threading
from eCubeLog import logger
import  CommonConnection
from ScriptProductExecution import  ScriptsExecution
import ast
import json
import requests
from executor import ScriptHandler
from pdb import set_trace as st

DATA_MAKER = lambda x: {
    "domainName": x['domainName'],
    "sourceUrl": x['sourceUrl'],
    "proxyUsername": x['proxyUsername'],
    "startDT": "2018-03-13 21:52:20",
    "pythonScriptName": x['pythonScriptName'],
    "IsCategory": x['IsCategory'],
    "endDT": x['endDT'],
    "requestId": x['requestId'],
    "proxyCountry": x['proxyCountry'],
    "ParserScript": x['ParserScript'],
    "subRequestId": x['subRequestId'],
    "ProxyInformation": x['ProxyInformation'],
    "Proxy Attempts": '',
    "totalResponse": x['totalResponse'],
    "status": x['status'],
    "Error": x['Error'],
    "TimeStamp": x['TimeStamp'],
    "response": x['response'],
    "RequestRunId": x['RequestRunId'],
    "proxyAddress": x['proxyAddress'],
    "proxyPort": x['proxyPort'],
    "Proxies Used": '',
    "PNFStatus": "PNF"
}


class ParserDynamicConsumer():

    def __init__(self):
        self.QueueCount = ""

    # def ParserDynamicQueueCount(self):
    #     args = {}
    #     args['x-max-length'] = 100000000
    #     self.QueueCount = self.channel.queue_declare(queue='RS', durable=True,
    #                                                    arguments=args).method.message_count
    #
    #     return  self.QueueCount


    def ParserDynamicRabbitConnection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        return channel


    def ParserDynamicDBConnection(self):
        '''
        DB Connection here
        :return:
        '''
        logger.debug('Dynamic Parsing Consumer --- Group Master Called')
        Groupdb = CommonConnection.MySQLConnection()
        group = Groupdb.cursor()
        group.execute("select * from tbl_Bli_GroupMaster")
        grouplist = []
        for row in group.fetchall():
            GroupRowList = (row[1], row[2] or 0)
            grouplist.append(GroupRowList)

        grouplist_dict = dict(grouplist)

        group.close()
        Groupdb.close()
        return grouplist_dict


    def callback(ch, method, properties, body):

        '''
        :param ch:   connection channel
        :param method:  method name
        :param properties: priority Properties
        :param body:  message
        :return:
        '''

        # print("Messaging recived from QUEUE")
        print("Recieving Messages --", body)
        data = body.decode('utf-8')
        # consume_data = data.replace("'", "\"")
        # consume_data = json.loads(consume_data)  # convert string to python dict

        #consume_data = ast.literal_eval(data)
        #subRequestId = consume_data['subRequestId']
        consume_data = ast.literal_eval(data)[0]
        subRequestId = consume_data['meta']['subRequestId']

        mongoDBCur = CommonConnection.MongoConnection()

        #if "Hotel" in consume_data['Businesstype']:
        if "hotelName" in consume_data.keys():
            print("Integrate Hotel Script ------------")
            #scriptParse = ScriptHandler('', **consume_data)
            #data=scriptParse.execute_parse()
            data={'hotelname':'Taj', 'hoteladdress':'Mumbai Marine Drive' ,
                'city':'Mumbai', 'checkindate': '01-01-2018', 'checkoutdate': '10-01-2018', 
                'PostCode':'4210001','Adult': 2, 'roomtypes' : [{'RoomType':'delux','Rate':'1000'}, 
                    {'RoomType':'Single','Rate':'2000'}, {'RoomType':'Double','Rate':'500'}] }

            data=json.dumps(data)
            result = requests.post('http://localhost:5000/api/v1/service/SaveResponseHotelData',data=data)

            #ch.basic_ack(delivery_tag=method.delivery_tag)


        else:

            consume_data = mongoDBCur.HTMLRepository.find_one({'subRequestId': subRequestId})

            if consume_data['IsCategory'] == "Yes":

                json_data = json.dumps(consume_data)
                try:
                    result = requests.post('http://192.168.8.7/site3/api/v1/SaveResponseData', json=consume_data)
                    # result = requests.post('http://192.168.7.128/site3/api/v1/SaveResponseData', json=consume_data)
                except Exception as e:
                    pass
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print("save Response Called for data",consume_data )
                data = ScriptsExecution.ConsumerRequestData('', **consume_data)

                '''
                try:
                    data = ScriptsExecution.ConsumerRequestData('',**consume_data)
                    print(data)
                except Exception as e:
                    # logger.error('Script Executer Return Error',str(e))
                    print("Script Executer error",e)
                    data  = None
                      data = "Error"
                '''

                if data == "PNF":
                    PNFData = DATA_MAKER(consume_data)
                    print("PNFDATA", PNFData)

                    ch.basic_ack(delivery_tag=method.delivery_tag)

                    DataInsert = mongoDBCur.PNFData.insert(PNFData)

                elif data == "Access Denied":
                    AccessDenied = DATA_MAKER(consume_data)
                    print("Access Denied", AccessDenied)
                    DataInsert = mongoDBCur.PNFData.insert(AccessDenied)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    ch.basic_ack(delivery_tag=method.delivery_tag)


    def DynamicParserMain(self):
        grouplistDict = ParserDynamicConsumer.ParserDynamicDBConnection("")
        channel = ParserDynamicConsumer.ParserDynamicRabbitConnection("")

        for key,value in grouplistDict.items():

            for _ in range(int(value)):
                #channel.basic_consume(ParserDynamicConsumer.callback, queue="Parser" + str(key), consumer_tag=None)
                channel.basic_consume(ParserDynamicConsumer.callback, queue="Parser", consumer_tag=None)

        channel.start_consuming()


# logger.debug('Consumer Ready to start')
obj = ParserDynamicConsumer()
t1 = threading.Thread(target=obj.DynamicParserMain, args=())
t1.start()
print("Dynamic parser Consumer running Time", datetime.datetime.now())
time.sleep(0.1)

