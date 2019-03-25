import pika
import time
import threading
import pymysql
from threading import active_count
from eCubeLog import logger
import CommonConnection

class DynamicProducer():

    def __init__(self):
        #threading.Thread.__init__(self)
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

        DBMeesages.callproc("MessagingCategoryQueue")

        message = DBMeesages.fetchall()
        logger.debug("Dynamic Queue Db Connection called")

        DBMeesages.close()
        db.close()

        return message

    def UpdateStatusPushedToQueue(PushedQueueID):
        '''
        Update Status -- Message Pushed to Queue  in CrawlRequestDetails table using SubRequestId

        :return:
                '''

        Statusdb = CommonConnection.MySQLConnection()
        Statuscur = Statusdb.cursor()
        cnt = 0
        PushedQueueID = PushedQueueID
        for SubID in PushedQueueID:

            Statuscur.execute("update  tbl_CrawlRequestDetail set FK_StatusId = 11 where SubRequestId = %s ", (SubID))
            Statusdb.commit()
            cnt += 1

        Statuscur.close()
        Statusdb.close()
        print("Successfully updated Status -- Pushed in Queue Count-----",str(cnt))
        return "Successfully updated Status"


    def DomainWiseFetchALL(self,obj_list):

        NewMessageDump = []
        obj_types = {obj['DomainName']: list() for obj in obj_list}
        batch_obj_list = {o_t: [o for o in obj_list if o['DomainName'] == o_t] for o_t in obj_types}
        BATCH_LIMIT = 500
        final_batch = list()
        to_break = False
        while not to_break:
            for obj_type, obj_type_list in batch_obj_list.items():
                batch = list()
                batch_limit = BATCH_LIMIT if len(obj_type_list) > BATCH_LIMIT else len(obj_type_list)
                for i in range(0, batch_limit):
                    batch.append(obj_type_list.pop(0))
                if batch:
                    final_batch.append(batch)


            #to_break = True
            # for obj_type, obj_type_list in batch_obj_list.items():
            #     if obj_type_list:
            #         to_break = False

            # Below is added to paused data after getting 10 10 [diffrent domain messages]

            if len([True for b in batch_obj_list.values() if b]) == 1:
                to_break = True


        for data in final_batch:
                 for data in data:

                     #print(data['SubRequestId'],data['DomainName'])
                     NewMessageDump.append(data)

        #print("MULTIDOMAIN SUBREQUEST ID",NewMessageDump)
        return NewMessageDump


    def SingleDomainEntry(self,DumpDict):
        domain_names = set()
        l = []
        for newDump in DumpDict:
            a = (newDump['DomainID'])
            l.append(a)
            domain_names.add(newDump['DomainName'])

        newdata = set(l)
        domain_names = list(domain_names)
        lDATA = (list(newdata))
        if len(lDATA) == 1:
            set_of_10s = []
            counter = [0] * len(lDATA)
            #print(len(DumpDict))

            for message in DumpDict:

                if counter[domain_names.index(message['DomainName'])] >= 500:
                    continue
                else:
                    set_of_10s.append(message)
                    counter[domain_names.index(message['DomainName'])] += 1

            # for row in set_of_10s:
            #     print(row['DomainID'], row['DomainName'], row['SubRequestId'])

            return set_of_10s

    def run(self):
        logger.debug("Dynamic Scrapping Producer --- Main function  Called")

        '''
        Database Query Call 
        '''

        message = DynamicProducer.MessageQueryCall(self)

        if message:
            DumpDict = []
            l = []

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
                            ('GroupName', row[10] or ""),
                            ("DomainID", row[11] or str('')),
                            ("BusinessType", "Retail")
                            ]

                data_row_dict = dict(row_list)

                data_row_dict.update({"RequestInput": {"RequestUrl": data_row_dict['RequestUrl']}})

                #print("Crawler Producer Input Dictionary", data_row_dict)

                DumpDict.append(data_row_dict)

            for newDump in DumpDict:
                a = (newDump['DomainID'])
                l.append(a)
            newdata = set(l)
            lDATA = (list(newdata))

            if len(lDATA) > 1:

                NewMessageDump = DynamicProducer.DomainWiseFetchALL("", DumpDict)
                Multi_SubRequest = []
                for message in NewMessageDump:
                    self.channel.basic_publish(exchange='', routing_key=str(message['GroupName']),
                                               body=str(message))
                    print("Queue Sending Multiple Domain Messages -----------", message)

                    Multi_SubRequest.append(message['SubRequestId'])

                MultiStatusUpdate = DynamicProducer.UpdateStatusPushedToQueue(Multi_SubRequest)

                print("Messages Pushed in  and Status updated  in MySQl crawl table")


            else:

                Single_SubRequest = []
                SingleFetch = DynamicProducer.SingleDomainEntry("", DumpDict)
                cnt = 0

                for single_message in SingleFetch:
                    self.channel.basic_publish(exchange='', routing_key=str(single_message['GroupName']),
                                               body=str(single_message))


                    print("Queue Sending Single Domain Messages ------------", single_message)

                    Single_SubRequest.append(single_message['SubRequestId'])
                    cnt +=1



                MultiStatusUpdate = DynamicProducer.UpdateStatusPushedToQueue(Single_SubRequest)


                if MultiStatusUpdate == "Successfully updated Status":

                    time.sleep(10)
                    t2 = DynamicProducer()
                    #t2.start()

        self.connection.close()
        logger.debug("Dynamic Queue Connection closed successfully")


