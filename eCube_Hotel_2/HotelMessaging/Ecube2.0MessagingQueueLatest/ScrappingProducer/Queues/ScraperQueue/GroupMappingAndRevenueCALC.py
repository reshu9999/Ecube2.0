import pymysql
import schedule
import CommonConnection


def REVENUECalculator(BLIName,GroupName, Revenue):


        db = CommonConnection.MySQLConnection()
        group = db.cursor()

        try:
            group.callproc("MessagingBLIGroupMappingMaster", args=(BLIName, GroupName, Revenue))
            db.commit()
        except Exception as e:
            print("Group Mapping SP Error")


        try:
            group.callproc("SP_updateGroupRevenue")
            db.commit()
        except Exception as e:
            print("Group Mapping SP Error")



        group.execute("select * from   tbl_Bli_GroupMaster;")
        print(group.fetchall())

REVENUECalculator("Booking","Booking",200)



# GroupDBMaster()
# redis_channel.publish('print data')
# #
# schedule.every(0.5).minutes.do(GroupDBMaster)
# while True:
#     schedule.run_pending()
