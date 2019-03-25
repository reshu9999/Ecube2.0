#!/usr/bin/python
import pymysql
import pika
import datetime
import pymongo
from pymongo import MongoClient


import pymysql
from pymongo import MongoClient
from Common import Commmon


import csv

client = MongoClient('localhost', 27017)
mongodb = client.HTMLDumps
#reportPath = 'http://ecxusubt07.eclerx.com:5000/fetchreport/'

reportPath = "http://127.0.0.1:5000/fetchreport/"


# db = pymysql.connect(host="192.168.8.67",
#                      user="tech",
#                      passwd="eclerx#123",
#                      db="eCube_Centralized_DB")


# db = pymysql.connect(host="localhost",
#                      user="tech",
#                      passwd="eclerx#123",
#                      db="eCube_Centralized_DB")

db = pymysql.connect(host="192.168.8.37",
                     user="tech",
                     passwd="eclerx#123",
                     db="eCube_Centralized_DB")

# db = pymysql.connect(host="192.168.131.23",
#                      user="tech",
#                      passwd="Eclerx#123",
#                      db="eCube_Centralized_DB")


class DBconnection:

    ##### Report QUEUE

    def GetInQueRequest(self):

        cur = db.cursor()
        print("OK Connected")
        try:
            cur.callproc('sp_GetInQueRequest', args=(""))
            db.commit()
        except Exception as e:
            print("Stored Procedure not properly execued")

            db.close()
        return cur

    def GetCrawlResponse(self,id):
        resultData = []


        result = mongodb.CrawlResponse.find({'RequestRunId': int(id)})
        print("Report Get Crawl Function Called",result)

        for item in result:

            finaldict = Commmon.entries_to_remove(item)
            resultData.append(finaldict)
        return resultData


    def UpdateReportStatus(self,requestRunId, status):
        cur = db.cursor()
        print("Report Update Status Function called")
        try:
            cur.callproc('sp_UpdateReportStatus', args=(requestRunId,status))
            db.commit()
        except Exception as e:
            print("Stored Procedure not properly executed - sp_UpdateReportStatus",str(e))

        #db.close()
        return cur

    def SaveReportLink(self, requestRunId, reportName):
        reportLink = reportPath+ reportName
        print("****************",reportLink)
        print(reportName)
        print(requestRunId)
        cur = db.cursor()
        print("Save Report Link function called")
        try:
            cur.callproc('sp_UpdateReportLink', args=(requestRunId, reportLink))
            db.commit()
        except Exception as e:
            print("Stored Procedure not properly executed --- sp_UpdateReportLink",str(e))

            #db.close()
        return cur




