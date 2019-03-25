import time
import json

from queues.connections import MySQLConnection, RabbitConnection
from queues.core import QueueLogger as QL

from datetime import date, datetime, timedelta


# TODO: aetos: Remove DB Logic From Producer Classes
class RequestProducer(MySQLConnection):

    def getRequest(self):
        cur = self.get_cursor
        print("running")
        print('Database Connection Established')

        try:
            # if True:
            cur.callproc('spGetRequestRunDetail')
            res = cur.fetchall()
            # from pdb import set_trace; set_trace()
            for r in res:
                print(r)
                print(r[0], r[1], r[-1])
                self.SaveRequest(r[0], r[1], r[-1], cur)
                self.UpdateStatus(r[0], cur)
            cur.close()
        except Exception as e:
            print('Error Returned  by spGetRequestRunDetail Query "%s"' % str(e))
        self.clean_connections()
        return True

    def SaveRequest(self, RequestRunId, RequestId, ReqModeId, cur):
        try:
            args = [RequestId, RequestRunId, ReqModeId]

            if ReqModeId == 1:
                cur.callproc(procname='spInsertRequestDetails', args=args)
            if ReqModeId in (2, 3):
                args1 = [RequestId]
                cur.callproc('spGetPreCrawlDetails', args=args1)
                res = cur.fetchall()
                for i in res:
                    if i[6] == 1:  # Based on Boardtype ID.
                        startDate = i[4]
                        endDate = i[5]
                        for n in range((endDate - startDate).days + 1):
                            thisdate = startDate + timedelta(n)
                            if thisdate.strftime('%A') in i[7]:
                                args2 = [i[1], RequestRunId, i[0], thisdate]
                                print('Arg2', args2)
                                if ReqModeId == 2:
                                    cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                                elif ReqModeId == 3:
                                    cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                        self.connection.commit()
                    elif i[6] == 2:
                        for advancedt in i[10].split(','):
                            thisdate = date.today() + timedelta(int(advancedt))
                            args2 = [i[1], RequestRunId, i[0], thisdate]
                            print('Arg2', args2)
                            if ReqModeId == 2:
                                cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                            elif ReqModeId == 3:
                                cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                        self.connection.commit()
                    elif i[6] == 3:
                        for advancedt in i[10].split(','):
                            thisdate = datetime.strptime(advancedt, '%m/%d/%Y').date()
                            args2 = [i[1], RequestRunId, i[0], thisdate]
                            print('Arg2', args2)
                            if ReqModeId == 2:
                                cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                            elif ReqModeId == 3:
                                cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                        self.connection.commit()
                    elif i[6] == 4:
                        for advancedt in i[10].split(','):
                            thisdate = date.today() + timedelta(int(advancedt) * 7)
                            args2 = [i[1], RequestRunId, i[0], thisdate]
                            print('Arg2', args2)
                            if ReqModeId == 2:
                                cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                            elif ReqModeId == 3:
                                cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                        self.connection.commit()
        except Exception as e:
            print('Error Returned  by spInsertRequestDetails Query', str(e))
            return json.dumps({'StatusCode': 500, 'ResultData': e})

    def UpdateStatus(self, RequestRunId, cur):
        print('updated')
        try:
            args = [RequestRunId]
            cur.callproc('spUpdateRequestStatus', args)
            self.connection.commit()
        except Exception as e:
            print('Error Returned  by spUpdateRequestStatus Query', str(e))
            return json.dumps({'StatusCode': 500, 'ResultData': e})


# TODO: aetos: Remove DB Logic From Producer Classes
class HotelCrawling(object):
    MYSQL_CONNECTION = MySQLConnection
    QUEUE_CONNECTION = RabbitConnection

    def __init__(self):
        self.queue_conn = self.QUEUE_CONNECTION().connection
        self.mysql_conn = self.MYSQL_CONNECTION()
        self.channel = self.queue_conn.channel()

        args = {"x-max-length": 100000000, 'x-max-priority': 9}

        print("Dynamic Queue Connection established")

    def MessageQueryCall(self):

        print("Dynamic Scrapping Producer -- Queue Called")

        cur = self.MYSQL_CONNECTION().get_cursor
        '''
        SP Called Location 

        '''

        cur.callproc("MessagingHotelQueue")

        message = cur.fetchall()
        print("Dynamic Queue HOTEL  Db Connection called")

        cur.close()

        return message

    def UpdateStatusPushedToQueue(self, PushedQueueID):
        '''
        Update Status -- Message Pushed to Queue  in CrawlRequestDetails table using subRequestId

        :return:
        '''

        cur = self.mysql_conn.get_cursor
        cnt = 0
        PushedQueueID = PushedQueueID
        for SubID in PushedQueueID:
            cur.execute(
                "update  tbl_HotelCrawlRequestDetail set StatusId = 11 where HotelCrawlRequestDetailId = %s ", (SubID))
            self.mysql_conn.connection.commit()
            cnt += 1

        cur.close()
        print("Successfully updated Status -- Pushed in Queue Count-----", str(cnt))
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

            if len([True for b in batch_obj_list.values() if b]) in (0, 1):
                to_break = True

        for data in final_batch:
            for data in data:
                # print(data['subRequestId'],data['DomainName'])
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

            return set_of_10s

    def run(self):
        print("Dynamic Scrapping Producer --- Main function  Called")

        '''
        Database Query Call 
        '''
        message = self.MessageQueryCall()
        if message:
            DumpDict = []
            l = []
            for row in message:
                row_list = [
                    ("requestId", row[0]),
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
                data_row_dict.update({
                    "RequestInputs": {
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
                        "room": row[22] or "",
                        "competitorId": row[23] or "",
                    }
                })

                DumpDict.append(data_row_dict)

            for newDump in DumpDict:
                a = (newDump['DomainID'])
                l.append(a)
            newdata = set(l)
            lDATA = (list(newdata))
            if len(lDATA) > 1:
                NewMessageDump = self.DomainWiseFetchALL(DumpDict)
                Multi_SubRequest = []
                for message in NewMessageDump:
                    self.channel.basic_publish(exchange='', routing_key=str(message['GroupName']),
                                               body=str(message))
                    print("Queue Sending Multiple Domain Messages -----------", message)

                    Multi_SubRequest.append(message['subRequestId'])

                MultiStatusUpdate = self.UpdateStatusPushedToQueue(Multi_SubRequest)

                print("Messages Pushed in  and Status updated  in MySQl crawl table")
            else:
                Single_SubRequest = []
                SingleFetch = self.SingleDomainEntry(DumpDict)
                cnt = 0

                for single_message in SingleFetch:
                    self.channel.basic_publish(exchange='', routing_key=str(single_message['GroupName']),
                                               body=str(single_message))

                    print("Queue Sending Single Domain Messages To '%s'------------" % single_message['GroupName'],
                          single_message)

                    Single_SubRequest.append(single_message['subRequestId'])
                    cnt += 1

                # from pdb import set_trace; set_trace()

                MultiStatusUpdate = self.UpdateStatusPushedToQueue(Single_SubRequest)

                if MultiStatusUpdate == "Successfully updated Status":
                    time.sleep(10)
                    t2 = HotelCrawling()

        self.queue_conn.close()
        self.mysql_conn.clean_connections()
        print("Dynamic Queue Connection closed successfully")
