#Consuming Data from the queue. 
'''
import pika
from pdb import set_trace as st

def callback(ch, method, properties, body):
    pass

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
result=channel.queue_declare()
st()
channel.basic_consume(callback, queue='ExpediaHotelCrawl', no_ack=False)
connection.close()

'''
from pyrabbit2 import Client
from crawler import executor
from time import sleep
from pdb import set_trace as st

def startConsume():
    cl=Client('localhost:15672','test','test')
    queues=[q['name'] for q in cl.get_queues()]
    for queue in queues:
        print('Queue:-->',queue)
        msg=cl.get_messages('/',queue)
        print(msg)
        if msg==200:
            print("Queue is empty, Process will check after 10 secs..")
            sleep(10)
            startConsume()
        else:
            exc=executor.ScriptHandler(msg)
            exc.execute_crawl()

startConsume()
