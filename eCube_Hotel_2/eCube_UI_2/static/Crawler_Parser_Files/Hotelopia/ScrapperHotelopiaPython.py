import datetime
import copy
import math
import hashlib
from datetime import timedelta
import json
import requests
import pandas as pd
import time

from lxml import etree, html
from copy import deepcopy
from Crawling.scripts.Hotelbeds import ScrapperConfigHotelopiaPython
from Crawling.scripts.core import exceptions
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler


class HotelopiaLogger(CrawlingLogger):
    NAME = 'hotelopia_crawling'

HotelopiaLogger.set_logger()
CrawlerBase.TRL = HotelopiaLogger
CrawlerBase.CONFIG_FILE = ScrapperConfigHotelopiaPython


class HotelopiaHotel(HotelHandler):

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        pageHtml = html.fromstring(self._html['html_element'].encode('utf-8'))

        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0])

    @property
    def _get_cache_page(self):
        return self._html

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': self._landing_page._html.decode("utf-8")}

    @property
    def _get_room_types(self):
        roomType = self._html
        price = None
        return {'roomTypeHTML': roomType, 'priceHTML':price}

    @classmethod
    def get_hotel(cls, hotel_url, latitude_url, landing_page):
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers())

        # from pdb import set_trace; set_trace()
        # resp_html, response, _ = cls.get_request(cls.complete_hotel_url(hotel_url, landing_page.domain), headers, proxy, cookie=cookie)
        resp_html = html.tostring(hotel_url).decode('utf-8')
        html_elem = {'html_element': resp_html, 'latitude_html': None}
        return cls(landing_page, html_elem)

    def save_html(self, index,dest_code):
        hotel_data = dict()
        meta_data = dict()
        if self._landing_page.adults == 2:
            Adult_val = "2 Adt"
        elif self._landing_page.adults == 4:
            Adult_val = "2 Adt 2 Child"
        elif self._landing_page.adults == 3:
            Adult_val = "3 Adt"
        else:
            Adult_val = "1 Adt"
        # Properties from Parent
        hotel_data['index'] = index
        hotel_data['hotel_count'] = self.hotel_count
        hotel_data['city'] = self.city
        hotel_data['country'] = self.country
        hotel_data['city_zone'] = str(dest_code)
        hotel_data['checkIn'] = str(self.check_in)
        hotel_data['checkOut'] = str(self.check_out)
        hotel_data['pos'] = self._landing_page.pos
        hotel_data['adults'] = str(Adult_val)

        # Crawler Output
        hotel_data['htmls'] = self._get_html
        try:
            hotel_data['hotelName'] = self._get_name
        except Exception as e:
            raise self.EXCEPTIONS['HOTEL_NOT_FOUND'](str(e))
        hotel_data['roomTypes'] = self._get_room_types
        hotel_data['cachePageHTML'] = self._get_cache_page
        hotel_data['hotel_id'] = self._landing_page.hotel_web_id

        # Meta Data
        meta_data['requestId'] = self._landing_page.request_id
        meta_data['cachePageToken'] = self._get_cache_filename
        meta_data['subRequestId'] = self._landing_page.sub_request_id
        meta_data['requestRunId'] = self._landing_page.request_run_id
        meta_data['startDT'] = str(self.start_time)
        meta_data['endDT'] = str(datetime.datetime.now())
        hotel_data['meta'] = meta_data

        self.TRL.debug_log(
            'Saving Hotel:%s' % self._get_name, self._landing_page.request_id, self._landing_page.sub_request_id,
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers())
        hotel_data['meta']['cachePageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cache_page
        )
        # return self.SERVICE_CALLS['save_html'](hotel_data)
        response = copy.deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)


class HotelopiaLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.Hotelopia.com'
    HOTEL_HANDLER_CLASS = HotelopiaHotel
    HOTEL_LIST_DRIVER = False
    PROXY_LESS_HIT = True

    # def __init__(self, request_data):
    #     super(HotelopiaLandingPage, self).__init__(request_data)
    #     proxy = HotelopiaProxyHandler()
    #     proxy.initiate_new_proxy(self.domain_name, self.country)
    #     self.proxy = proxy


    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        # No hotel links are returned, hence passing a blank list

        lxml__elem = html.fromstring(str(self._html).encode('utf-8'))
        hotels = lxml__elem.xpath(self.CONFIG_FILE.hotelLinksXpath)
        self.hotel_count = len(hotels)
        #from pdb import set_trace; set_trace()
        return hotels

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        return [self._clean_host_url + lt for lt in html.fromstring(str(self._html)).xpath(self.CONFIG_FILE.latLongXpath)]

    @property
    def _get_url_params(self):

        return {}

    def _url_maker(self):
        self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id, self.request_run_id)
        self.TRL.debug_log('Params:%s' % self._get_url_params, self.request_id, self.sub_request_id, self.request_run_id)
        return "https://api.hotelbeds.com/hotel-api/1.0/hotels"

    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        # from pdb import set_trace; set_trace()
        pass


    def _process_homepage(self):
        pass

    # @property
    def _get_headers(self, encrypt=False):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """

        if encrypt:
            headers = {"Host": "www.convertstring.com",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        else:
            signature, api_key, secret = self.get_SSH__signature
            headers = {
                "Api-Key": api_key,
                "X-Signature": signature,
                "Accept": "application/xml",
                "Content-Type": "application/xml",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

        return headers

    def _get_hotel_list(self, url=None):
        if not url:
            link = self._url_maker()
        elif isinstance(url, str):
            link = url
        elif callable(url):
            link = url(self)
        else:
            self.TRL.error_log('Invalid URL to get Hotel List', self.request_id, self.sub_request_id,
                               self.request_run_id)
            raise self.EXCEPTIONS['INVALID_URL']

        # from pdb import set_trace; set_trace()
        # print("self.proxy.address")
        # print(self.proxy.address)

        pos = self.pos
        # outAirport = self.toAirport
        # inAirport = self.fromAirport

        payload = self.get_request_xml_string
        resp, resp_obj, _ = self.post_request_without_proxy(link, self._get_headers(), body=payload, driver=self.HOTEL_LIST_DRIVER)

        self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
        request_type = RequestHandler._get_request_type()
        if request_type['driver']:
            self._set_cookie(_)
        else:
            self._set_cookie(resp_obj)

        self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return resp

    # @classmethod
    # def post_request(cls, url, headers, body, body_type='url_string', cookie=None, timeout=10, driver=False):
    #
    #     request_type = cls._get_request_type()
    #     cls.TRL.debug_log('URL:%s' % url,  headers=headers)
    #     cls.TRL.debug_log('Request Type:%s' % request_type,  headers=headers)
    #     driver_obj = None
    #     if request_type['driver'] and driver:
    #         options = cls.OPTIONS
    #         # options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
    #         driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
    #         driver.get(url)
    #         driver_obj = driver
    #
    #     if request_type['request']:
    #         param_dict = {
    #             'url': url,
    #             'data': json.dumps(body) if body_type == 'json' else body,
    #             # 'proxies': proxy.to_python('http'),
    #             'headers': headers,
    #             'timeout': timeout,
    #         }
    #         if cookie:
    #             param_dict['cookies'] = cookie
    #
    #         response = requests.post(**param_dict)
    #         res_html = response.text
    #         res_obj = response
    #     else:
    #         raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']
    #     return res_html, res_obj, driver_obj

    @classmethod
    def post_request_without_proxy(cls, url, headers, body, body_type='url_string', cookie=None, timeout=60,
                                   driver=False):
        """
        :param url:
        :param headers:
        :param body: Post body
        :param body_type: url_string or json
        :param cookie:
        :param timeout:
        :return: response html and response object
        """
        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, headers=headers)
        driver_obj = None
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            # options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            # driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:
            param_dict = {
                'url': url,
                'data': json.dumps(body) if body_type == 'json' else body,
                'headers': headers,
                'timeout': timeout,
            }
            if cookie:
                param_dict['cookies'] = cookie

            response = requests.post(**param_dict)

            res_html = response.content
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj


    # @classmethod
    # def get_request(cls, url, headers, proxy, cookie=None, timeout=10, driver=False):
    #
    #     request_type = cls._get_request_type()
    #     cls.TRL.debug_log('URL:%s' % url, proxy=proxy, headers=headers)
    #     cls.TRL.debug_log('Request Type:%s' % request_type, proxy=proxy, headers=headers)
    #     driver_obj = None
    #
    #     # from pdb import set_trace; set_trace()
    #     if request_type['driver'] and driver:
    #         options = cls.OPTIONS
    #         options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
    #         driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
    #         driver.get(url)
    #         driver_obj = driver
    #
    #     if request_type['request']:
    #
    #         if '192.168.6.1' in url:
    #             response = requests.get(url, timeout=timeout)
    #         else:
    #             if cookie:
    #                 response = requests.get(url, proxies=proxy.to_python('http'), timeout=timeout)
    #             else:
    #                 response = requests.get(url, proxies=proxy.to_python('http'), timeout=timeout)
    #
    #         res_html = response.content
    #         res_obj = response
    #     else:
    #         raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']
    #
    #     return res_html, res_obj, driver_obj

    @classmethod
    def get_request_without_proxy(cls, url, headers, cookie=None, timeout=120, driver=False):
        """
        :param url:
        :param headers:
        :param proxy:
        :param cookie:
        :param timeout:
        :return: response html and response object
        """
        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, headers=headers)
        driver_obj = None

        # from pdb import set_trace; set_trace()
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            # options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:
            if '192.168.6.1' in url:
                response = requests.get(url, timeout=timeout)
            else:
                if cookie:
                     response = requests.get(url, headers=headers, timeout=timeout, cookies=cookie)
                else:
                     response = requests.get(url, headers=headers, timeout=timeout)

            res_html = response.text
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj

    @property
    def get_request_xml_string(self):
        codes = self.get_primary_hotels
        # from pdb import set_trace; set_trace()
        code_batch = codes
        currency, source_market = self.get_currency__source_mrkt(self.city, self.pos)
        yy1, mm1, dd1 = self.set_checkIn(inDate=self.check_in)
        yy2, mm2, dd2 = self.set_checkOut(outDate=self.check_out)
        strDestinationCode=self.Destination_code(self.city)
        payload = ""
        #from pdb import set_trace; set_trace()
        if currency:
            payload = payload + '<availabilityRQ xmlns="http://www.hotelbeds.com/schemas/messages" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" sourceMarket="{}" Currency="{}">'.format(
                source_market, currency)
            payload = payload + '<stay checkIn="{}-{}-{}" checkOut="{}-{}-{}"/>'.format(yy1, mm1, dd1, yy2, mm2, dd2)
            payload = payload + '<occupancies><occupancy rooms="1" adults="{}" children="{}">'.format(self.adults, self.children)

        if self.adults == 4:
            payload = payload + "<paxes><pax type=""CH"" age=""6""/><pax type=""CH"" age=""8""/></paxes>"

        payload = payload + '</occupancy></occupancies><destination code="' + strDestinationCode + '"/></availabilityRQ>'
        return payload

    @property
    def get_primary_hotels(self):

        url = "http://192.168.6.1/HotelBedsAvailibilityReport/ui/matchingdll/primaryhotel.aspx?strCountry={}&strCity={}".format(
            self.country, self.city)
        # response, response_obj, driver_obj = self.get_request(url, headers=self._get_headers(), proxy=self.proxy)
        response= requests.get(url, verify=False)
#        response, response_obj, driver_obj = self.get_request_without_proxy(url, headers=self._get_headers())
        xml__elem = etree.fromstring(response.text)
        codes = xml__elem.xpath('//nvcrWebSiteHotelId/text()')
        codes = list(map(lambda x: '<hotel>{}</hotel>'.format(x), codes))
        return codes

    @property
    def get_SSH__signature(self):
        epochTime = int(datetime.datetime.now().timestamp())
        api_key, secret = self.get_apikey_secret(self.pos)
        signature_temp = api_key + secret + str(epochTime)
        sha_signature = hashlib.sha256(signature_temp.encode('utf-8')).hexdigest()

        return sha_signature, api_key, secret

    def get_apikey_secret(self, pos):
        pos = pos.lower()
        if pos == "United Kingdom".lower(): return "v2un2yt8t8te92jsjwvsdq5m", "VEASW6bxD7"
        if pos == "Spain".lower(): return "jb8qgpugswajmpuqr54zgp4y", "mBYbr87kjK"


    def get_currency__source_mrkt(self, area, country):
        area = area.lower()
        country = country.lower()
        if area == "IBIZA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "IBIZA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Stockholm".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Zion National Park - UT".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "PRAGUE".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "KUALA LUMPUR".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "ANDORRA".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Niagara Falls".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "MADRID".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "COSTA DEL SOL".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "PHUKET".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Daytona Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "ROME".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Kedah / Langkawi".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Cocoa Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Paris".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "ALGARVE".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "TENERIFE".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "BANGKOK".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Vancouver Island".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "COPENHAGEN".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "WARSAW".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Quebec".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "FUERTEVENTURA".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "SINGAPORE".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Antalya".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Alanya".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Orlando Area - Florida - FL".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "AGADIR".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "MARRAKECH".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "GRAN CANARIA".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "DUBAI".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "KRAKOW".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Canadian Rockies".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "GRANADA".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Ottawa".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Majorca".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "BALI".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "BARCELONA".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "BERLIN".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "BERLIN".lower() and country == "Spain".lower(): return "GBP", "ES"
        if area == "London".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "LANZAROTE".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Amsterdam and vicinity".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "SEVILLE".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Las Vegas - NV".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Las Vegas - NV".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "HONG KONG".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Abu Dhabi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"

    def Destination_code (self,area):
        area = area.lower()
        if area == "Stockholm".lower(): return "STO"
        if area == "Zion National Park - UT".lower() : return "SGU"
        if area == "PRAGUE".lower(): return "PRG"
        if area == "ANDORRA".lower(): return "AND"
        if area == "Paris".lower(): return "PAR"
        if area == "Niagara Falls".lower(): return "NI"
        if area == "MADRID".lower(): return "MAD"
        if area == "COSTA DEL SOL".lower(): return "AGP"
        if area == "ROME".lower(): return "ROE"
        if area == "Kedah / Langkawi".lower(): return "LGK"
        if area == "Cocoa Area - FL".lower(): return "COI"
        if area == "Berlin".lower(): return "BER"
        if area == "TENERIFE".lower(): return "TFS"
        if area == "BANGKOK".lower(): return "BKK"
        if area == "KUALA LUMPUR".lower() : return "KUL"
        if area == "Vancouver Island".lower(): return "BC"
        if area == "COPENHAGEN".lower(): return "CPH"
        if area == "WARSAW".lower(): return "WAW"
        if area == "FUERTEVENTURA".lower(): return "FUE"
        if area == "SINGAPORE".lower(): return "SIN"
        if area == "Alanya".lower(): return "GBP", "UK"
        if area == "Orlando Area - Florida - FL".lower(): return "MCO"
        if area == "AGADIR".lower(): return "AGA"
        if area == "GRAN CANARIA".lower(): return "LPA"
        if area == "KRAKOW".lower(): return "KRK"
        if area == "GRANADA".lower(): return "GRX"
        if area == "Majorca".lower(): return "PMI"
        if area == "BALI".lower(): return "BAI"
        if area == "BARCELONA".lower(): return "+BCN"
        if area == "London".lower(): return "LON"
        if area == "LANZAROTE".lower(): return "ACE"
        if area == "Amsterdam and vicinity".lower(): return "AMS"
        if area == "SEVILLE".lower(): return "SVQ"
        if area == "Las Vegas - NV".lower(): return "LVS"
        if area == "HONG KONG".lower(): return "HKG"
        if area == "IBIZA".lower(): return "IBZ"


    def set_checkIn(self, inDate):
        #from pdb import set_trace; set_trace()
        current_date = self.check_in.date()
        current_date = current_date.strftime('%Y-%m-%d')

        inYear, inMonth, inDay = current_date.split('-')
        try:
            inDay, inMonth, inYear = inDate.split('/')
        except:
            pass
        try:
            inDay, inMonth, inYear = inDate.split('-')
        except:
            pass
        try:
            inDay, inMonth, inYear = inDate.split(':')
        except:
            pass
        try:
            inDay, inMonth, inYear = inDate.split('.')
        except:
            pass
        return inYear, inMonth, inDay


    def set_checkOut(self, outDate):
        #from pdb import set_trace; set_trace()
        current_date = self.check_out.date()
        current_date = current_date.strftime('%Y-%m-%d')

        outYear, outMonth, outDay = current_date.split('-')
        try:
            outDay, outMonth, outYear = outDate.split('/')
        except:
            pass
        try:
            outDay, outMonth, outYear = outDate.split('-')
        except:
            pass
        try:
            outDay, outMonth, outYear = outDate.split(':')
        except:
            pass
        try:
            outDay, outMonth, outYear = outDate.split('.')
        except:
            pass
        return outYear, outMonth, outDay


    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = self._get_hotel_list()



    def _save_hotel(self, index, hotel_url,zone_index):
        latitude_url = None
        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url, self.request_id, self.sub_request_id, self.request_run_id)

        if self.hotels_id_dict is not None:
            self._set_hotel_web_id(self.hotels_id_dict[index])

        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(hotel_url, latitude_url, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        dest_code = html.fromstring(self._html).xpath(self.CONFIG_FILE.hotel_ZoneName)[0]
        dest_code = str(dest_code) + "_" + str(zone_index)
        #hotel_data = hotel.save_html(index, dest_code)
        return hotel.save_html(index, dest_code)

    def crawl_hotels(self, redelivered):
        # redelivered = False
        partial_hotels = list()
        if redelivered:
            partial_hotels = self.SERVICE_CALLS['get_partial_hotels'](self.sub_request_id)
            print('crawled_hotels found')
            print(len(partial_hotels))

        self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
        try:
            self._set_html()
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ProxyError
        ) as e:
            raise self.EXCEPTIONS['SCRIPT_TIMEOUT']

        self.TRL.debug_log('Hotels Found:%s' % len(self._hotels), self.request_id, self.sub_request_id, self.request_run_id)
        crawled_hotels = partial_hotels
        hotels_count = len(crawled_hotels)


        zone_count = math.ceil(len(self._hotels)/200)
        zone_count=zone_count+1
        i=0
        for zone_index in range(zone_count):
            zone_index=zone_index+1
            if zone_index>1:
                hotels_count=xx
            xx=200*zone_index
            # for i, hotel_url in enumerate(self._hotels[hotels_count:xx]):
            for hotel_url in self._hotels[hotels_count:xx]:
                # for i, hotel_url in enumerate(self._hotels[hotels_count:hotels_count+2]):
                print("indexxx====",i)
                # i += hotels_count
                # time.sleep(1)
                # hotel = self._save_hotel(i, hotel_url)
                # crawled_hotels.append(hotel)
                try:
                    hotel = self._save_hotel(i, hotel_url,zone_index)
                    crawled_hotels.append(i)
                    self.SERVICE_CALLS['increase_completed_hotel_count']()
                except (
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.ProxyError
                ) as e:
                    self.request_data.update({'hotels': crawled_hotels})
                    self.SERVICE_CALLS['save_partial_hotels'](self.request_data, str(e))
                    raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
                except self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']:
                    pass
                self.request_data.update({'hotels': crawled_hotels})
                i = i + 1
        return self.request_data


# def crawl_hotels(consumer_data, redelivered):
#     return HotelbedsLandingPage(consumer_data).crawl_hotels(redelivered)


############test bed compatile###############
def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    crawled_data = HotelopiaLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    return crawled_data



