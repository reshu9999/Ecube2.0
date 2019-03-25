# import time
# import threading
import datetime
from queues.consumer import ReparseConsumer

obj = ReparseConsumer()
# t1 = threading.Thread(target=obj.Main, args=())
# t1.start()
print("Dynamic Reparse Consumer running Time", datetime.datetime.now())
# time.sleep(0.1)
obj.Main()
