import pymysql
from pymongo import MongoClient
import  time
import CommonConnection
class PNFStatus:

    def __init__(self):

        self.mongodb = CommonConnection.MongoConnection()
        self.db = CommonConnection.MySQLConnection()
        self.RabbitCon = CommonConnection.RabbitMQConnection()
        self.IPAddr = CommonConnection.ServivesIP()

    def FetchPNFDataMongo(self):

        #records = self.mongodb.PNFData.find({'requestId':212}).limit(100)
        records = self.mongodb.PNFData.find({'PNFStatus':{'$ne':'MarkedPNF'}}).limit(100)


        PNFSubRequestIDList = []

        for row in records:

            PNFSubRequestIDList.append(row['subRequestId'])


        return PNFSubRequestIDList


    def  MarkedPNFMongo(self,PNFSubRequestIDList):
        cnt = 0
        for PNFStatuUpdate in PNFSubRequestIDList:

            UPDATE  = self.mongodb.PNFData.update_one(
                {'subRequestId':PNFStatuUpdate},
                {
                    '$set':
                        {'PNFStatus':'MarkedPNF'}
                }
            )
            cnt += 1


        print("Messages Marked PNF in PNF Mongo table ---",str(cnt))



    def UpdatePNFStatusMySQL(self):
         PNFSubRequestIDList = PNFStatus.FetchPNFDataMongo(self)

         UpdatedPNFStatus = PNFStatus.MarkedPNFMongo(self,PNFSubRequestIDList)

         cur = self.db.cursor()
         for subID in PNFSubRequestIDList:

             # cur.execute("select * from tbl_CrawlRequestDetail where SubRequestId = %s ",(subID))
             # print(cur.fetchall())
            '''
            Status Update in CrawlRequestDetail table Status = "PNF" [Status ID = 8] for PNF Recrawl
            '''
            cur.execute("update tbl_CrawlRequestDetail set FK_StatusId = 8 where SubRequestId = %s and FK_StatusId = 11",(subID))
            self.db.commit()
         cur.close()
         self.db.close()

while True:
    pnf_obj = PNFStatus()
    pnf_obj.UpdatePNFStatusMySQL()
    time.sleep(120)