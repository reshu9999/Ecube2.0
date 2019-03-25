#!/usr/bin/python
import pika
from resources.connections import MySQLBaseHandler, MongoDBBaseHandler
from resources.config_fetcher import reporting_config


class DBconnection(MySQLBaseHandler, MongoDBBaseHandler):

    META_KEYS = ('_id', 'RequestId', 'SubRequestId', 'RequestRunId', 'DomainName', 'PointOfSale', 'ProxyIp',
                 'ProxyUserName', 'ProxyPort', 'CategoryScrappingScript', 'ProductScrappingScript',
                 'ProductParsingScriptName', 'IsCategory', 'ScrapingStarttime', 'ScrapingEndtime', 'ParsingStarttime',
                 'ParsingEndtime')

    def __init__(self):
        MySQLBaseHandler.__init__(self, **reporting_config.get_pymysql_kwargs)
        MongoDBBaseHandler.__init__(self, reporting_config.get_mongodb_config['URL'])

    @classmethod
    def entries_to_remove(cls, data):
        for key in cls.META_KEYS:
            if key in data:
                del data[key]
        return data

    @property
    def GetInQueRequest(self):
        cur = self._cursor
        print("OK Connected")
        try:
            cur.callproc('sp_GetInQueRequest', args=(""))
            self._db.commit()
        except Exception as e:
            print("Stored Procedure not properly executed")

        return cur

    def GetCrawlResponse(self, requestRunId):
        resultData = []

        result = self.client.HTMLDumps.CrawlResponse.find({'RequestRunId': int(requestRunId)})
        print("Report Get Crawl Function Called", result)

        for item in result:
            finaldict = self.entries_to_remove(item)
            resultData.append(finaldict)

        return resultData

    def UpdateReportStatus(self, requestRunId, status):
        cur = self._cursor
        print("Report Update Status Function called")
        try:
            cur.callproc('sp_UpdateReportStatus', args=(requestRunId, status))
            self._db.commit()
        except Exception as e:
            print("Stored Procedure not properly executed - sp_UpdateReportStatus", str(e))

        return cur


class RabbitConnection:

    @classmethod
    def report_queue(cls):
        credentials = pika.PlainCredentials('guest', 'guest')

        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='Report', durable=True)
        return channel
