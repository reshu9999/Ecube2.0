import json
import time
import requests
import datetime

from queues.core import HotelAdditionCache
from resources.connections import MySQLBaseHandler
from resources.config_fetcher import reporting_config


class PostCrawlingProcess(object):

    CACHE_HANDLER = HotelAdditionCache

    def __init__(self, request_run_id):
        self.request_run_id = request_run_id
        self.cache_handler = self.CACHE_HANDLER(self.request_run_id)

    def _hotel_addition(self):
        print("Hotel Addition for RD:%s Start Time:%s" % (self.request_run_id, datetime.datetime.now()))

        db = MySQLBaseHandler(**reporting_config.get_pymysql_kwargs)._db
        cur = db.cursor()

        cur.callproc('sp_AddNewlyAdded_Hotel', [self.request_run_id])
        db.commit()

        cur.close()
        db.close()

    def _qa_checks(self):
        print("QA Checks for RD:%s Start Time:%s" % (self.request_run_id, datetime.datetime.now()))

        db = MySQLBaseHandler(**reporting_config.get_pymysql_kwargs)._db
        cur = db.cursor()
        cur.callproc('sp_GetBatchDataAfterErrorCheck_PostCrawling', [self.request_run_id])
        db.commit()

        cur.close()
        db.close()

    def _post_crawling_automation(self):
        print("Post Crawling Start Time", datetime.datetime.now())
        self.cache_handler.mark_running()
        self._hotel_addition()
        self._qa_checks()
        print("Post Crawling End Time", datetime.datetime.now())
        self.cache_handler.mark_completed()

    def run_post_crawling_automation(self):
        try:
            self._post_crawling_automation()
        except Exception as e:
            print('Post Crawling Process Failed "%s"' % str(e))
            self.cache_handler.mark_failed()


def main(queued_first=True):
    batch_running = PostCrawlingProcess.CACHE_HANDLER.get_running_req_run()
    if not batch_running:
        queued_req_run_ids = PostCrawlingProcess.CACHE_HANDLER.get_queued_req_runs()
        # failed_req_run_ids = PostCrawlingProcess.CACHE_HANDLER.get_failed_req_runs()
        if queued_req_run_ids and queued_first:
            to_run_req_run_id = queued_req_run_ids[0]
            PostCrawlingProcess(to_run_req_run_id).run_post_crawling_automation()
        # elif failed_req_run_ids:
        #     to_run_req_run_id = failed_req_run_ids[0]
        #     PostCrawlingProcess(to_run_req_run_id).run_post_crawling_automation()
    time.sleep(30)


while True:
    main()
