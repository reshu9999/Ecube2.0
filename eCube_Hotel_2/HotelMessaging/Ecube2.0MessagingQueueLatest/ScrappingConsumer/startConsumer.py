from Queues.ScraperQueue.DynamicScrapperConsumer import DynamicConsumer

from multiprocessing import Process
from eCubeLog import logger
from time import sleep
import sys
from os import popen
import threading
import time
import datetime
from pdb import set_trace as st

#sys.path[0]='/home/tech/Ecube2.0MessagingQueueLatest/ScrappingConsumer/Queues/ScraperQueue/'


NoOfConsumer = 1


def newconsume():
    logger.debug('Dynamic Scrapping Consumer --- Ready to start')
    obj = DynamicConsumer()
    #t1 = threading.Thread(target=obj.Main, args=())
    #t1.start()
    obj.Main()
    print("Consumer running Time", datetime.datetime.now())
    time.sleep(0.1)


# for p in range(NoOfConsumer):
#     p1=Process(target=newconsume,args=())
#     p1.start()
#     sleep(2)

newconsume()

# from Queues.ScraperQueue import ScrapperTravelRepublicPython
