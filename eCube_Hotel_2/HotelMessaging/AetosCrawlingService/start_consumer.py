import time
import datetime
import threading

from time import sleep
from multiprocessing import Process
# from queues.consumer import DynamicConsumer
from queues.consumer import AetosConsumer

NoOfConsumer = 3


def newconsume():
    print('Dynamic Scrapping Consumer --- Ready to start')
    # obj = DynamicConsumer()
    obj = AetosConsumer()
    # t1 = threading.Thread(target=obj.Main, args=())
    # t1.start()
    obj.Main()
    print("Consumer running Time", datetime.datetime.now())
    time.sleep(0.1)


# for p in range(NoOfConsumer):
#     p1 = Process(target=newconsume, args=())
#     p1.start()
#     sleep(2)
#
newconsume()
