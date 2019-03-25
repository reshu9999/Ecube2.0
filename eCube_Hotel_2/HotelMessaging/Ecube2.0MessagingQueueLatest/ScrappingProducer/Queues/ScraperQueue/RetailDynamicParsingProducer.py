import pika
import time
import threading
import pymysql
from threading import active_count
from eCubeLog import logger
from pymongo import  MongoClient
import datetime
import CommonConnection
class ParserDynamicProducer(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        args = {}

        args["x-max-length"] = 10000000
        args['x-max-priority'] = 9

        self.mongodb = CommonConnection.MongoConnection()
        self.db = CommonConnection.MySQLConnection()
        self.RabbitCon = CommonConnection.RabbitMQConnection()
        self.IPAddr = CommonConnection.ServivesIP()

        logger.debug("Dynamic Queue Connection established")



    def DatabaseQueryCall(self):

        logger.debug("Dynamic Parser Producer ---  Database Called")
        '''
        Query Logic task
        :return:
        '''
        print("Parser Database Called ")


        last_updated_date = self.mongodb.ParserQueueUpdate.find_one({'_id': 1})
        Last_Parser_update_date = last_updated_date['QueueUpdateDateTime']
        #records = db.HTMLRepository.find({'$and': [{'TimeStamp': {'$gte': Last_Parser_update_date}}]})

        records = self.mongodb.HTMLRepository.find({'parsingStatus': 1})
        print(records)

        if not records:

            SYSdate = datetime.datetime.now()
            self.mongodb.ParserQueueUpdate.update(
                {
                    'PARSER': '1'
                },
                {
                    "$set": {'QueueUpdateDateTime': datetime.datetime.strftime(SYSdate, '%Y-%m-%d %H:%M:%S')}
                })

        return records


    def run(self):


        SUBREQUESTID = []

        logger.debug("Dynamic Parser Producer ---  Main Function alled")

        records = ParserDynamicProducer.DatabaseQueryCall(self)

        for msg in records:


            if msg:
                        self.channel.basic_publish(exchange='', routing_key= "Parser"+str(msg['groupName']),
                                                           body=str(msg))
                        print("Queue Sending Messages", msg)

            SUBREQUESTID.append(msg['subRequestId'])

        self.connection.close()

        ParserDynamicProducer.UpdateSUBRequest(self,SUBREQUESTID)

        logger.debug("Dynamic Queue Connection closed successfully")


    def UpdateSUBRequest(self,SUBREQUESTID):


        for row in SUBREQUESTID:

            self.mongodb.HTMLRepository.update(
                {
                    'subRequestId': row
                },
                {
                    "$set": {'parsingStatus': 0 }
                })




# logger.debug("Dynamic Producer started ")
# t1 = ParserDynamicProducer()
# t1.start()

while True:
    t1 = ParserDynamicProducer()
    t1.setDaemon(True)
    t1.start()
    time.sleep(60)









# def QueueGetCount(self):
    #     '''
    #     To get Count How many Messages is in Queue
    #     :return:
    #     '''
    #     args = {}
    #     args["x-max-length"] = 100000
    #     self.Count_QUEUE1 = self.channel.queue_declare(queue='RS', durable=True,
    #                                                   arguments=args).method.message_count
    #
    #     return self.Count_QUEUE1














