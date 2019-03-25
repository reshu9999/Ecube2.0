import schedule
import datetime
import pymysql
import requests
import time
import csv
from bson.codec_options import CodecOptions
from bson.son import SON

folderPath = '/home/tech/Reports/'
from pymongo import MongoClient

# from Common.config_coordinator import config_fetcher
# mysql_config = config_fetcher.get_mysql_config
# services_config = config_fetcher.get_services_config
# MONGODB_CONFIG = config_fetcher.get_mongodb_config


class ScheduleRequestRun:
    def getConnection(self):
        try:
            # db = pymysql.connect(host=mysql_config['HOST'],
            #                      user=mysql_config['USER'],
            #                      passwd=mysql_config['PASSWORD'],
            #                      db=mysql_config['DB'],
            #                      autocommit=True)
            db = pymysql.connect(
                host="10.100.18.85",
                user="tech",
                passwd="eclerx#123",
                db="eCube_Centralized_DB",
                autocommit=True)
            cur = db.cursor()
        except pymysql.DatabaseError as d:
            print(d.args[0])

        return cur

    def getMongoDbConnection(self):
        client = MongoClient('mongodb://localhost:27017/')
        # client = MongoClient(MONGODB_CONFIG['URL'])
        db = client.HTMLDumps
        return db

    def getMongoData(self, reqRunId):
        db = self.getMongoDbConnection()
        opts = CodecOptions(document_class=SON)
        collection_son = db.CrawlResponse.with_options(codec_options=opts)
        finalRecordList = []

        records = collection_son.find({
            'RequestRunId': int(reqRunId)
        }, {"_id": 0})

        for val in records:
            finalRecordList.append(val)

        return finalRecordList

    def getdataRequestRunId(self):
        cur = self.getConnection()
        cur.callproc('GetRequestRunIdForCSV', args=(""))
        obj_list = cur.fetchall()

        for row in obj_list:
            requestRun_Id = str(row[0])
            requestrunidlist = self.getMongoData(requestRun_Id)
            valMessage = self.createCSVReport(requestrunidlist, folderPath,
                                              requestRun_Id)

    def createCSVReport(self, objData, folderPath, filename):
        report_data = open(folderPath + "Batch_" + filename, 'w', newline='')
        csvwriter = csv.writer(report_data)
        for count, data in enumerate(objData):
            if count == 0:
                header = data.keys()
                csvwriter.writerow(header)
                csvwriter.writerow(data.values())
        report_data.close()
        return "Report created on location " + folderPath + "Batch_" + filename + " Successfully."



# start_Scheduler()


while True:
    r = ScheduleRequestRun()
    k = r.getdataRequestRunId()
    time.sleep(60)


# r = ScheduleRequestRun()
# k = r.getdataRequestRunId()

# "_id":0,"comPrice_8":1,"comPrice_1":1,"comStockQty_5":1,
#                 "UOM":1,"nvcrISPN":1,"volume_discount1":1,
#                 "comBreak_9":1,"comBreak_10":1,
#                 "comBreak_1":1,"manPartId":1,
#                 "comStockLoc_4":1,"Weight_KG":1,
#                 "RoHsCompliance":1,"Ordermultiplequantity":1,
#                 "comBreak_8":1,"IsCategory":1,
#                 "manPackQty":1,"comPrice_10":1,
#                 "comCategory_L3":1,"comCategory_L1":1,
#                 "comStockQty_1":1,"Country_of_Origin":1,
#                 "comPrice_4":1,"comCategory_L4":1,
#                 "comBreak_6":1,"comStockLoc_1":1,
#                 "comStockQty_3":1,"comPrice_6":1,
#                 "comStockQty_4":1,"comPrice_5":1,"requestId":1,"TechnicalDataSheetURL":1,"manName":1,
#                 "Specification":1,"comPrice_7":1,
#                 "status":1,"RequestRunId":1,"comBreak_2":1,
#                 "volume_discount3":1,"Packaging":1,
#                 "comStockLoc_2":1,"inDateAdded":1,
#                 "comBreak_7":1,"DomainName":1,
#                 "Customs_Tarrif_No":1,"comPrice_2":"1",
#                 "comProductURL":1,"comStockLoc_3":1,
#                 "comStockLoc_5":1,"subRequestId":1,
#                 "comBreak_5":1,"EANnumber":1,
#                 "comPromotion":1,"volume_discount7":1,"manPartDesc":1,
#                 "rsCompetitorId":1,"comBreak_4":1,"Minimumorderquantity":1,"rsMarketId":1,"volume_discount5":1,
#                 "comPrice_9":1,"RequestUrl":1,"comImageURL":1,"comOrderCode":1,"volume_discount4":1,
#                 "comCategory_L2":1,"comBreak_3":1,"volume_discount6":1,"Was_price":1,"volume_discount2":1,
#                 "comPrice_3":1,"comCurrency":1,"comStockQty_2":1