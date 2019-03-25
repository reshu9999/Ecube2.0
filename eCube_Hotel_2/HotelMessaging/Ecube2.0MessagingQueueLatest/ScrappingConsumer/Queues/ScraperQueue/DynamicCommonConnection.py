import pymysql
from pymongo import MongoClient

from config_fetcher import crawling_consumer_config


def MySQLConnection():

    '''
    MYSQL Server DB Connection string

    :return:
    '''

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

    return pymysql.connect(**crawling_consumer_config.get_pymysql_kwargs)



def MongoConnection():

    '''
        Mongo Database Connection string

    :return:
    '''
    #client = MongoClient('mongodb://192.168.7.134:27017/')
    client = MongoClient(crawling_consumer_config.get_mongodb_args)
    mongodb = client.HTMLDumps

    return mongodb