logger.debug("Dynamic Producer Scrapping started ")
# t1 = DynamicProducer()
# t1.start()
print("SCRIPT CALLED --- ")
while True:
    t1 = DynamicProducer()
    t1.run()
    # t1.setDaemon(True)
    # t1.start()
    time.sleep(10)























'''
Below Code Commented Code is used for QUEUE COunt 
'''

'''
    def QueueGetCount(self):

        args = {}
        args["x-max-length"] = 100000000
        args['x-max-priority'] = 9

        self.Count_QUEUE1 = self.channel.queue_declare(queue='RS', durable=True,
                                                      arguments=args).method.message_count
        self.Count_QUEUE2 = self.channel.queue_declare(queue='Arrow', durable=True,
                                                       arguments=args).method.message_count

        self.Count_QUEUE3 = self.channel.queue_declare(queue='Conrad', durable=True,
                                                       arguments=args).method.message_count

        return self.Count_QUEUE1,self.Count_QUEUE2,self.Count_QUEUE3



    def DatabaseQueryCall(self):

        db = pymysql.connect(host="localhost",
                             user="root",
                             passwd="root@123",
                             db="eCube_Centralized_DB")

        group = db.cursor()
        group.execute("select * from tbl_Bli_GroupMaster")

    #     return group,db

'''

# def start():
#
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#
#     args = {}
#     args["x-max-length"]= 10000
#
#     channel.queue_declare(queue='MyQUEUE_1', durable=True, arguments=args)
#     channel.queue_declare(queue='MyQUEUE_2', durable=True, arguments=args)
#
#
#     count_hello = channel.queue_declare(queue='MyQUEUE_1', durable=True, arguments=args).method.message_count
#     count_hello1 = channel.queue_declare(queue='MyQUEUE_2', durable=True, arguments=args).method.message_count
#     print(count_hello, count_hello1)
#
#     for a in range(1000):
#
#         if count_hello <= count_hello1:
#             channel.basic_publish(exchange='', routing_key='MyQUEUE_1', body='AnkushLambe'+str(a))
#             # print("Message Sending", a)
#         else:
#
#             channel.basic_publish(exchange='', routing_key='MyQUEUE_2', body='XXXXXXXXXXX' + str(a))
#
#     connection.close()
#
# start()

