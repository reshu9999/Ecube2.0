import json
import time
import datetime
import requests

from lxml import html
from selenium import webdriver
from Queues.ScraperQueue.core import services, exceptions
# from core import services, exceptions


class CrawlerBase(object):
    TRL = None
    CONFIG_FILE = None


class RequestHandler(CrawlerBase):
    OPTIONS = webdriver.ChromeOptions()
    EXECUTABLE_PATH = '/home/ironeagle/Code/eCube_Hotel_2/HotelMessaging/Ecube2.0MessagingQueueLatest/ScrappingConsumer/Queues/ScraperQueue/core/chromedriver'
    DRIVER_CLASS = webdriver.Chrome

    EXCEPTIONS = {
        'INCORRECT_REQUEST_TYPE': exceptions.IncorrectRequestType,
        'MISSING_REQUEST_TYPE': exceptions.MissingRequestType,
        'MISSING_VISIT_HOMEPAGE': exceptions.MissingVisitHomePage,
    }

    @classmethod
    def _get_request_type(cls):
        if not hasattr(cls.CONFIG_FILE, 'requestType'):
            raise cls.EXCEPTIONS['MISSING_REQUEST_TYPE']
        return cls.CONFIG_FILE.requestType

    @classmethod
    def _get_visit_homepage(cls):
        if not hasattr(cls.CONFIG_FILE, 'visitHomePage'):
            raise cls.EXCEPTIONS['MISSING_VISIT_HOMEPAGE']
        return cls.CONFIG_FILE.visitHomePage

    # TODO: aetos: add option driver or request rather than taking from config
    @classmethod
    def get_request(cls, url, headers, proxy, cookie=None, timeout=10, driver=False):
        """
        :param url:
        :param headers:
        :param proxy:
        :param cookie:
        :param timeout:
        :return: response html and response object
        """
        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, proxy=proxy, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, proxy=proxy, headers=headers)
        driver_obj = None

        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver
        elif request_type['driver'] and not driver:
            pass
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        if request_type['request']:
            if cookie:
                response = requests.get(url, headers=headers, proxies=proxy.to_python('http'), timeout=timeout, cookies=cookie)
            else:
                response = requests.get(url, headers=headers, proxies=proxy.to_python('http'), timeout=timeout)

            res_html = response.text
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj

    @classmethod
    def post_request(cls, url, headers, proxy, body, body_type='url_string', cookie=None, timeout=10, driver=False):
        """
        :param url:
        :param headers:
        :param proxy:
        :param body: Post body
        :param body_type: url_string or json
        :param cookie:
        :param timeout:
        :return: response html and response object
        """
        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, proxy=proxy, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, proxy=proxy, headers=headers)
        driver_obj = None
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver
        elif request_type['driver'] and not driver:
            pass
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        if request_type['request']:
            param_dict = {
                'url': url,
                'data': json.dumps(body) if body_type == 'json' else body,
                'headers': headers,
                'proxies': proxy.to_python('http'),
                'timeout': timeout,
            }
            if cookie:
                param_dict['cookies']=cookie

            response = requests.post(**param_dict)

            res_html = response.text
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj


