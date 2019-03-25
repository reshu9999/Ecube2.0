from multiprocessing import Process
from time import sleep
import time
import datetime

from queues.core import QueueLogger as QL
# from queues.consumer import DynamicConsumer
from queues.pnf_consumer import AetosScriptTimeoutConsumer

NoOfConsumer = 3


def newconsume():
    print('Dynamic Scrapping Consumer --- Ready to start')
    # obj = DynamicConsumer()
    obj = AetosScriptTimeoutConsumer()
    # t1 = threading.Thread(target=obj.Main, args=())
    # t1.start()
    obj.Main()
    print("Consumer running Time", datetime.datetime.now())
    time.sleep(0.1)


# for p in range(NoOfConsumer):
#     p1 = Process(target=newconsume, args=())
#     p1.start()
#     sleep(2)

newconsume()
