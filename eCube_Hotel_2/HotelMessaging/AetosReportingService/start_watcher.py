import datetime
import schedule
import time

from resources.connections import MySQLBaseHandler
from resources.config_fetcher import reporting_config


def ReportingCount():
    print("Stored Procedure Started Time ", datetime.datetime.now())

    db = MySQLBaseHandler(**reporting_config.get_pymysql_kwargs)._db
    cur = db.cursor()
    # from pdb import set_trace;set_trace()
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

# ReportingCount()
