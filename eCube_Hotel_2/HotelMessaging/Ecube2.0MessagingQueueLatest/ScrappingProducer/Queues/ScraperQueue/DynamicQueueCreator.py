import pika
import pymongo
import pymysql
import datetime
# import schedule
import os
import time
import  CommonConnection


class DynamicQuening:
    def __init__(self):

        self.mongodb = CommonConnection.MongoConnection()
        self.db = CommonConnection.MySQLConnection()
        self.RabbitCon = CommonConnection.RabbitMQConnection()
        self.IPAddr = CommonConnection.ServivesIP()
        self.maxLength = 100000000
        self.maxPriority = 9


    def QueueCreatorDatabase(self):


        cur = self.db.cursor()
        cur.execute("select * from tbl_Bli_GroupMaster")
        CurData = cur.fetchall()

        cur.close()
        self.db.close()
        return CurData


    def RetailGroupSelector(self):
        cur = self.db.cursor()
        cur.execute("select * from tbl_Bli_GroupMaster  where businessType = 'Retail'")
        CurData = cur.fetchall()

        cur.close()
        self.db.close()
        return CurData


    def HotelGroupSelector(self):
        cur = self.db.cursor()
        cur.execute("select * from tbl_Bli_GroupMaster  where businessType = 'Hotel'")
        CurData = cur.fetchall()

        cur.close()
        self.db.close()
        return CurData




    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        args = {}
        #args["x-max-length"] = self.maxLength
        args['x-max-priority'] = self.maxPriority

        CurData = DynamicQuening.QueueCreatorDatabase(self)
        for rows in CurData:
            print(rows)
            Groupname = rows[1]

            self.channel.queue_declare(queue=str(Groupname), durable=True, arguments=args)
            self.channel.queue_declare(queue="Parser" + str(Groupname), durable=True, arguments=args)

        print("Queues updated")



while True:
    a = DynamicQuening()
    a.run()
    time.sleep(3600)



