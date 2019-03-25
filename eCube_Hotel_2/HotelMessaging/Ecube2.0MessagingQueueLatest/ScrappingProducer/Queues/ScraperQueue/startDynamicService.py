import  ToGetRequests

from multiprocessing import Process
from time import sleep
from eCubeLog import logger

sleeptime=30

def getreq():
    while True:
        ToGetRequests.getRequest()
        sleep(sleeptime)



logger.info('Attempting GetRequest. ')
p1=Process(target=getreq,args=())
p1.start()
logger.info('GetRequest Process Started. ')


