#!/usr/bin/env python
import time
#from RabbitConnections import Rabbit_connection
# import win32com.client
import json
from ScrappingConsumer.Queues.ScraperQueue.ScriptExecutor import  ScriptsExecution
import threading
# from Queues import *
import datetime
import time
from eCubeLog import logger
from pdb import set_trace as st

class CrawlerConsumer():
    # print ("calling first consumer")
    def callback(self,ch, method, properties, body):
        #print(type(body))
        print("Receiving Messages -- %r" % body)
        print("Consumer running Time", datetime.datetime.now())

        try:
            data = body.decode('utf-8')
            consume_data = data.replace("'", "\"")
            consume_data = json.loads(consume_data)  # convert string to python dict

        except Exception as e:
            data = body.decode('utf-8')
            consume_data = eval(data)


            # print('Error while converting into JSON')
            # logger.error("Consumer Input Json not properly Serialize"+ str(e))
        #st()
        scexec = ScriptsExecution(consume_data)
        data=scexec.run()


        # try:
        #     scexec = ScriptsExecution(consume_data)
        #     data=scexec.run()
        #     print("Received as a response",data)
        # except Exception as e:
        #     print('Error Occur Check logs',str(e))
        #     logger.error('Error at ConsumerRequestDataScraper:' +str(e))
        #     data = None
        # if data:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug('Crawling done')

    # channel = Rabbit_connection.CrawlerQueueConnection("")   # calling Category Queue Connection class
    # channel.basic_qos(prefetch_count=1)
    # channel.basic_consume(callback,
    #                   queue='Crawler')
    # channel.start_consuming()

'''
logger.debug('Consumer Ready to start')
t1 = threading.Thread(target=CrawlerConsumer,args=[])
t1.start()
print("Consumer running Time",datetime.datetime.now())
time.sleep(0.1)
'''
