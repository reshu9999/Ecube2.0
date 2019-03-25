import pika
import json
import requests

from queues.executor import ScriptHandler
from queues.connections import MySQLConnection, MongoConnection
from queues.core import QueueLogger as QL
from queues.core import Callback


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


class DynamicConsumer(object):

    @classmethod
    def ParserDynamicRabbitConnection(cls):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        return channel

    @classmethod
    def ParserDynamicDBConnection(cls):
        '''
        DB Connection here
        :return:
        '''
        QL.debug_log('Dynamic Parsing Consumer --- Group Master Called')
        Groupdb = MySQLConnection()._db
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
        print("Receiving Messages --")

        data = body.decode('utf-8')
        # consume_data = data.replace("'", "\"").replace('\\\\', '\\')
        consume_data = json.loads(data)  # convert string to python dict

        # consume_data = ast.literal_eval(data)
        #subRequestId = consume_data['subRequestId']

        # from pdb import set_trace as st; st()
        # consume_data = ast.literal_eval(data)[0]

        subRequestId = consume_data['subRequestId']

        # mongoDBCur = CommonConnection.MongoConnection()

        # from pdb import set_trace as st; st()

        if "hotel" in consume_data.keys():
            scriptParse = ScriptHandler(consume_data)
            parsed_data = scriptParse.execute_parse()
            # MongoConnection().save_successful_parse(parsed_data)
            sub_request_completed = MongoConnection().save_partial_parse(parsed_data, 'to_be_parsed')
            if sub_request_completed:
                print('aetos done')

                request_id = consume_data['requestId']
                sub_req_id = consume_data['subRequestId']
                mysql_conn = MySQLConnection()._db
                print('args for update request run detail "%s"' % (",".join(['lasun', str(request_id), str(sub_req_id), '69'])))
                cur = mysql_conn.cursor()
                cur.execute('call sp_UpdateRequestRunDetail("lasun", %s, %s, "69")' % (request_id, sub_req_id))
                mysql_conn.commit()
                cur.close()
                mysql_conn.close()
            ch.basic_ack(delivery_tag=method.delivery_tag)

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

    @classmethod
    def DynamicParserMain(cls):
        grouplistDict = cls.ParserDynamicDBConnection()
        print("grouplistDict")
        print(grouplistDict)
        channel = cls.ParserDynamicRabbitConnection()

        for key, value in grouplistDict.items():

            for _ in range(int(value)):
                #channel.basic_consume(ParserDynamicConsumer.callback, queue="Parser" + str(key), consumer_tag=None)
                channel.basic_consume(cls.callback, queue="Parser", consumer_tag=None)

        channel.start_consuming()


class ReparseConsumer(object):
    @staticmethod
    def callback(ch, method, properties, body):
        Callback(ch, method, properties, body).consume()

    def RabbitConnection(self):

        print('Dynamic Scrapping Consumer --- rabbitMQ Connection called')

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat_interval=0))
        # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        return channel

    def Main(self):
        print("Dynamic Scrapping Producer --- Main function  Called")

        channel = self.RabbitConnection()

        try:
            channel.basic_consume(ReparseConsumer.callback, queue='Reparse', consumer_tag=None)
        except pika.exceptions.ChannelClosed:
            print('Closed or no Queue ' + 'Reparse')
            channel = self.RabbitConnection()

        channel.start_consuming()
