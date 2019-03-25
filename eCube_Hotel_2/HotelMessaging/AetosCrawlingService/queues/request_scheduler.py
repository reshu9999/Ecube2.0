import pymysql

from queues.core import RequestScheduler


def schedule_request():
    RequestScheduler().make_request_run_details()
