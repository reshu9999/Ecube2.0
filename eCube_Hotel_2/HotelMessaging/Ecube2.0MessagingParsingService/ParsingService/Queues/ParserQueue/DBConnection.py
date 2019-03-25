#!/usr/bin/python
import pymysql
import pika
import datetime
import pymongo
from pymongo import MongoClient
import pymysql
from pymongo import MongoClient


# Common  File for Report Queue
# from Common import Commmon


import csv

client = MongoClient('192.168.8.69',27017)
db = client.HTMLDumps

db = pymysql.connect(host="192.168.131.23",
                     user="tech",
                     passwd="Eclerx#123",
                     db="eCube_Centralized_DB")

# db = pymysql.connect(host="192.168.7.134",
#                      user="tech",
#                      passwd="eclerx#123",
#                      db="eCube_Centralized_DB")

class DBconnection:

    def ParserQueueConnection(self):
        print("Parser Database Called ")

        # client = MongoClient('192.168.7.134', 27017)
        # db = client.HTMLDumps

        client = MongoClient('localhost', 27017)
        db = client.HTMLDumps


        last_updated_date = db.ParserQueueUpdate.find_one({'_id': 1})
        Last_Parser_update_date = last_updated_date['QueueUpdateDateTime']

        records = db.HTMLRepository.find({'TimeStamp': {'$gte': Last_Parser_update_date}})



        if records:

            SYSdate = datetime.datetime.now()
            db.ParserQueueUpdate.update(
                {
                    'PARSER': '1'
                },
                {
                    "$set": {'QueueUpdateDateTime': datetime.datetime.strftime(SYSdate, '%Y-%m-%d %H:%M:%S')}
                })

        return records




 # '''
 #            Parsing Queury
 #        '''
 #
 #        #records = db.HTMLRepository.find({'$and' : [{'TimeStamp': {'$gte': Last_Parser_update_date}}, {'Error':"0"}]})
 #
 #
 #        '''
 #        Temporary re-parsing query
 #        '''
 #
 #        records = db.HTMLRepository.find({'requestId':'416'})
 #
 #        '''
 #        1.  comment if records block query for Re-Parsing
 #        2. Uncomment if records query block for Parsing
 #
 #        '''
