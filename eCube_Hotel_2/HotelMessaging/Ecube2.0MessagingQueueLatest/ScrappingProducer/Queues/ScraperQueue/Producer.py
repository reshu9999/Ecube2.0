# import os
# # from ScrappingProducer.Queues.ScraperQueue.DBConnection import DBconnection
# # from ScrappingProducer.Queues.ScraperQueue.RabbitConnections import  Rabbit_connection
#
# from Queues.ScraperQueue.DBConnection import DBconnection
# from Queues.ScraperQueue.RabbitConnections import  Rabbit_connection
#
# import pika
# import threading
# import schedule
# import time
# from eCubeLog import logger
# import datetime
#
#
# def CrawlingQueue():
#
#         # print("Crawler Producer Start Time", datetime.datetime.now())
#         # logger.debug('Crawler Producer Started')
#         cur = DBconnection.SQL_Crawler('')  # Calling Database connections
#         channel = Rabbit_connection.CrawlerQueueConnection('')  # Calling Producer and Queue Connections
#         test = 0
#         if cur:
#             for row in cur.fetchall():
#
#                 print("IS Category",row[4])
#                 row_list = [("RequestId", str(row[0]) or str('')),
#                             ("SubRequestId", str(row[1]) or str('')),
#                             ("RequestRunId", str(row[2]) or str('')),
#                             ("RequestUrl", row[3] or str('')),
#                             ('IsCategory', str(0)),
#                             #('IsCategory', str(row[4]) or str('')),    # commented for mouser testing
#                             ("DomainName", row[5] or str('')),
#                             ('ParserScript', row[6] or str('')),
#                             ('ScraperScript', row[7] or str('')),
#                             ("PointOfSale", row[8] or str('')),
#                             ('Country', row[9] or str('')),
#                             ('Region',"India"),
#                             ]
#
#
#                 print("Crawler Producer Input Dictionary",row_list)
#                 data_row_dict = dict(row_list)
#                 channel.basic_publish(exchange='',
#                                       routing_key='Crawler',
#                                       body=str(data_row_dict),
#                                       properties=pika.BasicProperties(
#                                           delivery_mode=2,
#                                       ))
#
#             # time.sleep(10)
#             # cur.close()
#             return True
#         else:
#             time.sleep(10)
#             CrawlingQueue()
#
# #
# if __name__=='__main__':
#     print("Crawler Producer Start Time",datetime.datetime.now())
#     logger.debug('Crawler Producer Started')
# #
# CrawlingQueue()
#
# '''
# schedule.every(0.5).minutes.do(CrawlingQueue)
# while True:
#     schedule.run_pending()
#
# '''
#
# #
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # from DBConnection import DBconnection
# # from RabbitConnections import  Rabbit_connection
# # import pika
# # import threading
# #
# # class Producer:
# #     def CrawlingQueue(self):
# #         cur = DBconnection.SQL_Crawler(self)  # Calling Database connections
# #         channel = Rabbit_connection.CrawlerQueueConnection(self)  # Calling Producer and Queue Connections
# #         test = 0
# #         # if test == 0:
# #         if cur:
# #
# #             for row in cur.fetchall():
# #                 row_list = [("RequestId", row[0] or None),
# #                             ("SubRequestId", row[1] or None),
# #                             ("RequestRunId", row[2] or None),
# #                             ("RequestUrl", row[3] or None),
# #                             ('IsCategory', row[4] or None),
# #                             ("DomainName", row[5] or None),
# #                             ('ParserScript', row[6]) or None,
# #                             ('ScraperScript', row[7] or None),
# #                             ("PointOfSale", row[8] or None),
# #                             ('Country', row[9] or None),
# #                             ('Region',"India"),
# #                             ]
# #
# #                 print(row_list)
# #                 data_row_dict = dict(row_list)
# #                 channel.basic_publish(exchange='',
# #                                       routing_key='Crawler',
# #                                       body=str(data_row_dict),
# #                                       properties=pika.BasicProperties(
# #                                           delivery_mode=2,
# #                                       ))
# #
# #             # time.sleep(10)
# #         cur.close()
# #         return True
# #
# #     def ParsingQueue(self):
# #         cur = DBconnection.SQL_Parser(self)   # Calling Database connections
# #         channel = Rabbit_connection.ParserQueueConnection(self)  # Calling Producer Connections
# #         rows = cur.fetchall()
# #         for row in rows:
# #
# #             row_list = [("RequestId", row[1] or None), ("RequestRunId", row[2] or None),
# #                         ("SubRequestId", row[3] or None), ("RequestUrl", row[4] or None),
# #                         ("DomainName", row[5] or None), ("PointOfSale", row[6]),
# #                         ('IsCategory', row[7] or None), ('CategoryScraperScript', row[8] or None),
# #                         ('ParserScript', row[9] or None)]
# #
# #             print(row_list)
# #             data_row_dict = dict(row_list)
# #
# #
# #             channel.basic_publish(exchange='',
# #                              routing_key='Parser',    # Queue name same as routing key
# #                               body=str(data_row_dict),
# #                               properties=pika.BasicProperties(
# #                               delivery_mode = 2,))
# #
# #             # time.sleep(10)
# #         cur.close()
# #         return True
# #
# # if __name__ == '__main__':
# #     pro = Producer()
# #     t1 = threading.Thread(target=pro.CrawlingQueue, args=[])
# #     # t2 = threading.Thread(target= pro.ParsingQueue, args=[])
# #     t1.start()
# #     # t2.start()
# #
