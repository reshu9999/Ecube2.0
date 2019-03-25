from queues.connections import RedisConnection


def read_from_source(deep_keys, data_source):
    res = data_source
    for key in deep_keys:
        res = res.get(key, dict())
    return res


class MultiLines(Exception):
    pass


class IncorrectReparseType(Exception):
    pass


class ReportingCacheMapper(object):

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

    def __init__(self, data_key, db_key, default=None):
        self.data_key = data_key
        self.db_key = db_key
        self.index = self.get_index
        self.default = default or 'Null'
        self.keys = data_key.split('.')
        self.is_multi = '[]' in self.data_key

    @classmethod
    def get_index_for_key(cls, db_key):
        return cls.REPORT_FIELDS.index(db_key)

    @property
    def get_index(self):
        return self.get_index_for_key(self.db_key)

    @property
    def get_family(self):
        key_parts = self.data_key.split('.')
        parent = key_parts[0].replace('[]', '')
        child = ".".join(key_parts[1:])

        return parent, child

    def get_value(self, data_source):
        if self.is_multi:
            raise MultiLines

        return self.index, read_from_source(self.keys, data_source) or self.default


class ReportingCacheHandler(object):
    COL_LEN = 78
    INSTANCE_PARAMS = [
        ReportingCacheMapper('hotelName', 'nvcrHotelName', ''),
        ReportingCacheMapper('website_id', 'nvcrCompetitorHotelID', ''),
        ReportingCacheMapper('address', 'nvcrHotelLocation', ''),
        ReportingCacheMapper('starRating', 'nvcrHotelStar', ''),
        ReportingCacheMapper('supplier', 'strSupplier', ''),
        ReportingCacheMapper('adult', 'intAdult', '0'),
        ReportingCacheMapper('index', 'nvcrHotelCount', '0'),
        ReportingCacheMapper('total_hotel', 'nvcrTotalHotel', '0'),
        ReportingCacheMapper('longitude', 'nvcrLongitude', '0'),
        ReportingCacheMapper('latitude', 'nvcrLatitude', '0'),
        ReportingCacheMapper('city_zone', 'nvcrMultipleZoneCheck', '0'),
        ReportingCacheMapper('room_types[].type', 'nvcrRoomType', ''),
        ReportingCacheMapper('room_types[].price', 'mnyRate', '0'),
        ReportingCacheMapper('room_types[].board_code', 'nvcrBoard', '0'),
        ReportingCacheMapper('room_types[].currency', 'nvcrCurrency', '0'),
        ReportingCacheMapper('room_types[].daily_price', 'nvcrDailyRate', '0'),
        ReportingCacheMapper('room_types[].paymentOption', 'nvcrDirectPayment', '0'),
    ]
    META_PARAMS = [
        ReportingCacheMapper('cachePageURL', 'nvcrPagePath', ''),
        ReportingCacheMapper('startDT', 'dtmCrawlDateTime', ''),
    ]
    INPUT_PARAMS = [
        ReportingCacheMapper('requestRunId', 'intDiPBagDynamicId', ''),
        ReportingCacheMapper('subRequestId', 'intSubDipbagDynamicId', ''),
        ReportingCacheMapper('RequestInputs.country', 'nvcrHotelAddress', ''),
        ReportingCacheMapper('RequestInputs.city', 'nvcrCity', ''),
        ReportingCacheMapper('RequestInputs.checkIn', 'sdtmCheckinDate', ''),
        ReportingCacheMapper('RequestInputs.checkOut', 'sdtmCheckoutDate', ''),
        ReportingCacheMapper('RequestInputs.competitorId', 'intSupplierId', ''),
        ReportingCacheMapper('RequestInputs.pos', 'nvcrCancellationPolicy', ''),
    ]
    CACHE_CONNECTION = RedisConnection
    HASH_TEMPLATE = 'rid:%s_rrid:%s_srid:%s_hid:%s'

    def __init__(self, hid, data, input_data):
        # from pdb import set_trace; set_trace()
        self.CACHE_CONNECTION.NAMESPACE = 'hotel_report_lines'
        self.hotel_index = hid + 1
        self._instance = data.copy()
        self._meta_data = data['meta'].copy()
        self._input_data = input_data.copy()

        self.req_id = self._input_data['requestId']
        self.req_run_id = self._input_data['requestRunId']
        self.sub_req_id = self._input_data['subRequestId']
        self.cache_data = self._empty_list
        self.cache_hash = self.HASH_TEMPLATE % (self.req_id, self.req_run_id, self.sub_req_id, self.hotel_index)
        self.multi_line_keys = dict()

    @property
    def _empty_list(self):
        return [None for i in range(0, len(ReportingCacheMapper.REPORT_FIELDS))]

    @classmethod
    def _get_value(cls, deep_key, data_source):
        return deep_key.get_value(data_source)

    def _add_custom_values(self):
        self.cache_data[ReportingCacheMapper.get_index_for_key('intSiteID')] = 1
        self.cache_data[ReportingCacheMapper.get_index_for_key('bitReCrawl')] = 0
        self.cache_data[ReportingCacheMapper.get_index_for_key('sintBatchCrawlStatus')] = 3
        self.cache_data[ReportingCacheMapper.get_index_for_key('nvcrCrawlDescription')] = 'Completed'
        # if self._input_data['DomainName'] == 'Global Market H1':
        #     self.cache_data[27] = self._instance['website_id']
        #     self.cache_data[51] = 'Null'
        for i, cd in enumerate(self.cache_data):
            if cd is None:
                self.cache_data[i] = 'Null'
        return self.cache_data

    def _make_multi_line_data(self):
        cache_data_master = self.cache_data.copy()
        self.cache_data = list()
        for parent, child_params in self.multi_line_keys.items():
            child_data_sources = self._instance[parent]
            for child_data_source in child_data_sources:
                child_cache_data_master = cache_data_master.copy()
                for param in child_params:
                    _, child = param.get_family
                    child_cache_data_master[param.index] = read_from_source(child.split('.'), child_data_source)
                self.cache_data.append(child_cache_data_master)

    def _prepare_cache_data(self, param, data_source):
        try:
            index, value = self._get_value(param, data_source)
            self.cache_data[index] = value
        except MultiLines:
            parent, child = param.get_family
            if parent in self.multi_line_keys:
                self.multi_line_keys[parent].append(param)
            else:
                self.multi_line_keys.update({parent: [param]})

    def make_entry(self):
        for param in self.INSTANCE_PARAMS:
            self._prepare_cache_data(param, self._instance)
        for param in self.META_PARAMS:
            self._prepare_cache_data(param, self._meta_data)
        for param in self.INPUT_PARAMS:
            self._prepare_cache_data(param, self._input_data)

        self._add_custom_values()
        self._make_multi_line_data()
        print('self.CACHE_CONNECTION.set_key(self.cache_hash, self.cache_data)')
        print(self.cache_hash, self.cache_data)
        # from pdb import set_trace; set_trace()

        self.CACHE_CONNECTION.set_key(self.cache_hash, self.cache_data)
