#!/usr/bin/env python
import time
from RabbitConnections import Rabbit_connection
# import win32com.client
import json
from ScriptProductExecution import  ScriptsExecution
import threading
import ast
import requests
import pymongo
from pymongo import MongoClient
import datetime
import time
from eCubeLog import logger

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


class ParserConsumer():
    # print ("calling first consumer")

    def callback(ch, method, properties, body):

        print("parser Consumer Message time", datetime.datetime.now())
        logger.debug('Consumer Ready to start')

        print("Recieving Messages --",body)
        data = body.decode('utf-8')

        # consume_data = data.replace("'", "\"")
        # consume_data = json.loads(consume_data)  # convert string to python dict

        consume_data = ast.literal_eval(data)

        subRequestId = consume_data['subRequestId']
        client = MongoClient('localhost', 27017)
        #client = MongoClient('192.168.7.134', 27017)
        db = client.HTMLDumps
        consume_data = db.HTMLRepository.find_one({'subRequestId': subRequestId})


        if consume_data['IsCategory'] == "Yes":

            json_data = json.dumps(consume_data)
            try:
                result = requests.post('http://192.168.8.7/site3/api/v1/SaveResponseData', json=consume_data)
                #result = requests.post('http://192.168.7.128/site3/api/v1/SaveResponseData', json=consume_data)
            except Exception as e:
                pass
            print(result)
            if result:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
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
                print("PNFDATA",PNFData)

                ch.basic_ack(delivery_tag=method.delivery_tag)

                DataInsert = db.PNFData.insert(PNFData)

            elif data == "Access Denied":

                AccessDenied = DATA_MAKER(consume_data)
                print("Access Denied",AccessDenied)

                DataInsert = db.PNFData.insert(AccessDenied)

                ch.basic_ack(delivery_tag=method.delivery_tag)


            else:

                ch.basic_ack(delivery_tag=method.delivery_tag)


    

    '''
    Below Code commented and added in startParserConsumerServices.py file 
    '''


    print("Connected")
    channel = Rabbit_connection.ParserQueueConnection("")   # calling Category Queue Connection class
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                      queue='Parser')
    channel.start_consuming()





logger.debug('Consumer Ready to start')

t1 = threading.Thread(target=ParserConsumer,args=[])
t1.start()
time.sleep(0.08)