class ProxyHandler(RequestHandler):

    RETRY_COUNT = 3
    EXCEPTIONS = {
        'MISSING_GET_PROXY_PARAMS': exceptions.GetProxyParamsMissing,
        'PROTOCOL_NOT_ALLOWED': exceptions.ProxyProtocolNotAllowed,
        'MISSING_KEY_TO_SET_PROXY': exceptions.ProxySetParamsMissing,

        'NOT_FOUND': exceptions.ProxyNotFound,
        'NOT_WORKING': exceptions.ProxyNotWorking,

        'SERVER_ERROR': exceptions.ProxyGivingServerError,
        'SERVER_DOWN_ERROR': exceptions.ProxyGivingServerError,
        'PNF_ERROR': exceptions.ProxyGivingPNF,
        'REQUEST_ERROR': exceptions.ProxyGivingAuthError,
        'PROXY_AUTH_ERROR': exceptions.ProxyNotAuthError,
    }
    SERVICE_CALLS = {
        'get_proxy': services.API.GetProxy,
        'save_proxy': services.API.SaveProxyDetails
    }

    ALLOWED_PROTOCOLS = ['http', 'https']

    def __init__(self):
        self.tries_left = self.RETRY_COUNT
        self.domain = None
        self.response = None
        self.request_url = None
        self.country = None
        self.server = None
        self.port = None
        self.username = None
        self.password = None
        self._status = None
        self._error = None
        self.is_preview = None

    def _set_proxy(self, data_dict):
        # data_dict = {
        #     'IP': 'london.wonderproxy.com',
        #     'UserName': 'sachin',
        #     'Password': 'sachin@123',
        #     'port': '80',
        #     'proxyCountry': 'london',
        # }
        # data_dict = {
        #     'IP': 'shp-prx117-at-v00001.tp-ns.com',
        #     'UserName': 'prx117',
        #     'Password': 'GNP7zFHc)A',
        #     'port': '80',
        #     'proxyCountry': 'london',
        # }
        # data_dict = {
        #     'IP': 'shp-prx117-au-v00001.tp-ns.com',
        #     'UserName': 'prx117',
        #     'Password': 'GNP7zFHc)A',
        #     'port': '80',
        #     'proxyCountry': 'AU',
        # }
        # required_keys = ['domainName', 'proxyCountry', 'proxyAddress', 'proxyPort', 'proxyUsername', 'Password']
        required_keys = ['UserName', 'IP', 'Password', 'port']

        for key in required_keys:
            if key not in data_dict:
                self.TRL.error_log('Missing Key:%s in %s' % (key, data_dict))
                raise self.EXCEPTIONS['MISSING_KEY_TO_SET_PROXY'](
                    '"%s" key missing from Get Proxy Response "%s"' % (key, data_dict))

        # Meta Data
        self.domain = data_dict['IP']
        # self.domain = 'www.starwood.com'
        self.country = data_dict['proxyCountry']
        # self.country = 'Spain'
        # Properties for Proxy
        self.server = data_dict['IP']
        # self.server = "69.39.224.131"
        self.port = data_dict['port']
        # self.port = "80"
        self.address = self.server + ':' + self.port
        self.username = data_dict['UserName']
        self.password = data_dict['Password']
        self.TRL.debug_log('Proxy:%s Set' % self.address, proxy=self)

    def _update_status(self, reason, region='Europe', code='1'):
        self.SERVICE_CALLS['save_proxy'](
            self.domain, self.server, self.port, self.username, reason, self.country, region, code)
        self.TRL.debug_log('Updating Proxy:%s' % reason, proxy=self)

    @classmethod
    def _check_response_code(cls, response):
        cls.TRL.debug_log('Status Code:%s' % response.status_code)
        if 500 <= response.status_code < 600:
            if response.status_code == 503:
                cls.TRL.debug_log('Server Down')
                raise cls.EXCEPTIONS['SERVER_DOWN_ERROR']
            cls.TRL.debug_log('Server Error')
            raise cls.EXCEPTIONS['SERVER_ERROR']

        if 400 <= response.status_code < 500:
            if response.status_code == 404:
                cls.TRL.debug_log('Page Not Found')
                raise cls.EXCEPTIONS['PNF_ERROR']
            if response.status_code == 407:
                cls.TRL.debug_log('Proxy Not Authorised')
                raise cls.EXCEPTIONS['PROXY_AUTH_ERROR']
            cls.TRL.debug_log('Proxy Giving Not Authorised Error')
            raise cls.EXCEPTIONS['REQUEST_ERROR']

    def update_status_blocked(self):
        self._update_status('Blocked')

    def update_status_unblocked(self):
        self._update_status('UnBlocked')

    def initiate_new_proxy(self, domain=None, country=None):
        domain = domain or self.domain
        country = country or self.country
        self.TRL.debug_log('Initiating Proxy for D:%s and C:%s' % (domain, country))
        if not domain:
            self.TRL.debug_log('Missing Param D:%s and C:%s' % (not bool(domain), not bool(country)))
            raise self.EXCEPTIONS['MISSING_GET_PROXY_PARAMS']

        self._set_proxy(self.SERVICE_CALLS['get_proxy'](domain, country))

    def check_proxy(self, url, headers):
        self.TRL.debug_log('Proxy Check Tries:%s' % self.tries_left, proxy=self, headers=headers)
        if not self.tries_left:
            self.TRL.debug_log('Proxy Not Working', proxy=self, headers=headers)
            raise self.EXCEPTIONS['NOT_WORKING']

        try:
            _, response, _ = self.get_request(url, headers, self, timeout=10)
            self._check_response_code(response)
            self.TRL.debug_log('Got Working Proxy', proxy=self, headers=headers)
            self.update_status_unblocked()
            return True
        except self.EXCEPTIONS['SERVER_DOWN_ERROR'] as e:
            time.sleep(5)
        except Exception as e:
            pass

        self.tries_left -= 1

        self.update_status_blocked()

        self.initiate_new_proxy()
        return self.check_proxy(url, headers)

    # TODO: aetos: make both http and https
    def to_python(self, protocol):
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise self.EXCEPTIONS['PROTOCOL_NOT_ALLOWED']
        return {
            "http": 'http://' + self.username + ':' + self.password + '@' + self.address,
            "https": 'https://' + self.username + ':' + self.password + '@' + self.address,
        }

    def to_driver(self, protocol):
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise self.EXCEPTIONS['PROTOCOL_NOT_ALLOWED']
        return self.address

    def to_log(self, protocol):
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise self.EXCEPTIONS['PROTOCOL_NOT_ALLOWED']
        return self.address


