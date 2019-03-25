import pymysql
from pymongo import  MongoClient


def MySQLConnection():

    '''
    MYSQL Server DB Connection string

    :return:
    '''

    db = pymysql.connect(host="192.168.131.23",
                         user="tech",
                         passwd="Eclerx#123",
                         db="eCube_Centralized_DB")
    # db = pymysql.connect(host="192.168.7.134",
    #                      user="tech",
    #                      passwd="eclerx#123",
    #                      db="eCube_Centralized_DB")

    return db



def MongoConnection():

    '''
        Mongo Database Connection string

    :return:
    '''
    #client = MongoClient('mongodb://192.168.7.134:27017/')
    client = MongoClient('192.168.8.69',27017)
    mongodb = client.HTMLDumps

    return mongodb
