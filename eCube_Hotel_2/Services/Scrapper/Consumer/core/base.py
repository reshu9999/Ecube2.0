import time
import datetime
import requests
from core import services, exceptions

from lxml import html
from selenium import webdriver


class CrawlerBase(object):
    TRL = None
    CONFIG_FILE = None


class RequestHandler(CrawlerBase):
    OPTIONS = webdriver.ChromeOptions()
    EXECUTABLE_PATH = 'chromedriver.exe'
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

    @classmethod
    def get_request(cls, url, headers, proxy, cookie=None, timeout=10):
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

        if request_type == 'driver':
            options = cls.OPTIONS
            options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            return driver.page_source, driver

        elif request_type == 'request':
            response = requests.get(url, headers=headers, proxies=proxy.to_python('http'), timeout=timeout)
            return response.text, response

        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']


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
        required_keys = ['domainName', 'proxyCountry', 'proxyAddress', 'proxyPort', 'proxyUsername', 'Password']

        for key in required_keys:
            if key not in data_dict:
                self.TRL.error_log('Missing Key:%s in %s' % (key, data_dict))
                raise self.EXCEPTIONS['MISSING_KEY_TO_SET_PROXY'](
                    '"%s" key missing from Get Proxy Response "%s"' % (key, data_dict))

        # Meta Data
        self.domain = data_dict['domainName']
        self.country = data_dict['proxyCountry']

        # Properties for Proxy
        self.server = data_dict['proxyAddress']
        self.port = data_dict['proxyPort']
        self.address = self.server + ':' + self.port
        self.username = data_dict['proxyUsername']
        self.password = data_dict['Password']
        self.TRL.debug_log('Proxy:%s Set' % self.address, proxy=self)

    def _update_status(self, reason, region='Europe', code='1'):
        self.SERVICE_CALLS['save_proxy'](
            self.domain, self.server, self.port, self.username, reason, self.country, region, code)
        self.TRL.debug_log('Updating Proxy:%s' % reason, proxy=self)

    @classmethod
    def _check_response_code(cls, response):
        cls.TRL.debug_log('Status Code:%s' % response.status_code)
        if 500 >= response.status_code < 600:
            if response.status_code == 503:
                cls.TRL.error_log('Server Down')
                raise cls.EXCEPTIONS['SERVER_DOWN_ERROR']
            cls.TRL.error_log('Server Error')
            raise cls.EXCEPTIONS['SERVER_ERROR']

        if 400 >= response.status_code < 500:
            if response.status_code == 404:
                cls.TRL.error_log('Page Not Found')
                raise cls.EXCEPTIONS['PNF_ERROR']
            if response.status_code == 407:
                cls.TRL.error_log('Proxy Not Authorised')
                raise cls.EXCEPTIONS['PROXY_AUTH_ERROR']
            cls.TRL.error_log('Proxy Giving Not Authorised Error')
            raise cls.EXCEPTIONS['REQUEST_ERROR']

    def update_status_blocked(self):
        self._update_status('Blocked')

    def update_status_unblocked(self):
        self._update_status('UnBlocked')

    def initiate_new_proxy(self, domain=None, country=None):
        domain = domain or self.domain
        country = country or self.country
        self.TRL.debug_log('Initiating Proxy for C:%s and D:%s' % (domain, country))
        if not domain:
            self.TRL.debug_log('Missing Param C:%s and D:%s' % (not bool(domain), not bool(country)))
            raise self.EXCEPTIONS['MISSING_GET_PROXY_PARAMS']

        self._set_proxy(self.SERVICE_CALLS['get_proxy'](domain, country))

    def check_proxy(self, url, headers):
        self.TRL.debug_log('Proxy Check Tries:%s' % self.tries_left, proxy=self, headers=headers)
        if not self.tries_left:
            self.TRL.debug_log('Proxy Not Working', proxy=self, headers=headers)
            raise self.EXCEPTIONS['NOT_WORKING']

        try:
            _, response = self.get_request(url, headers, self, 10)
            self._check_response_code(response)
            self.TRL.debug_log('Got Working Proxy', proxy=self, headers=headers)
            return True
        except self.EXCEPTIONS['SERVER_DOWN_ERROR'] as e:
            time.sleep(5)
        except Exception as e:
            pass

        self.tries_left -= 1

        self.update_status_blocked()

        self.initiate_new_proxy()
        return self.check_proxy(url, headers)

    def to_python(self, protocol):
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise self.EXCEPTIONS['PROTOCOL_NOT_ALLOWED']
        return {"http": 'http://' + self.username + ':' + self.password + '@' + self.address + '/'}

    def to_driver(self, protocol):
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise self.EXCEPTIONS['PROTOCOL_NOT_ALLOWED']
        return self.address

    def to_log(self, protocol):
        if protocol not in self.ALLOWED_PROTOCOLS:
            raise self.EXCEPTIONS['PROTOCOL_NOT_ALLOWED']
        return self.address


