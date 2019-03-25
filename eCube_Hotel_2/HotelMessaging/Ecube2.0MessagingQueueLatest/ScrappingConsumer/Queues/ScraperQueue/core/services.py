import json
import copy
import requests
from Queues.ScraperQueue.resources.db_connectors import MongoBaseHandler
from Queues.ScraperQueue.core.utils import get_nohodo_proxy, get_user_agent, hotel_data_save_checker


class ProxyCaller(object):

    @classmethod
    def get_proxy_url(cls):
        # return '192.168.7.128'
        return '192.168.8.34'

    @classmethod    
    def get_port(cls):
        # return '8005'
        return '8001'


class API(object):

    PROXYDETAILS = {
        'url': ProxyCaller.get_proxy_url(),
        'port': ProxyCaller.get_port(),
    }

    @classmethod
    def GetProxy(cls, domain, country):
        # return get_nohodo_proxy(domain, country)
        domain = 'Travel'
        url = "http://{0}:{1}/api/v1/getProxy?domain={2}&country=".format(cls.PROXYDETAILS['url'],
                                                                cls.PROXYDETAILS['port'], domain)
        # from pdb import set_trace; set_trace()
        response = requests.get(url).json()
        response.update({'proxyCountry': 'UK'})
        response.update({'port': str(response['port'])})
        return response

    @classmethod
    def SaveProxyDetails(cls, domain, server, port, username, reason, country, region, code):
        domain = 'Travel'
        url = "http://{0}:{1}/api/v1/proxy?Domain={2}&Proxyserver={3}&ProxyPort={4}&proxyusername={5}&ProxyStatus={6}&ProxyCountry={7}&proxyRegion={8}&ProxyType={9}&BlockReason={10}"
        url = url.format(cls.PROXYDETAILS['url'], cls.PROXYDETAILS['port'], domain, server, port, username, reason, country, region, code, reason)
        response = requests.get(url)
        return response.text

    @classmethod
    def GetUserAgent(cls, domain):
        return get_user_agent(domain)

    @classmethod
    def GetMatchingHotel(cls, country, city):
        url = "http://192.168.4.217/DipbagCrawler/MatchingDll.aspx?strCountry={0}&strState=&strCity={1}&strPSupplier=&strSSupplier=TravelRepublic&strProject=Hotelbeds".format(
            country.upper(), city.upper())
        # updated url here

        hotel_data = requests.get(url)
        return hotel_data.text

    @classmethod
    def GetCityMatchingZone(cls):
        url = "https://192.168.4.217/hotelbeds/GTA_Destination_mapping.html"
        # updated url here

        city_data = requests.get(url)
        return city_data.text

    @classmethod
    def SaveHtml(cls, hotel_data):
        return hotel_data_save_checker(hotel_data)

    @classmethod
    def GetPartialHotels(cls, sub_request_id):
        return PartialHotelHandler(sub_request_id).get_hotels()

    @classmethod
    def SavePartialHotels(cls, partial_data, error):
        PartialHotelHandler(partial_data['subRequestId']).save_hotels(partial_data, error)


class MongoHandler(MongoBaseHandler):

    DB_NAME = 'HTMLDumps'

    @staticmethod
    def _get_individual_hotels(crawled_data):
        insert_list = list()
        master_data_copy = copy.deepcopy(crawled_data)
        hotels = master_data_copy.pop('hotels')
        for hotel in hotels:
            insert_data = master_data_copy.copy()
            insert_data['hotel'] = hotel
            insert_list.append(insert_data)
        return insert_list

    def save_successful_crawl(self, crawled_data):
        collection = self.get_collection('HTMLRepository')
        insert_list = self._get_individual_hotels(crawled_data)

        # from pdb import set_trace; set_trace()
        for insert_data in insert_list:
            collection.insert(insert_data)

    def save_pnf(self, pnf_data, error):
        collection = self.get_collection('PNFData')
        insert_data = copy.deepcopy(pnf_data)
        insert_data.update({'error_msg': error})
        collection.insert(insert_data)


# '''
class PartialHotelHandler(MongoBaseHandler):

    DB_NAME = 'PartialHotelsDump'
    STATUS = ['running', 'completed', 'timeout']

    @staticmethod
    def _get_individual_hotels(crawled_data):
        insert_list = list()
        master_data_copy = copy.deepcopy(crawled_data)
        hotels = master_data_copy.pop('hotels')
        for hotel in hotels:
            insert_data = master_data_copy.copy()
            insert_data['hotel'] = hotel
            insert_list.append(insert_data)
        return insert_list

    @staticmethod
    def _get_collated_hotels(mongo_datas):
        return [copy.deepcopy(hotel_data['hotel']) for hotel_data in mongo_datas]

    def __init__(self, sub_request_id):
        self.sub_req = sub_request_id
        self.status = None

    def make_query(self, custom_query=None):
        if not custom_query:
            custom_query = dict()
        if not isinstance(custom_query, dict):
            raise ValueError('custom_query should be dict')

        query = {'subRequestId': self.sub_req}
        query.update(custom_query.copy())
        return query

    @classmethod
    def _read_single_doc(cls, docs):
        for doc in docs:
            return doc

    def _mark_sub_req(self, status):
        self.clear_status()
        print('marking status "%s" for SRID:%s' % (status, self.sub_req))
        status_data = {'subRequestId': self.sub_req, 'status': status}
        collection = self.get_collection('StatusRepository')
        collection.insert(status_data.copy())

    def mark_sub_req_running(self):
        self._mark_sub_req('running')

    def mark_sub_req_timeout(self):
        self._mark_sub_req('timeout')

    def mark_sub_req_completed(self):
        self._mark_sub_req('completed')

    def _get_sub_req_status(self, refresh=True):
        if refresh or not self.status:
            print('get status for SRID:%s' % self.sub_req)
            collection = self.get_collection('StatusRepository')
            doc = self._read_single_doc(collection.find(self.make_query()))
            if doc:
                print('status found "%s" for SRID:%s' % (doc['status'], self.sub_req))
                self.status = doc['status']
        return self.status

    def _check_sub_req_status(self, status):
        print('checking status "%s" for SRID:%s' % (status, self.sub_req))
        return status == self._get_sub_req_status(refresh=False)

    def check_sub_req_running(self):
        return self._check_sub_req_status('running')

    def check_sub_req_timeout(self):
        return self._check_sub_req_status('timeout')

    def check_sub_req_completed(self):
        return self._check_sub_req_status('completed')

    def clear_status(self):
        print('clearing status for SRID:%s' % self.sub_req)
        collection = self.get_collection('StatusRepository')
        collection.remove(self.make_query())

    def get_hotels(self):
        print('getting partial hotels')
        collection = self.get_collection('HTMLRepository')
        docs = collection.find(self.make_query())
        return self._get_collated_hotels(docs)

    def save_hotels(self, partial_data, error):
        print('saving partial hotels')
        partial_data.update({'error': error})
        collection = self.get_collection('HTMLRepository')
        collection.remove(self.make_query())

        insert_list = self._get_individual_hotels(partial_data)

        for insert_data in insert_list:
            insert_data.update({'error_msg': error})
            collection.insert(insert_data)
# '''


MongoHandler.set_mongo_url()
PartialHotelHandler.set_mongo_url()