class HotelLandingPageHandler(RequestHandler):

    HOST = None
    HOTEL_HANDLER_CLASS = None
    RETRY_COUNT = 3
    EXCEPTIONS = {
        'INVALID_URL': exceptions.InvalidURL,
        'LAT_LONG_ERROR': exceptions.LatLongNotFountError,
        'SCRIPT_PNF': exceptions.ScriptPNF,
    }
    SERVICE_CALLS = {
        'get_user_agent': services.API.GetUserAgent,
        'get_matching_hotel': services.API.GetMatchingHotel,
        'get_city_zone': services.API.GetCityMatchingZone,
        'get_partial_hotels': services.API.GetPartialHotels,
        'save_partial_hotels': services.API.SavePartialHotels,
    }

    def __init__(self, request_data):

        # Meta Data
        self.request_id = request_data['requestId']
        self.sub_request_id = request_data['subRequestId']
        self.request_run_id = request_data['requestRunId']
        self.request_data = request_data.copy()
        self.TRL.debug_log('INIT Crawling', self.request_id, self.sub_request_id, self.request_run_id)

        # Properties for Hotel List
        self.domain = self._clean_host_url
        self.country = request_data['country']
        self.city = request_data['RequestInputs']['city']
        self.children = request_data['RequestInputs']['children']
        self.adults = request_data['RequestInputs']['adults']

        self.hotel_name = request_data['RequestInputs']['hotelName']
        self.room = request_data['RequestInputs']['room']
        self.board = request_data['RequestInputs']['board']
        self.rating = request_data['RequestInputs']['starRating']
        self.hotel_web_id = request_data['RequestInputs']['webSiteHotelId']
        self.pos = request_data['RequestInputs']['pos']

        self.check_in = request_data['RequestInputs']['checkIn']
        self.check_out = request_data['RequestInputs']['checkOut']
        self.nights = request_data['RequestInputs']['nights']
        self.days = request_data['RequestInputs'].get('days', 0)
        self.start_time = datetime.datetime.now()
        self._html = None
        self.hotel_count = 0

        # manage_hotel_ids
        self.hotels_id_dict = None
        self.match_hotel_list = None

        # Properties for Making Request
        self.cookie = None
        self.user_agent = self.SERVICE_CALLS['get_user_agent'](self.domain)
        self.TRL.debug_log('User Agent:%s' % self.user_agent, self.request_id, self.sub_request_id, self.request_run_id)
        # self.headers = {
        #     'User-Agent': self.user_agent.strip()
        # }
        # TODO: aetos: add a function which sets headers and make it NonImplemented
        # self.headers = {
        #     'Host': self.HOST,
        #     'Connection': 'keep-alive',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng*/*;q=0.8',
        #     'User-Agent': self.user_agent.strip()
        # }
        self.headers = self._get_headers
        # self.headers = self._get_headers()
        self.TRL.debug_log('Headers:%s' % self.headers, self.request_id, self.sub_request_id, self.request_run_id)
        proxy = ProxyHandler()
        proxy.initiate_new_proxy(self.domain, self.country)
        self.proxy = proxy

    @property
    def _clean_host_url(self):
        url = self.HOST
        if url.endswith('/'):
            url = url[:-1]
        return url

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        raise NotImplementedError

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        raise NotImplementedError

    @property
    def _get_url_params(self):
        """
        :return: dict of key value to be added in URL
        """
        raise NotImplementedError

    @property
    def _get_currency(self):
        """
        :return: currency name as string
        """
        return "USD"

    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        raise NotImplementedError

    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        raise NotImplementedError

    def _set_headers(self, headers):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        raise NotImplementedError

    def _process_homepage(self):
        raise NotImplementedError

    def _get_host_url_for_url_maker(self):
        return self._clean_host_url

    def _url_maker(self):
        self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id, self.request_run_id)
        self.TRL.debug_log('Params:%s' % self._get_url_params, self.request_id, self.sub_request_id, self.request_run_id)

        return "".join([self._clean_host_url + '/preferredguest/search/results/detail.html?'] + ['&%s=%s' % (i, p) for i, p in
                                                                                      self._get_url_params.items()])

    def _get_hotel_list(self, url=None):
        if not url:
            link = self._url_maker()
        elif isinstance(url, str):
            link = url
        elif callable(url):
            link = url(self)
        else:
            self.TRL.error_log('Invalid URL to get Hotel List', self.request_id, self.sub_request_id, self.request_run_id)
            raise self.EXCEPTIONS['INVALID_URL']

        try:
            self.proxy.check_proxy(link, self.headers)

        except (
            ProxyHandler.EXCEPTIONS['SERVER_DOWN_ERROR'],
            ProxyHandler.EXCEPTIONS['SERVER_ERROR'],
            ProxyHandler.EXCEPTIONS['PNF_ERROR'],
            ProxyHandler.EXCEPTIONS['PROXY_AUTH_ERROR'],
            ProxyHandler.EXCEPTIONS['REQUEST_ERROR']
        ) as e:
            self.TRL.error_log(
                'No Working Proxy Found:%s' % str(e), self.request_id, self.sub_request_id, self.request_run_id,
                headers=self.headers)
            raise ProxyHandler.EXCEPTIONS['NOT_WORKING']

        resp, resp_obj, _ = self.get_request(link, self.headers, self.proxy, driver=False)

        self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
        request_type = RequestHandler._get_request_type()
        if request_type['driver']:
            self._set_cookie(_)
        else:
            self._set_cookie(resp_obj)

        self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return resp

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = html.fromstring(self._get_hotel_list())

    def _set_hotel_web_id(self, hotel_url):
        """
        Set hotel web_id if not set
        :param: hotel url
        :return: None
        """
        raise NotImplementedError

    def _save_hotel(self, index, hotel_url):
        try:
            latitude_url = self._lat_long_links[self._hotels.index(str(hotel_url))]
        except exceptions.LatLongNotFountError:
            self.TRL.debug_log('Latitude and Longitude not found in URL', self.request_id, self.sub_request_id, self.request_run_id)
            latitude_url = None

        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url, self.request_id, self.sub_request_id, self.request_run_id)

        if self.hotels_id_dict is not None:
            self._set_hotel_web_id(self.hotels_id_dict[index])

        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(hotel_url, latitude_url, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        hotel_data = hotel.save_html(index)
        return hotel_data

    def crawl_hotels(self, redelivered):
        # redelivered = False
        partial_hotels = list()
        if redelivered:
            partial_hotels = self.SERVICE_CALLS['get_partial_hotels'](self.sub_request_id)
            print('crawled_hotels found')
            print(len(partial_hotels))
            # from pdb import set_trace; set_trace()

        self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
        try:
            self._set_html()
        except Exception as e:
            self.request_data.update({'hotels': list()})
            self.SERVICE_CALLS['save_partial_hotels'](self.request_data, str(e))
            raise self.EXCEPTIONS['SCRIPT_PNF']

        self.TRL.debug_log('Hotels Found:%s' % len(self._hotels), self.request_id, self.sub_request_id, self.request_run_id)
        crawled_hotels = partial_hotels
        hotels_count = len(crawled_hotels)
        # crawled_hotels = [self._save_hotel(i, hotel_url) for i, hotel_url in enumerate(self._hotels[:1])]
        for i, hotel_url in enumerate(self._hotels[hotels_count:5]):
            i += hotels_count
            try:
                # if i == 3:
                #     raise Exception('Aetos Exception at "%s"' % i)
                hotel = self._save_hotel(i, hotel_url)
                crawled_hotels.append(hotel)
            except Exception as e:
                self.request_data.update({'hotels': crawled_hotels})
                self.SERVICE_CALLS['save_partial_hotels'](self.request_data, str(e))
                raise self.EXCEPTIONS['SCRIPT_PNF']
        self.request_data.update({'hotels': crawled_hotels})
        return self.request_data


class HotelHandler(RequestHandler):

    SERVICE_CALLS = {
        'save_html': services.API.SaveHtml
    }

    def __init__(self, landing_page, hotel_html):

        # Properties for Hotel
        self._landing_page = landing_page
        self._html = hotel_html
        self.country = landing_page.country
        self.city = landing_page.city
        self.start_time = landing_page.start_time
        self.check_in = landing_page.check_in
        self.check_out = landing_page.check_out
        self.hotel_count = landing_page.hotel_count

        # Properties for Making Request
        self.proxy = landing_page.proxy
        self.headers = landing_page.headers
        self.cookie = landing_page.cookie

    @property
    def _get_name(self):
        # hotelNameXpath
        raise NotImplementedError

    @property
    def _get_city_zone(self):
        return self.city.upper()

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        raise NotImplementedError

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """
        raise NotImplementedError

    def save_html(self, index):
        hotel_data = dict()
        meta_data = dict()

        # Properties from Parent
        hotel_data['index'] = index
        hotel_data['hotel_count'] = self.hotel_count
        hotel_data['city'] = self.city
        hotel_data['country'] = self.country
        hotel_data['city_zone'] = self._get_city_zone
        hotel_data['checkIn'] = str(self.check_in)
        hotel_data['checkOut'] = str(self.check_out)

        # Crawler Output
        hotel_data['htmls'] = self._get_html
        hotel_data['hotelName'] = self._get_name
        hotel_data['roomTypes'] = self._get_room_types
        hotel_data['hotel_id'] = self._landing_page.hotel_web_id

        # Meta Data
        meta_data['requestId'] = self._landing_page.request_id
        meta_data['subRequestId'] = self._landing_page.sub_request_id
        meta_data['requestRunId'] = self._landing_page.request_run_id
        meta_data['startDT'] = str(self.start_time)
        meta_data['endDT'] = str(datetime.datetime.now())
        hotel_data['meta'] = meta_data

        self.TRL.debug_log(
            'Saving Hotel:%s' % self._get_name, self._landing_page.request_id, self._landing_page.sub_request_id,
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers)
        return self.SERVICE_CALLS['save_html'](hotel_data)

    @classmethod
    def complete_hotel_url(cls, hotel_url, domain):
        if str(hotel_url).split('/')[2] != domain:
            hotel_url = domain + hotel_url
        return hotel_url

    @classmethod
    def get_hotel(cls, hotel_url, latitude_url, landing_page):
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers)

        hotel_url = cls.complete_hotel_url(hotel_url, landing_page.domain)

        resp_html, response, _ = cls.get_request(hotel_url, headers, proxy, cookie=cookie)
        html_elem = {'html_element': resp_html, 'latitude_html': cls._get_latitude(latitude_url, proxy, headers, cookie=cookie)}
        return cls(landing_page, html_elem)

    @classmethod
    def _get_latitude(cls, latitude_url, proxy, headers, cookie):
        if latitude_url is not None:
            resp_html, response, _ = cls.get_request(latitude_url, headers, proxy, cookie=cookie)
        else:
            resp_html = 'Latitude URL not present'
        return {'html_element': resp_html}
