import time
import datetime
from queues.producer import ReparseProducer

obj = ReparseProducer()
print("Dynamic Reparse Consumer running Time", datetime.datetime.now())

while True:
    obj.Main()
    time.sleep(10)
