# from ScrappingProducer.Queues.ScraperQueue import ToGetRequests
# from ScrappingProducer.Queues.ScraperQueue import Producer


from Queues.ScraperQueue import ToGetRequests
from Queues.ScraperQueue import HotelCrawlingProducer
# from Queues.ScraperQueue import Producer
from pdb import set_trace as st

from multiprocessing import Process
from time import sleep
from eCubeLog import logger

sleeptime = 10


def getreq():
    while True:
        ToGetRequests.getRequest()
        sleep(sleeptime)


def producer():
    # sleep(sleeptime)
    while True:
        prg = HotelCrawlingProducer.HotelCrawling()
        prg.run()
        # Producer.Crawling()
        sleep(sleeptime)


logger.info('Attempting GetRequest. ')
p1 = Process(target=getreq, args=())
p1.start()
print("ToGetRequest Started...")
logger.info('GetRequest Process Started. ')
logger.info('Attempting Producer')
p2 = Process(target=producer, args=())
p2.start()
print("HotelCrawl Started...")
logger.info('Producer Process Started. ')
