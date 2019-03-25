import datetime
import pymysql
import schedule
import CommonConnection
import time


def ReportingCount():
    print("Stored Procedure Started Time ", datetime.datetime.now())

    db = CommonConnection.MySQLConnection()
    cur = db.cursor()
    cur.callproc("sp_UpdateRequestRundetailReporting")
    db.commit()

    # cur.callproc("SP_updateTotalCompletedPNFCounts")
    # db.commit()


    cur.close()
    db.close()
    print("Updated Successfully")
    print("END Time", datetime.datetime.now())

    return True



print("Scheduler Started Time ",datetime.datetime.now())

schedule.every(0.25).minutes.do(ReportingCount)
while True:
    schedule.run_pending()





#ReportingCount()











