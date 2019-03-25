import threading

from queues.consumer import ReportConsumer


t1 = threading.Thread(target=ReportConsumer, args=[])
t1.start()

