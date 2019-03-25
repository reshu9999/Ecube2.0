import schedule
import pymysql
import datetime
import time
from dateutil.rrule import rrule, MONTHLY
from datetime import timedelta

from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config

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

# spitl records and insert into table.
def splitRecords():

    try:
        cur = getConnection()
        cur.execute("Select ScheduleMasterId,ScheduleType,StartDate,EndDate,TriggerDayDate,SM.Time,SM.CreatedDate as ScheduleCreatedDate from tbl_ScheduleMaster SM join tbl_ScheduleTypeMaster STM on SM.SM_ScheduleTypeId = STM.ShedulId where SM.Active = 1 and STM.Active = 1 and SM.Split = 0 ")

        for row in cur.fetchall():
            Schedule_MasterId =row[0]
            Schedule_Type = row[1]
            schedule_startDate = row[2]
            schedule_endDate = row[3]
            schedule_TriggerDayDate = row[4]
            schedule_time = row[5]

            if Schedule_Type == 'Daily':
                get_Dates(Schedule_MasterId, cur, schedule_endDate, schedule_startDate, schedule_time)
            elif Schedule_Type=="Monthly":
                get_MonthlyDates(Schedule_MasterId, cur, schedule_TriggerDayDate, schedule_endDate, schedule_startDate,schedule_time)
            elif Schedule_Type=="Weekly":
                get_weeklyDates(Schedule_MasterId, cur, schedule_TriggerDayDate, schedule_endDate, schedule_startDate,schedule_time)
            elif Schedule_Type=="Once":
                cur.execute("Insert into eCube_Centralized_DB.tbl_ScheduleDate(FK_ScheduleMasterId,ScheduleDate,ScheduleTime,Status,CreatedDateTime)values(%s,%s,%s,%s,%s);",(Schedule_MasterId, schedule_startDate, schedule_time, '1', datetime.datetime.now()))
                cur.execute("update eCube_Centralized_DB.tbl_ScheduleMaster set Split = '1' where ScheduleMasterId = %s",Schedule_MasterId)

    except pymysql.InternalError as e:
        raise print(e.args[0])

    finally:
        cur.close()

# this will give you a list containing weekly dates
def get_weeklyDates(Schedule_MasterId, cur, schedule_TriggerDayDate, schedule_endDate, schedule_startDate,schedule_time):
    dayName = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    Weekly_totaldates = [schedule_startDate + timedelta(days=x) for x in range((schedule_endDate - schedule_startDate).days + 1)]
    for d in Weekly_totaldates:
        day = dayName[d.weekday()]
        comma_seprated_days = schedule_TriggerDayDate.split(',')
        for weekly_d in comma_seprated_days:
            if weekly_d == day:
                cur.execute("Insert into tbl_ScheduleDate(FK_ScheduleMasterId,ScheduleDate,ScheduleTime,Status,CreatedDateTime)values(%s,%s,%s,%s,%s);",(Schedule_MasterId, d, schedule_time, '1', datetime.datetime.now()))
    cur.execute("update tbl_ScheduleMaster set Split = '1' where ScheduleMasterId = %s",Schedule_MasterId)


# this will give you a list containing monthly dates
def get_MonthlyDates(Schedule_MasterId, cur, schedule_TriggerDayDate, schedule_endDate, schedule_startDate,schedule_time):
    comma_seprated_dates = schedule_TriggerDayDate.split(',')
    for de in comma_seprated_dates:
        strt_dt = schedule_startDate + timedelta(days=int(de) - 1)
        end_dt = schedule_endDate
        Total_Monthly_dates = [dt for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
        for monthly_d in Total_Monthly_dates:
            cur.execute("Insert into tbl_ScheduleDate(FK_ScheduleMasterId,ScheduleDate,ScheduleTime,Status,CreatedDateTime)values(%s,%s,%s,%s,%s);",(Schedule_MasterId, monthly_d, schedule_time, '1', datetime.datetime.now()))
    cur.execute("update tbl_ScheduleMaster set Split = '1' where ScheduleMasterId = %s",Schedule_MasterId)

# this will give you a list containing all of the dates
def get_Dates(Schedule_MasterId, cur, schedule_endDate, schedule_startDate, schedule_time):
    totaldates = [schedule_startDate + timedelta(days=x) for x in range((schedule_endDate - schedule_startDate).days + 1)]
    for d in totaldates:
        cur.execute("Insert into tbl_ScheduleDate(FK_ScheduleMasterId,ScheduleDate,ScheduleTime,Status,CreatedDateTime)values(%s,%s,%s,%s,%s);",(Schedule_MasterId, d, schedule_time, '1', datetime.datetime.now()))
    cur.execute("update tbl_ScheduleMaster set Split = '1' where ScheduleMasterId = %s",Schedule_MasterId)

# this will trigger the method in per minute
def start_Scheduler(methodname):
    schedule.every().minutes.do(methodname)
    while 1:
        schedule.run_pending()
        time.sleep(1)

# start_Scheduler(splitRecords)
splitRecords()