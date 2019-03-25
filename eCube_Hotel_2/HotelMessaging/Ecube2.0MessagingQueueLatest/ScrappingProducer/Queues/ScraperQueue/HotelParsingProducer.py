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

        records = self.mongodb.HTMLRepository.find({'parsingStatus': 1})
        print(records)

        if not records:

            SYSdate = datetime.datetime.now()
            self.mongodb.ParserQueueUpdate.update(
                {
                    'PARSER': '1'
                },
                {
                    "$set": {'HotelQueueUpdateDateTime': datetime.datetime.strftime(SYSdate, '%Y-%m-%d %H:%M:%S')}
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


















