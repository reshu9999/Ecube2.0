import ast
from resources.connections import MySQLBaseHandler, RedisBaseHandler
from resources.config_fetcher import reporting_config


class ReportCache(RedisBaseHandler):

    NAMESPACE = 'hotel_report_lines'
    HOST = reporting_config.get_redis_config['HOST']
    PORT = reporting_config.get_redis_config['PORT']
    DB = 3

    @classmethod
    def _decode_line(cls, line):
        decoded_line = line.decode('utf-8')
        return ast.literal_eval(decoded_line)

    @classmethod
    def get_lines(cls, request_id):
        lines = list()
        # request_id = 1
        line_keys = list(cls.scan_keys('rid:%s_*' % request_id))
        # from pdb import set_trace; set_trace()
        for line_group in [cls._decode_line(cls.get_and_del_key(key.decode('utf-8').split('__')[1])) for key in line_keys]:
        # for line_group in [cls._decode_line(cls.get_key(key.decode('utf-8').split('__')[1])) for key in line_keys]:
            for line in line_group:
                lines.append(line)
        return lines


class BatchAlreadyRunning(Exception):
    pass


class BatchNotRunning(Exception):
    pass


class DifferentBatchRunning(Exception):
    pass


class HotelAdditionCache(RedisBaseHandler):

    NAMESPACE = 'hotel_addition'
    HOST = reporting_config.get_redis_config['HOST']
    PORT = reporting_config.get_redis_config['PORT']
    DB = 4

    FAILED = 'failed'
    QUEUED = 'queued'

    def __init__(self, request_run_id):
        self.req_run_id = request_run_id

    @classmethod
    def get_running_req_run(cls, clear=False):
        if cls.key_exists('current_running'):
            if clear:
                req_run = cls.get_and_del_key('current_running')
            else:
                req_run = cls.get_key('current_running')
            return int(req_run)

    @classmethod
    def _get_req_runs_by_status(cls, status=None):
        req_runs_by_status = dict()
        for key in cls.scan_keys('*'):
            if 'current' not in key.decode('utf-8'):
                req_run = int(key.decode('utf-8').split('__')[1])
                req_run_status = cls.get_key(req_run).decode('utf-8')
                if req_run_status not in req_runs_by_status:
                    req_runs_by_status[req_run_status] = [req_run]
                else:
                    req_runs_by_status[req_run_status].append(req_run)
        if status:
            return req_runs_by_status[status] if status in req_runs_by_status else list()
        return req_runs_by_status

    @classmethod
    def get_queued_req_runs(cls):
        return cls._get_req_runs_by_status(cls.QUEUED)

    @classmethod
    def get_failed_req_runs(cls):
        return cls._get_req_runs_by_status(cls.FAILED)

    @classmethod
    def get_all_req_runs(cls):
        return cls._get_req_runs_by_status()

    def _mark_current_as_running(self):
        if self.key_exists('current_running'):
            req_run_id = self.get_running_req_run()
            raise BatchAlreadyRunning('Batch RR:%s Already Running' % req_run_id)
        self.set_key('current_running', self.req_run_id)

    def _check_current(self):
        curr_req_run = self.get_running_req_run()
        if not curr_req_run:
            raise BatchNotRunning('Batch RR:%s Not Running' % self.req_run_id)
        if not curr_req_run == self.req_run_id:
            raise DifferentBatchRunning('Batch RR:%s Not RR:%s Running' % (curr_req_run, self.req_run_id))

    def _mark_finished(self):
        self._check_current()
        self.delete_key('current_running')

    def mark_queued(self):
        self.set_key(self.req_run_id, self.QUEUED)

    def mark_running(self):
        self._mark_current_as_running()
        self.delete_key(self.req_run_id)

    def mark_completed(self):
        self._mark_finished()

    def mark_failed(self):
        self._mark_finished()
        self.set_key(self.req_run_id, self.FAILED)


