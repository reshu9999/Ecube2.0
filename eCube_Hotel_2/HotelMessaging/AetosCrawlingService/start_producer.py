from pdb import set_trace as st

from multiprocessing import Process
from time import sleep
from queues.core import QueueLogger as QL
from queues.producer import RequestProducer, HotelCrawling

sleeptime = 10


def getreq():
    while True:
        req_producer = RequestProducer()
        req_producer.getRequest()
        sleep(sleeptime)


def producer():
    # sleep(sleeptime)
    while True:
        prg = HotelCrawling()
        prg.run()
        # Producer.Crawling()
        sleep(sleeptime)


print('Attempting GetRequest. ')
p1 = Process(target=getreq, args=())
p1.start()
# getreq()
print("ToGetRequest Started...")
print('GetRequest Process Started. ')
print('Attempting Producer')
# producer()
p2 = Process(target=producer, args=())
p2.start()
print("HotelCrawl Started...")
print('Producer Process Started. ')
