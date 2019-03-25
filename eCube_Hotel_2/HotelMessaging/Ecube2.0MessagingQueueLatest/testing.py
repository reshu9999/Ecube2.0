
# import pika
# import pymongo
# import pymysql
# import datetime
# # import schedule
# import os
# import time
# #import  CommonConnection
#
#
# class DynamicQuening:
#     def __init__(self):
#         self.maxLength = 10000
#         self.maxPriority = 9
#
#
#
#     def test(self):
#         self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#         self.channel = self.connection.channel()
#         args = {}
#         args["x-max-length"] = self.maxLength
#         args['x-max-priority'] = self.maxPriority
#         self.channel.queue_declare(queue=str("TestingLength"), durable=True, arguments=args)
#
#
#         print("Queues updated")
#
#
# a = DynamicQuening()
# while True:
#     a.test()
#     time.sleep(1000)
#
#
#
#
#
#
#


























# from pymongo import MongoClient
#
# # client = MongoClient('localhost', 27017)
# # db = client.HTMLDumps
#
#
# client = MongoClient('192.168.7.134', 27017)
# db = client.HTMLDumps
# record = db.RequestQueueMonitor.find({"RequestId":{'$in':[629]}}).count()
# print(record)
#
#
# [604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629]

#
# [604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629

# for data in record:
#     print(data['GroupName'])



#
# # data = db.PNFData.find({'PNFStatus':'PNF'})
# # print(data)
# # for row in data:
# #     print(row['PNFStatus'])
# datat = db.PNFData.find({"requestId":212})
#
# # new_d = db.HTMLRepository.insert({"GroupName":"RS"})
# # print(datat)
# for data in datat:
#     print(data['GroupName'])
#
# # data = db.PNFData.find({'PNFStatus':{'$ne':'MarkedPNF'}}).count()
# # print(data)
# # for row in data:
# #     print(row['PNFStatus'])
#
#
# # 784702  785802


# # last_updated_date = db.ParserQueueUpdate.find_one({'_id': 1})
# # Last_Parser_update_date = last_updated_date['QueueUpdateDateTime']
# #
# #         #records = db.HTMLRepository.find({'TimeStamp': {'$gte': Last_Parser_update_date}})
# #
# # records = db.HTMLRepository.find({'$or' : [{'TimeStamp': {'$gte': Last_Parser_update_date}}, {'Error':"0"}]})
# # for row in records:
# #     print(row)
#
#
# client = MongoClient('192.168.7.134', 27017)
# db = client.HTMLDumps
#
#
#
# # records = db.HTMLRepository.find({'TimeStamp': {'$gte': Last_Parser_update_date}})
#
# # records = db.HTMLRepository.find({'$and' : [{'TimeStamp': {'$gte': Last_Parser_update_date}}, {'Error':"0"}]})
#
# records = db.HTMLRepository.find({'subRequestId': "191235"})
