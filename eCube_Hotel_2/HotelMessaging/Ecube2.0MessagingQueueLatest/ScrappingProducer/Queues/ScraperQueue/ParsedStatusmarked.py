import pymysql
from pymongo import MongoClient
from time import  sleep
import CommonConnection

class ParsedStatus:

    def __init__(self):

        self.mongodb = CommonConnection.MongoConnection()
        self.db = CommonConnection.MySQLConnection()
        self.RabbitCon = CommonConnection.RabbitMQConnection()
        self.IPAddr = CommonConnection.ServivesIP()


    def FetchParsedDataMongo(self):

        #records = self.mongodb.ParsedData.find({'requestId':212}).limit(100)
        records = self.mongodb.CrawlResponse.find({'ParsedStatus':{'$ne':'MarkedParsed'}})


        ParsedSubRequestIDList = []

        for row in records:

            ParsedSubRequestIDList.append(row['subRequestId'])


        return ParsedSubRequestIDList


    def  MarkedParsedMongo(self,ParsedSubRequestIDList):
        cnt = 0
        for ParsedStatuUpdate in ParsedSubRequestIDList:

            UPDATE  = self.mongodb.CrawlResponse.update_one(
                {'subRequestId':ParsedStatuUpdate},
                {
                    '$set':
                        {'ParsedStatus':'MarkedParsed'}
                }
            )
            cnt += 1


        print("Messages Marked Parsed in Parsed Mongo table ---",str(cnt))



    def UpdateParsedStatusMySQL(self):
         ParsedSubRequestIDList = ParsedStatus.FetchParsedDataMongo(self)

         UpdatedParsedStatus = ParsedStatus.MarkedParsedMongo(self,ParsedSubRequestIDList)

         cur = self.db.cursor()
         for subID in ParsedSubRequestIDList:

             # cur.execute("select * from tbl_CrawlRequestDetail where SubRequestId = %s ",(subID))
             # print(cur.fetchall())
            '''
            Status Update in CrawlRequestDetail table Status = "Parsed" [Status ID = 8] for Parsed Recrawl
            '''
            cur.execute("update tbl_CrawlRequestDetail set FK_StatusId = 12 where SubRequestId = %s and  FK_StatusId  = 11",(subID))
            self.db.commit()
         cur.close()
         self.db.close()

while True:
    Parsed_obj = ParsedStatus()
    Parsed_obj.UpdateParsedStatusMySQL()
    sleep(120)