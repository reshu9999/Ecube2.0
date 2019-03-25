import pika
import time
import threading
import pymysql
from threading import active_count
from eCubeLog import logger
from Queues.ScraperQueue import CommonConnection
from pdb import set_trace as st


class HotelCrawling():

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

        DBMeesages.callproc("MessagingHotelQueue")

        message = DBMeesages.fetchall()
        logger.debug("Dynamic Queue HOTEL  Db Connection called")

        DBMeesages.close()
        db.close()

        return message

    def UpdateStatusPushedToQueue(PushedQueueID):
        '''
        Update Status -- Message Pushed to Queue  in CrawlRequestDetails table using subRequestId

        :return:
        '''

        Statusdb = CommonConnection.MySQLConnection()
        Statuscur = Statusdb.cursor()
        cnt = 0
        PushedQueueID = PushedQueueID
        for SubID in PushedQueueID:

            Statuscur.execute("update  tbl_HotelCrawlRequestDetail set StatusId = 11 where HotelCrawlRequestDetailId = %s ", (SubID))
            Statusdb.commit()
            cnt += 1

        Statuscur.close()
        Statusdb.close()
        print("Successfully updated Status -- Pushed in Queue Count-----",str(cnt))
        return "Successfully updated Status"


    def DomainWiseFetchALL(self, obj_list):

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

            if len([True for b in batch_obj_list.values() if b]) in (0,1):
                to_break = True


        for data in final_batch:
                 for data in data:

                     #print(data['subRequestId'],data['DomainName'])
                     NewMessageDump.append(data)

        return NewMessageDump


    def SingleDomainEntry(self, DumpDict):
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

            for message in DumpDict:

                if counter[domain_names.index(message['DomainName'])] >= 500:
                    continue
                else:
                    set_of_10s.append(message)
                    counter[domain_names.index(message['DomainName'])] += 1

            # for row in set_of_10s:
            #     print(row['DomainID'], row['DomainName'], row['subRequestId'])

            return set_of_10s

    def run(self):
        logger.debug("Dynamic Scrapping Producer --- Main function  Called")

        '''
        Database Query Call 
        '''
        message = HotelCrawling.MessageQueryCall(self)
        if message:
            DumpDict = []
            l = []
            for row in message:
                row_list = [("requestId", row[0]),
                            ("subRequestId", row[1]),
                            ("requestRunId", row[2]),
                            ('IsCategory', row[3]),
                            ("DomainName", row[4] or str('')),
                            ('ParserScript', row[5] or str('')),
                            ('ScraperScript', row[6] or str('')),
                            ('GroupName', row[7] or ""),
                            ("DomainID", row[8] or str('')),
                            ("RequestUrl", str('')),
                            ("PointOfSale", ''),
                            ("BusinessType", "Hotel"),
                            ("country", row[19] or "",)
                            ]

                data_row_dict = dict(row_list)
                data_row_dict.update({"RequestInputs": {
                                    "RequestUrl": data_row_dict['RequestUrl'],
                                    "checkIn": str(row[9]) or "",
                                    "nights": row[10] or "",
                                    "CompetitorName": row[11] or "",
                                    "pos": row[12] or "",
                                    "adults": row[13] or "",
                                    "children": row[14] or "",
                                    "CrawlMode": row[15] or "",
                                    "hotelName": row[16] or "",
                                    "webSiteHotelId": row[17] or "",
                                    "city": row[18] or "",
                                    "starRating": row[20] or "",
                                    "board": row[21] or "",
                                    "room": row[22] or ""
                },})

                DumpDict.append(data_row_dict)

            for newDump in DumpDict:
                a = (newDump['DomainID'])
                l.append(a)
            newdata = set(l)
            lDATA = (list(newdata))
            if len(lDATA) > 1:
                NewMessageDump = HotelCrawling.DomainWiseFetchALL("", DumpDict)
                Multi_SubRequest = []
                for message in NewMessageDump:
                    self.channel.basic_publish(exchange='', routing_key=str(message['GroupName']),
                                               body=str(message))
                    print("Queue Sending Multiple Domain Messages -----------", message)

                    Multi_SubRequest.append(message['subRequestId'])

                MultiStatusUpdate = HotelCrawling.UpdateStatusPushedToQueue(Multi_SubRequest)

                print("Messages Pushed in  and Status updated  in MySQl crawl table")


            else:

                Single_SubRequest = []
                SingleFetch = HotelCrawling.SingleDomainEntry("", DumpDict)
                cnt = 0

                for single_message in SingleFetch:
                    self.channel.basic_publish(exchange='', routing_key=str(single_message['GroupName']),
                                               body=str(single_message))


                    print("Queue Sending Single Domain Messages ------------", single_message)

                    Single_SubRequest.append(single_message['subRequestId'])
                    cnt +=1



                MultiStatusUpdate = HotelCrawling.UpdateStatusPushedToQueue(Single_SubRequest)


                if MultiStatusUpdate == "Successfully updated Status":

                    time.sleep(10)
                    t2 = HotelCrawling()


        self.connection.close()
        logger.debug("Dynamic Queue Connection closed successfully")

if __name__=='__main__':
    logger.debug("Dynamic Producer Scrapping started ")
    # t1 = DynamicProducer()
    # t1.start()
    print("SCRIPT CALLED --- ")
    while True:
        t1 = HotelCrawling()
        t1.run()
        # t1.setDaemon(True)
        # t1.start()
    time.sleep(10)
