import schedule
import time
import datetime
import pymysql


from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config

def getConnection():
    db = pymysql.connect(host=mysql_config['HOST'],
                         user=mysql_config['USER'],
                         passwd=mysql_config['PASSWORD'],
                         db=mysql_config['DB'])
    cur = db.cursor()
    return cur

# database connection


def getRequest():
    cur = getConnection()
    sql = "SELECT * FROM scheduler.ScheduleDetails where date_format(scheduleDateTime,'%Y-%m-%d') = curdate() and scheduleStatus = 'Not Started'"
    cur.execute(sql)
    obj_list = cur.fetchall()

    current_date = datetime.datetime.now()
    print(current_date)
    for row in obj_list:
        if current_date.strftime("%Y-%M-%d %H:%M") == row[2].strftime("%Y-%M-%d %H:%M"):
            print(row[2])

        # with open("testing.txt", 'wb+') as fp:
            # fp.write("date is " + str(row[2]))


schedule.every().minutes.do(getRequest)

while 1:
    schedule.run_pending()
    time.sleep(1)
# getRequest()