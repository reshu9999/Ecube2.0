import pika
import time
import threading
import pymysql
from threading import active_count
from eCubeLog import logger
import CommonConnection


class DynamicProducer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        args = {}
        args["x-max-length"] = 100000000
        args['x-max-priority'] = 9

        logger.debug("Dynamic Queue Connection established")

    def MessageQueryCall(self):

        logger.debug("Dynamic Scrapping Producer -- Queue Called")


        db = CommonConnection.MySQLConnection()

        DBMeesages = db.cursor()
        '''
        SP Called Location 

        '''
        # DBMeesages.execute("select  SubRequestId,RequestId,RequestRunId,RequestinputdetailId from tbl_CrawlRequestDetail ")

        try:
            DBMeesages.callproc('MessagingCategoryQueue', args=(""))
            db.commit()
        except Exception as e:
            print("Stored Procedure not properly executed", e)

        message = DBMeesages.fetchall()
        logger.debug("Dynamic Queue Db Connection called")

        DBMeesages.close()
        db.close()

        return message

    def run(self):
        logger.debug("Dynamic Scrapping Producer --- Main function  Called")

        # Count_Queue1, Count_Queue2, Count_Queue3 = DynamicProducer.QueueGetCount(self)

        '''
        Database Query Call 
        '''

        message = DynamicProducer.MessageQueryCall(self)

        if message:
            for row in message:
                row_list = [("RequestId", row[0]),
                            ("SubRequestId", row[1]),
                            ("RequestRunId", row[2]),
                            ("RequestUrl", str(row[3]) or str('')),
                            ('IsCategory', row[4]),
                            # ('IsCategory', str(row[4]) or str('')),    # commented for mouser testing
                            ("DomainName", row[5] or str('')),
                            ('ParserScript', row[6] or str('')),
                            ('ScraperScript', row[7] or str('')),
                            ("PointOfSale", row[8] or str('')),
                            ('Country', row[9] or str('')),
                            ('Region', "India"),
                            ('GroupName', row[10] or "")
                            ]

                print("Crawler Producer Input Dictionary", row_list)
                data_row_dict = dict(row_list)

                '''
                
                Re  Crawl Priority Queue Set == 9
                '''
                priority = 9
                self.channel.basic_publish(exchange='',
                                           routing_key=str(data_row_dict['GroupName']),
                                           body=str(data_row_dict),
                                           properties=pika.BasicProperties(
                                            delivery_mode=2,
                                            priority=priority
                                           )
                                           )
                print("Queue Sending Messages", data_row_dict)

        self.connection.close()

        logger.debug("Dynamic Queue Connection closed successfully")


# logger.debug("Dynamic Producer Scrapping started ")
# t1 = DynamicProducer()
# t1.start()

while True:
    t1 = DynamicProducer()
    t1.setDaemon(True)
    t1.start()
    time.sleep(60)
