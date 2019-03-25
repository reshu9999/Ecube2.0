import time
import schedule

from queues.request_scheduler import schedule_request

schedule.every().minutes.do(schedule_request)
while True:
    # schedule.run_pending()
    schedule_request()
    time.sleep(10)
