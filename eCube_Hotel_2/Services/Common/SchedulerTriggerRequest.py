import schedule
import datetime
import pymysql
import requests
import time

from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config
services_config = config_fetcher.get_services_config

# database connection
def getConnection():
    try:
        db = pymysql.connect(host=mysql_config['HOST'],
                             user=mysql_config['USER'],
                             passwd=mysql_config['PASSWORD'],
                             db=mysql_config['DB'],
                             autocommit=True)
        cur = db.cursor()

    except pymysql.DatabaseError as d:
        print(d.args[0])

    return cur

# database connection

# trigger the request (start crawal api) on scheduled date and time.
def triggerRequest():

    try:
        cur = getConnection()
        cur.execute("SELECT SM_RequestId, scheduleDate, scheduleTime FROM tbl_ScheduleDate SD join tbl_ScheduleMaster SM on SD.FK_ScheduleMasterId = SM.ScheduleMasterId where date_format(scheduleDate, '%Y-%m-%d') = curdate() and Status = '1'")
        obj_list = cur.fetchall()

        current_time = datetime.datetime.now().time().strftime("%H:%M")
        for row in obj_list:
            request_Id = str(row[0])
            t = str(row[2])
            if str(current_time) == t[0:5]:
                requests.get("http://%s/StartCrawl?requestId=%s" % (services_config['SERVICES_IP'], request_Id))

    except pymysql.InternalError as e:
        print(e.args[0])


# this will trigger the method in per minute
def start_Scheduler(methodname):
    schedule.every().minutes.do(methodname)
    while 1:
        schedule.run_pending()
        time.sleep(1)

# start_Scheduler(triggerRequest)
triggerRequest()


# from dateutil.relativedelta import relativedelta
# six_months = date.today() + relativedelta(months=+1)
# print(six_months)
# d1 = datetime.date('2018,01,1')
# d2 = datetime.date('2018,06,31')
# print((d1.year - d2.year) * 12 + d1.month - d2.month)
# import datetime
# DayL = ['Mon','Tues','Wednes','Thurs','Fri','Satur','Sun']
# date = DayL[datetime.date(2018,1,22).weekday()] + 'day'
# #Set day, month, year to your value
# #Now, date is set as an actual day, not a number from 0 to 6.
# print(datetime.date(2018,1,22).weekday())
# print(date)
# import calendar
#
# def weekday_count(start, end):
#   start_date  = datetime.datetime.strptime(start, '%d/%m/%Y')
#   end_date    = datetime.datetime.strptime(end, '%d/%m/%Y')
#   week        = {}
#   for i in range((end_date - start_date).days):
#     day       = calendar.day_name[(start_date + datetime.timedelta(days=i+1)).weekday()]
#     week[day] = week[day] + 1 if day in week else 1
#   return week
#
# print(weekday_count("01/01/2017", "31/01/2017"))
#
# start_date  = datetime.datetime.strptime(start, '%d/%m/%Y')
# print(calendar.day_name[(start_date + datetime.timedelta(days=i+1)).weekday()])