class ReportHandler(MySQLBaseHandler):

    BULK_INSERT = False
    REPORT_CACHE = ReportCache
    REPORT_FIELDS = [
        # "intBatchCrawlID",
        "intDiPBagDynamicId",
        "intSiteID",
        "nvcrHotelName",
        "nvcrHotelAddress",
        "ncrPostCode",
        "nvcrCity",
        "intAdult",
        "sdtmCheckinDate",
        "sdtmCheckoutDate",
        "nvcrRoomType",
        "mnyRate",
        "nvcrCurrency",
        "nvcrPagePath",
        "sintBatchCrawlStatus",
        "intSupplierId",
        "nvcrBoard",
        "nvcrAvailabilty",
        "nvcrHotelStar",
        "nvcrBreakFast",
        "nvcrCrawlDescription",
        "nvcrRcode",
        "nvcrTax",
        "nvcrCancellationPolicy",
        "nvcrClassification",
        "nvcrDailyRate",
        "nvcrContractName",
        "nvcrUniqueCode",
        "nvcrHotelCode",
        "nvcrNetPrice",
        "nvcrSellingPrice",
        "nvcrCommision",
        "nvcrDirectPayment",
        "nvcrSellingPriceMandatory",
        "nvcrXmlroomtypecode",
        "nvcrPromotion",
        "nvcrPromotionDescription",
        "nvcrHotelCount",
        "nvcrTotalHotel",
        "bitReCrawl",
        "intSubDipbagDynamicId",
        "strbreakfast",
        "strSupplier",
        "nvcrZoneinfo",
        "nvcrRoomAvailability",
        "nvcrHotelLocation",
        "nvcrTaxdesc",
        "nvcrAdult",
        "nvcrOpaqueRate",
        "nvcrLeadTime",
        "nvcrDynamicProperty",
        "nvcrSupplierHotelURL",
        "nvcrCompetitorHotelID",
        "nvcrLongitude",
        "nvcrLatitude",
        "nvcrMultipleZoneCheck",
        "nvcrGeneralInfo",
        "NvcrCost",
        "NvcrCostCurrency",
        "NvcrTaxIncluded",
        "NvcrIncluded1",
        "NvcrTAXNotIncluded",
        "NvcrNotIncluded1",
        "nvcrTAX$Included",
        "NvcrCurrencyIncluded",
        "NvcrIncluded2",
        "NvcrTAX$NotIncluded",
        "NvcrCurrencyNotIncluded",
        "nvcrNotincluded2",
        "nvcrRoomChar",
        "dtmCrawlDateTime",
        "nvcrYieldManager",
        "nvcrContractManager",
        "nvcrDemandGroup",
        "nvcrSegmentation",
        "nvcrHotelContractingType",
        "nvcrTPS",
        "nvcrHotelStatus",
        "nvcrHotelChain",
    ]
    DB_INSERT_QUERY_TEMPLATE = "INSERT INTO `eCube_Centralized_DB`.`BatchCrawlData`(%s)VALUES(%s);"

    def __init__(self, result_data):
        host, user, password, db_name = reporting_config.get_pymysql_args
        super().__init__(host, user, password, db_name)
        self._data = result_data
        self.request_id = self._data['RID_RequestId']
        self.report_run_id = self._data['ReportRunId']
        self.request_run_id = self._data['RID_RequestRunId']

    def _db_insert_bulk(self, lines):
        raise NotImplementedError

    @property
    def _query_column_list(self):
        return ["`%s`" % field for field in self.REPORT_FIELDS]

    @staticmethod
    def _query_field_list(line):
        field_list = list()
        for i, field in enumerate(line):
            # print("i")
            # print(i)
            if i == 38:
                value = field
            elif field == {}:
                value = None
            elif field != 'Null':
                if isinstance(field, str):
                    value = field.encode('utf-8')
                else:
                    value = field
            else:
                value = None
            field_list.append(value)
        return field_list

    def _db_insert_line(self, line):
        insert_query = self.DB_INSERT_QUERY_TEMPLATE % (
            ",".join(self._query_column_list),
            ",".join(['%s' for i in self._query_field_list(line)]),
        )
        # print("insert_query")
        # print(insert_query)
        cur = self._cursor
        # from pdb import set_trace; set_trace()
        cur.execute(insert_query, self._query_field_list(line))
        self._db.commit()
        cur.close()
        # self.update_query(insert_query)

    def _call_hotel_addition(self):
        HotelAdditionCache(self.request_run_id).mark_queued()

    def process_report(self):
        print("process_report")
        report_lines = self.REPORT_CACHE.get_lines(self.request_id)
        print("len(report_lines)")
        print(len(report_lines))
        if self.BULK_INSERT:
            self._db_insert_bulk(report_lines)
        else:
            for line in report_lines:
                self._db_insert_line(line)
        self._call_hotel_addition()
        print("hotel addition queued")
        self.clean_connections()
        if report_lines:
            return 'Completed'
