# import time
# import threading
import datetime
from queues.consumer import DynamicConsumer

obj = DynamicConsumer()
# t1 = threading.Thread(target=obj.DynamicParserMain, args=())
# t1.start()
print("Dynamic parser Consumer running Time", datetime.datetime.now())
# time.sleep(0.1)
obj.DynamicParserMain()

