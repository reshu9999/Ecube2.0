#!/usr/bin/python
import datetime
import pymysql

from config_fetcher import crawling_consumer_config


class DBconnection:
    def SQL_Crawler(self):

        # db = pymysql.connect(host="192.168.8.67",
        #                      user="tech",
        #                      passwd="eclerx#123",
        #                      db="eCube_Centralized_DB")

        # db = pymysql.connect(host="localhost",
        #                      user="tech",
        #                      passwd="eclerx#123",
        #                      db="eCube_Centralized_DB")

        # db = pymysql.connect(host="192.168.8.37",
        #                      user="tech",
        #                      passwd="eclerx#123",
        #                      db="eCube_Centralized_DB")

        # db = pymysql.connect(host="192.168.131.23",
        #                      user="tech",
        #                      passwd="Eclerx#123",
        #                      db="eCube_Centralized_DB")

        db = pymysql.connect(**crawling_consumer_config.get_pymysql_kwargs)

        current_date = datetime.datetime.now()
        c_date = current_date.strftime("%d-%m-%Y %H:%M:%S")
        current_date = str(c_date)
        print("Current Date", current_date)

        cur = db.cursor()
        print("OK Connected")
        try:
            cur.callproc('MessagingCategoryQueue', args=(""))
            db.commit()
        except Exception as e:
            print("Stored Procedure not properly execued")

        db.close()
        return cur




