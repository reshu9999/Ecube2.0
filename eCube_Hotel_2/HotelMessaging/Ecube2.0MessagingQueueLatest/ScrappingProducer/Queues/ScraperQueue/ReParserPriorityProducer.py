import datetime
from random import SystemRandom
from threading import Thread,active_count
from time import sleep
import pika
import schedule
from pymongo import  MongoClient
import pymysql
from eCubeLog import logger
import CommonConnection


# Rabbit MQ Connection function
def RabbitConnection():
    '''
    Rabbit MQ Connection String
    :return:
    '''
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    data = {}
    data['x-max-priority'] = 9
    channel = connection.channel()
    channel.queue_declare(queue='parser', durable=True, arguments=data)
    return channel

# Database Connection class call
def DBFetchData():
    '''
        Database Selection Query call function
        :return:
    '''

    logger.debug("Priority Parser Producer --- Database Function called")

    client = MongoClient('localhost', 27017)
    mongoDB = client.HTMLDumps

    db = CommonConnection.MySQLConnection()

    group = db.cursor()

    '''
    Status ID - 8 Is "Reparse" status in tbl_RequestRunDetail table
    '''


    group.execute("select RequestRunId from  tbl_RequestRunDetail where FK_StatusId = 10")

    data = group.fetchall()
    requestRunIDList = []
    if data:
        for row in data:
            requestRunIDList.append(row[0])

    newRequestRunId = list(set(requestRunIDList))
    messages = []
    for requestRunID in newRequestRunId:
        records = mongoDB.HTMLRepository.find(
            {'$and': [{'RequestRunId': {'$eq': str(requestRunID)}}, {'Error': "0"}]})

        for row in records:
            messages.append(row)
    if messages:
            SYSdate = datetime.datetime.now()
            mongoDB.ParserQueueUpdate.update(
                {
                    'PARSER': '1'
                },
                {
                    "$set": {'ReParseQueueUpdateDateTime': datetime.datetime.strftime(SYSdate, '%Y-%m-%d %H:%M:%S')}
                })

    if data:
        for UpdateRunID in data:
            UpdateRequestRunId =  UpdateRunID[0]


            '''
            update tbl_RequestRunDetail Status = Push to Queue After Adding Reparse status records into ReParse Queue  
            '''

            group.execute("update tbl_RequestRunDetail  set ReParseStatus = 'Running' where RequestRunId = %s",(UpdateRequestRunId))
            db.commit()


    group.close()
    db.close()


    return messages


# Database update Query call function
def UpdateRecord(SubRequestId):

    '''
    Database update Query Call function
    :param SubRequestId:
    :return:
    '''
    return True


def ProducerMain():

    messages = DBFetchData()
    channel = RabbitConnection()

    if messages:
        for row in messages:
            message  = row
            priority = 9
            print(message)
            channel.basic_publish(exchange='',
                                  routing_key='parser',
                                  body=str(message),
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,
                                      priority=priority
                                  ))



logger.debug("Priority Parser Producer called")
main = ProducerMain()


# while True:
#     print("Start:", datetime.datetime.now())
#     main = ProducerMain()
#     sleep(60)
#     print("Sleep Time ")