class HotelLandingPageHandler(RequestHandler):

    # HOST = 'www.starwood.com'
    HOST = None

    RETRY_COUNT = 3
    EXCEPTIONS = {
        'INVALID_URL': exceptions.InvalidURL,
    }
    SERVICE_CALLS = {
        'get_user_agent': services.API.GetUserAgent
    }

    def __init__(self, request_data):

        # Meta Data
        self.request_id = request_data['requestId']
        self.sub_request_id = request_data['subRequestId']
        self.request_run_id = request_data['requestRunId']
        self.TRL.debug_log('INIT Crawling', self.request_id, self.sub_request_id, self.request_run_id)

        # Properties for Hotel List
        self.domain = request_data['domainName']
        self.country = request_data['country']
        self.city = request_data['RequestInputs']['city']
        self.children = request_data['RequestInputs']['children']
        self.adults = request_data['RequestInputs']['adults']

        self.hotel_name = request_data['RequestInputs']['hotelName']
        self.room = request_data['RequestInputs']['room']
        self.board = request_data['RequestInputs']['board']
        self.rating = request_data['RequestInputs']['starRating']
        self.hotel_wed_id = request_data['RequestInputs']['webSiteHotelId']
        self.pos = request_data['RequestInputs']['pos']

        self.check_in = request_data['RequestInputs']['checkIn']
        self.check_out = request_data['RequestInputs']['checkOut']
        self.nights = request_data['RequestInputs']['nights']
        self.days = request_data['RequestInputs']['days']
        self.start_time = datetime.datetime.now()
        self._html = None

        # Properties for Making Request
        self.cookie = None
        self.user_agent = self.SERVICE_CALLS['get_user_agent'](self.domain)
        self.TRL.debug_log('User Agent:%s' % self.user_agent, self.request_id, self.sub_request_id, self.request_run_id)
        # self.headers = {
        #     'User-Agent': self.user_agent.strip()
        # }
        self.headers = {
            'Host': self.HOST,
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng*/*;q=0.8',
            'User-Agent': self.user_agent.strip()
        }
        self.TRL.debug_log('Headers:%s' % self.headers, self.request_id, self.sub_request_id, self.request_run_id)
        proxy = ProxyHandler()
        proxy.initiate_new_proxy(self.domain, self.country)
        self.proxy = proxy

    @property
    def _clean_host_url(self):
        url = 'http://' + self.HOST
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

    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        raise NotImplementedError

    def _process_homepage(self):
        raise NotImplementedError

    def _url_maker(self):
        self.TRL.debug_log('Host:%s' % self._clean_host_url, self.request_id, self.sub_request_id, self.request_run_id)
        self.TRL.debug_log('Params:%s' % self._get_url_params, self.request_id, self.sub_request_id, self.request_run_id)

        return "".join([self._clean_host_url + '/'] + ['&%s=%s' % (p[0], p[1]) if i else '?%s=%s' % (p[0], p[1])
                                                       for i, p in self._get_url_params.items()])

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

        resp, resp_obj = self.get_request(link, self.headers, self.proxy)

        self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
        self._set_cookie(resp_obj)
        self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return html.fromstring(resp)

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = self._get_hotel_list()

    def _save_hotel(self, index, hotel_url):
        latitude_url = self._lat_long_links[self._hotels.index(str(hotel_url))]
        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url, self.request_id, self.sub_request_id, self.request_run_id)
        hotel = HotelHandler.get_hotel(hotel_url, latitude_url, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        hotel_data = hotel.save_html(index)
        return hotel_data

    def crawl_hotels(self):
        self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
        self._set_html()

        self.TRL.debug_log('Hotels Found:%s' % len(self._hotels), self.request_id, self.sub_request_id, self.request_run_id)
        return [self._save_hotel(i, hotel_url) for i, hotel_url in enumerate(self._hotels)]


class HotelHandler(RequestHandler):

    SERVICE_CALLS = {
        'save_html': services.API.SaveHtml
    }

    def __init__(self, landing_page, hotel_html):

        # Properties for Hotel
        self._landing_page = landing_page
        self._html = hotel_html
        self.city = landing_page.city
        self.start_time = landing_page.start_time
        self.check_in = landing_page.check_in
        self.check_out = landing_page.check_out

        # Properties for Making Request
        self.proxy = landing_page.proxy
        self.headers = landing_page.headers
        self.cookie = landing_page.cookie

    @property
    def _get_name(self):
        # hotelNameXpath
        raise NotImplementedError

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
        hotel_data['city'] = self.city
        hotel_data['checkIn'] = self.check_in
        hotel_data['checkOut'] = self.check_out

        # Crawler Output
        hotel_data['htmls'] = self._get_html
        hotel_data['hotelName'] = self._get_name
        hotel_data['roomTypes'] = self._get_room_types

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
    def get_hotel(cls, hotel_url, latitude_url, landing_page):
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers)

        resp_html, response = cls.get_request(hotel_url, headers, proxy)
        html_elem = {'html_element': resp_html, 'latitude_html': cls._get_latitude(latitude_url, proxy, headers, cookie)}
        return cls(landing_page, html_elem)

    @classmethod
    def _get_latitude(cls, latitude_url, proxy, headers, cookie):

        resp_html, response = cls.get_request(latitude_url, headers, proxy)
        return {'html_element': resp_html}
