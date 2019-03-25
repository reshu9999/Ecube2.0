import datetime
import copy
import math
from datetime import timedelta
import json
import requests
import hashlib
import pandas as pd
import time
import copy

from lxml import etree, html
from Crawling.scripts.Hotelbeds import ScrapperConfigHotelbedsPython
from Crawling.scripts.core import exceptions
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler


class HotelbedsLogger(CrawlingLogger):
    NAME = 'hotelbeds_crawling'

HotelbedsLogger.set_logger()
CrawlerBase.TRL = HotelbedsLogger
CrawlerBase.CONFIG_FILE = ScrapperConfigHotelbedsPython



class HotelbedsHotel(HotelHandler):

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
        return str(self._html)

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

        #from pdb import set_trace; set_trace()
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
        response = copy.deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)


class HotelbedsLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.Hotelbeds.com'
    HOTEL_HANDLER_CLASS = HotelbedsHotel
    HOTEL_LIST_DRIVER = False
    PROXY_LESS_HIT = True
    PROXY_VENDOR_WISE=None
    
    # def __init__(self,request_data):
    #     super(HotelbedsLandingPage,self).__init__(request_data)
    #     proxy=HotelbedsProxyHandler()
    #     proxy.initiate_new_proxy(self.domain_name,self.country)
    #     self.proxy=proxy

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

        #from pdb import set_trace; set_trace()
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            # options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:
            if 'eclerx' in url:
                #from pdb import set_trace; set_trace()
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
        #from pdb import set_trace; set_trace()
        code_batch = codes
        currency, source_market = self.get_currency__source_mrkt(self.city, self.pos)
        yy1, mm1, dd1 = self.set_checkIn(inDate=self.check_in)
        yy2, mm2, dd2 = self.set_checkOut(outDate=self.check_out)
        payload = ""
        if currency:
            payload = payload + '<availabilityRQ xmlns="http://www.hotelbeds.com/schemas/messages" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" sourceMarket="{}" Currency="{}">'.format(
                source_market, currency)
            payload = payload + '<stay checkIn="{}-{}-{}" checkOut="{}-{}-{}"/>'.format(yy1, mm1, dd1, yy2, mm2, dd2)
            payload = payload + '<occupancies><occupancy rooms="1" adults="{}" children="{}">'.format(self.adults, self.children)

        if self.adults == 4:
            payload = payload + "<paxes><pax type=""CH"" age=""6""/><pax type=""CH"" age=""8""/></paxes>"

        payload = payload + "</occupancy></occupancies><hotels>" + "".join(code_batch) + "</hotels></availabilityRQ>"
        return payload

    @property
    def get_primary_hotels(self):

        # url = "http://192.168.6.1/HotelBedsAvailibilityReport/ui/matchingdll/primaryhotel.aspx?strCountry={}&strCity={}".format(
        #     self.country, self.city)

        url = "http://10.100.18.86:8001/api/v1/GetMatchingPrimaryHotels?city={0}&country={1}".format(
            self.city.upper(), self.country.upper())
        print(url)
#        response, response_obj, driver_obj = self.get_headerless_request(url,proxy=self.proxy)
        response = requests.get(url,verify=False)
        #response, response_obj, driver_obj = self.get_request_without_proxy(url, headers=self._get_headers())
        xml__elem = etree.fromstring(response.text.replace('{"ResultData":"','').replace('<?xml version=\\"1.0\\" encoding=\\"UTF-8\\" ?>','').replace('","StatusCode":200}',''))
        codes = xml__elem.xpath('//nvcrWebSiteHotelId/text()')
        codes = list(map(lambda x: '<hotel>{}</hotel>'.format(x), codes))
        return codes

    # @property
    # def get_SSH__signature(self):
    #     headers = self._get_headers(encrypt=True)
    #     url = 'http://www.convertstring.com/Hash/SHA256'
    #     api_key, secret = self.get_apikey_secret(self.pos)
    #     signature_Temp = '{}{}{}'.format(api_key, secret, int(time.time()))
    #     payload = "InputOptions.Salt=&InputOptions.Type=ConvertString.Model.Tool.Options.HashInputOptions&InputOptions.Type=ConvertString.Model.Tool.Options.HashInputOptions&input=" + signature_Temp + "&outputtype=outputstring"
    #
    #     response, response_obj, driver_obj = self.post_request(url, headers,self.proxy,  body=payload)
    #     lxml__elem = html.fromstring(response)
    #     xsignature = lxml__elem.xpath('//*[@id="output"]/text()')[0]
    #     return xsignature, api_key, secret
    @property
    def get_SSH__signature(self):
        epochTime = int(datetime.datetime.now().timestamp())
        api_key, secret = self.get_apikey_secret(self.pos)
        signature_temp = api_key + secret + str(epochTime)
        sha_signature = hashlib.sha256(signature_temp.encode('utf-8')).hexdigest()

        return sha_signature, api_key, secret


    def get_apikey_secret(self, pos):
        pos = pos.lower()
        if pos == "afghanistan": return "puk7bgpazveakhddz646e83f", "etyUj7z4hs"
        if pos == "afghanistan": return "hr5v884jz3x7pz3mezqtyhxx", "H59YQadv3W"
        if pos == "france": return "ywwevfb734wtqh9wrbegw7hr", "35VuVMT4pG"
        if pos == "mexico": return "a8djbzumcw4xbfzhmj7y5tah", "WnMe3kKaJY"
        if pos == "spain": return "naumpmnjz7uhxahfds8ethhz", "6gVFRvXn3H"
        if pos == "united kingdom": return "teb45ernyj9rsz2cmzxupn8t", "etyUj7z4hs"
        if pos == "united states - usa": return "6kbt3c7td4n2kwx6p23npw8t", "B4vKp4AKgj"
        if pos == "indonesia": return "yxxjm3jcp6mk929hwmvgfcxe", "SXR33fe8st"
        if pos == "australia": return "y3kcmqyrhtnmmsd9z9qdyaye", "3a97vE5qEq"
        if pos == "argentina": return "jtgqfcrasjm85hfdc55q3ucf", "CFaU7qq4yp"
        if pos == "germany": return "vnj84yhbxq3jx5ktk4sa2smd", "du2Gn4aTUv"
        if pos == "united arab emirates": return "29gyvb6zxm9tdnm7zmdufctq", "BuwYftakvK"
        if pos == "portugal": return "2v9pcdwpn5xdtb38supahk96", "eDBTf4gzaf"
        if pos == "saudi arabia": return "sbwndp55xv695u24q9cwbkkg", "dUnBbYVmg5"
        if pos == "greece": return "4y9sqh3vs9aty7jrjdmye6yg", "A4ykmssXvG"
        if pos == "costa rica": return "nt3r2d7gzvdbtfjcegnscyzc", "cg5BAYxEGT"
        if pos == "malaysia": return "s3gezjx7pxredmzh4tx9qust", "W5sy6cdkv5"
        if pos == "india": return "tx6k7abnwcjnvwukgphgmqe8", "QPnERNTcEw"
        if pos == "south korea": return "xyr4c3waswea56faytxw387p", "PtX3Eg9Ngq"
        if pos == "colombia": return "bxpjj3wqd6y87nywmm82tssr", "S58agrrRDQ"
        if pos == "hong hong": return "c53gxsmrs2wucdyysfzadcnz", "vv5pu9XhCH"
        if pos == "china": return "exrj39amff4de5ertu7xrt7g", "HJChf929U4"


    def get_currency__source_mrkt(self, area, country):
        area = area.lower()
        country = country.lower()
        if area == "Grand Canyon National Park Area - AZ".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Scottsdale - AZ".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Girona".lower() and country == "UNITED Kingdom".lower(): return "EUR", "UK"
        if area == "Costa de Valencia".lower() and country == "UNITED Kingdom".lower(): return "EUR", "UK"
        if area == "Jacksonville Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "New Orleans - LA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Fort Lauderdale - Hollywood Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Baltimore - MD".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Buenos Aires".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Jakarta".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "New York Area - NY".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Bahrain".lower() and country == "SAUDI ARABIA".lower(): return "USD", "SA"
        if area == "Bahrain".lower() and country == "UNITED ARAB EMIRATES".lower(): return "AED", "AE"
        if area == "MONTREAL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "South Sardinia".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Stockholm".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Stockholm".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "MENORCA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MENORCA".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "HAMBURG".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Izmir".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Izmir".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Chicago - IL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Maldives".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "County Cork".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Riviera Maya / Playa del Carmen".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Bangalore".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Sarasota Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "BUCHAREST".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "PUNTA CANA".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Kusadasi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Hammamet".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Hammamet".lower() and country == "Germany".lower(): return "EUR", "DE"
        if area == "MUNICH".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Amsterdam and vicinity".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "FLORENCE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Cancun (and vicinity)".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "PORTO".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Majorca".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MILAN".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Kos".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MALTA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "ACAPULCO".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Riviera Maya / Playa del Carmen".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "FRANKFURT".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "FRANKFURT".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "California Wine Country - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Marmaris".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Aruba".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Minneapolis - MN".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Dubrovnik-South Dalmatia".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "SINGAPORE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Beijing Peking".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Thessaloniki".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Buenos Aires".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Delhi and NCR".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Los Cabos".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Montpellier".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Montpellier".lower() and country == "spain".lower(): return "EUR", "ES"
        if area == "Philadelphia - PA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Melbourne - VIC".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Melbourne - VIC".lower() and country == "Australia".lower(): return "AUD", "AU"
        if area == "Penang".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Penang".lower() and country == "INDONESIA".lower(): return "USD", "ID"
        if area == "Santiago de Chile".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Majorca".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Brussels".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Brussels".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Tampa - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Mexico City".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Pyrenees - Catalan".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Pyrenees - Catalan".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Strasbourg".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Strasbourg".lower() and country == "spain".lower(): return "EUR", "ES"
        if area == "FRANKFURT".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "LIVERPOOL".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "London".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "St. Petersburg Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Aruba".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Bordeaux".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Bordeaux".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Florida Keys - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Edinburgh".lower() and country == "SPAIN".lower(): return "GBP", "ES"
        if area == "Mauritius Islands".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Phoenix Area - AZ".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Biarritz".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "PRAGUE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Clearwater Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "KRAKOW".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Costa Brava and Costa Barcelona-Maresme".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Fethiye-Oludeniz".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Palm Beach Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "GRANADA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Chicago - IL".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "NICE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Otago- Queenstown".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Kemer".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Kemer".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Alentejo".lower() and country == "PORTUGAL".lower(): return "EUR", "PT"
        if area == "Alentejo".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "TURIN".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Helsinki".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Fez".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Maceio".lower() and country == "ARGENTINA".lower(): return "USD", "AR"
        if area == "Vancouver".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Siena".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "ALGARVE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "ALGARVE".lower() and country == "Portugal".lower(): return "EUR", "PT"
        if area == "Aberdeen".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Orlando Area - Florida - FL".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Rio de Janeiro".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Rio de Janeiro".lower() and country == "UNITED KINGDOM".lower(): return "MXN", "UK"
        if area == "Perth - WA".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Portland - OR".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Northern Cyprus".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "ROME".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "ROME".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "San Diego - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "San Jose / Central Valley".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Tel Aviv".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Kusadasi".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Cordoba".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "CRETE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "FLORENCE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Canadian Rockies".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Newcastle-upon-Tyne".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "MARRAKECH".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Paris".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Almeria Coast-Almeria".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Almeria Coast-Almeria".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "RIGA".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "RIGA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "COSTA DEL SOL".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "GENEVA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Pyrenees - Aragon".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Dublin".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Metro Manila".lower() and country == "UNITED STATES - USA".lower(): return "EUR", "US"
        if area == "BUDAPEST".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Rimini".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Adelaide - SA".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Adelaide - SA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "LYON".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Neapolitan Riviera".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "AGADIR".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Sitges Area - Costa del Garraf".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Hurghada".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Oslo".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Puerto Rico Island".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Benidorm - Costa Blanca".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Casablanca".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Amsterdam and vicinity".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Riviera Maya / Playa del Carmen".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Split-Middle Dalmatia".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Vancouver Island".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Ankara".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "CANNES".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Avignon".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Blackpool".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "GRANADA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Austin - TX".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Hawaii - Oahu - HI".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "TENERIFE".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Paris".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "GENEVA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Salzburg".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Centre Portugal".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "PHUKET".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Azores".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Azores".lower() and country == "PORTUGAL".lower(): return "EUR", "PT"
        if area == "Bournemouth".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "PRAGUE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "COSTA DE AZAHAR".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "GOLD COAST - QLD".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Cantabria".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Goa".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Kvarner Bay".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "GRAN CANARIA".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "BARCELONA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "KUALA LUMPUR".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "KUALA LUMPUR".lower() and country == "INDONESIA".lower(): return "USD", "ID"
        if area == "GLASGOW".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Ixtapa - Zihuatanejo".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Centre Portugal".lower() and country == "PORTUGAL".lower(): return "EUR", "PT"
        if area == "BERLIN".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Cancun (and vicinity)".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Belek".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Oslo".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "New York Area - NY".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Memphis - TN".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Channel Islands".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "LISBON".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Las Vegas - NV".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Skiathos".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "COSTA DE AZAHAR".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Boston - MA".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "BARCELONA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "VIENNA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Estoril Coast".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Barbados".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Buenos Aires".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "MALAGA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MOSCOW".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Peloponesse".lower() and country == "GREECE".lower(): return "EUR", "GR"
        if area == "Peloponesse".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Central and North Greece".lower() and country == "GREECE".lower(): return "EUR", "GR"
        if area == "Central and North Greece".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "CHIANG MAI".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Buzios".lower() and country == "ARGENTINA".lower(): return "USD", "AR"
        if area == "Corsica".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Corsica".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "BALI".lower() and country == "INDONESIA".lower(): return "USD", "ID"
        if area == "BALI".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Belek".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Jakarta".lower() and country == "INDONESIA".lower(): return "USD", "ID"
        if area == "Jakarta".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "MADRID".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Lake Tahoe - CA/NV".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "French Alps".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "IBIZA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "IBIZA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "BERLIN".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "TALLINN".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "St Petersburg".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "St Petersburg".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Zanzibar".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Los Angeles - CA".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Zion National Park - UT".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Santa Barbara Area - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Cairns - QLD".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Salou Area / Costa Dorada".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "North Sardinia".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "PAPHOS".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Mauritius Islands".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Calgary".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Guadalajara and Vicinity".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "MUNICH".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "North Sardinia".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "ALGARVE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Auckland".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "GRAN CANARIA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "BUDAPEST".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "SEOUL".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "FUERTEVENTURA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Bogota".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Zaragoza".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Zaragoza".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "ATHENS".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Hawaii - Oahu - HI".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Salou Area / Costa Dorada".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Washington D.C. - DC".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "BALI".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Fethiye-Oludeniz".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Denver - CO".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "MARSEILLE".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "MARSEILLE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Tours".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Cadiz / Jerez".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "AGADIR".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Niagara Falls".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Hurghada".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "BERLIN".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Las Vegas - NV".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "ATHENS".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Palm Springs - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Krabi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Metro Manila".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Bourgas / Black Sea Resorts".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Boston - MA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "BOLOGNA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Ho Chi Minh City (Saigon) and South".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Alicante - Costa Blanca".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Istria".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Salvador de la Bahia".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "San Jose - Silicon Valley - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Montego Bay".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Nashville - TN".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "HONG KONG".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Los Cabos".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Golfe de Saint Tropez".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Golfe de Saint Tropez".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Vizcaya - Bilbao".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Guangzhou".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Guangzhou".lower() and country == "CHINA".lower(): return "CNY", "CN"
        if area == "Sharm el Sheikh -Dahab".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Sharm el Sheikh -Dahab".lower() and country == "Germany".lower(): return "EUR", "DE"
        if area == "Costa De La Luz (Cadiz)".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Costa De La Luz (Cadiz)".lower() and country == "United Kingdom".lower(): return "EUR", "ES"
        if area == "Estoril Coast".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Zurich".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Amsterdam and vicinity".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Gdansk".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Porto and North of Portugal".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Medellin".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Gauteng- Johannesburg".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Panama City".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Porto SeguroVitoria".lower() and country == "ARGENTINA".lower(): return "USD", "AR"
        if area == "Lake Garda".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "MALAGA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "SEVILLE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "MYKONOS".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "TOULOUSE".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "TOULOUSE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "WARSAW".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "County Galway".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Benidorm - Costa Blanca".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Houston - TX".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "ISTANBUL".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Sydney - NSW".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Sydney - NSW".lower() and country == "Australia".lower(): return "AUD", "AU"
        if area == "Sydney - NSW".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "LISBON".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "GRAN CANARIA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "PUERTO VALLARTA".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Charleston - SC".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Atlanta - GA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Lima".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Quebec".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Doha".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Doha".lower() and country == "UNITED ARAB EMIRATES".lower(): return "USD", "AE"
        if area == "Verona".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "ASTURIAS".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "ASTURIAS".lower() and country == "United Kingdom".lower(): return "EUR", "ES"
        if area == "Kedah / Langkawi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "COPENHAGEN".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Naples".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "COSTA DE ALMERIA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "A Coruna".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Lago de Garda".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "California Coast - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Alicante - Costa Blanca".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Costa De La Luz (Huelva)".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Majorca".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Nassau".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "SEVILLE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Alanya".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "San Francisco Area - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "FUERTEVENTURA".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Siem Reap - North".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "BODRUM".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Hawaii - Maui - HI".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Brisbane - QLD".lower() and country == "AUSTRALIA".lower(): return "AUD", "AU"
        if area == "Bandung".lower() and country == "INDONESIA".lower(): return "USD", "ID"
        if area == "Nantes".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Nantes".lower() and country == "spain".lower(): return "EUR", "ES"
        if area == "Daytona Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Istria".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "SANTORINI".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Sicily".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Genoa".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Cologne / Bonn".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Hua Hin-Cha Am-Pranburi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Halkidiki".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Hanoi and North".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "W. Cape-Cape Town-Garden Route".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "SHANGHAI".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "SHANGHAI".lower() and country == "China".lower(): return "CNY", "CN"
        if area == "Venice (and vicinity)".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Venice (and vicinity)".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "Leeds".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Ottawa".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Fort Myers Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "TORONTO".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "TORONTO".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "CORFU".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "PUNTA CANA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Sofia".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Ayia Napa".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Dublin".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "TENERIFE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MANCHESTER".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "COSTA DEL SOL".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Taipei".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Taipei".lower() and country == "HONG KONG".lower(): return "USD", "HK"
        if area == "SAO PAULO".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "MADRID".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "BANGKOK".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "BANGKOK".lower() and country == "Spain".lower(): return "EUR", "ES"
        if area == "TENERIFE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Salt Lake City - UT".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Dallas - TX".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Samos".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "FUERTEVENTURA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "VIENNA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "SINGAPORE".lower() and country == "INDONESIA".lower(): return "SGD", "ID"
        if area == "SAO PAULO".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "Pattaya-Chonburi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Halkidiki".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "MUNICH".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "New Orleans - LA".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Mumbai".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Side".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "KRAKOW".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Zante".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "RHODES".lower() and chountry == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MADEIRA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Dusseldorf".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "LANZAROTE".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Mexico City".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "INVERNESS".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Koh Samui".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Nairobi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MARRAKECH".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Pontevedra".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Lourdes".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Zurich".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "VALENCIA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "VALENCIA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "ISTANBUL".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "ISTANBUL".lower() and country == "UNITED ARAB EMIRATES".lower(): return "EUR", "AE"
        if area == "Miami Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "York".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "COPENHAGEN".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Malacca Johor and South".lower() and country == "INDONESIA".lower(): return "USD", "ID"
        if area == "ANDORRA".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "ANDORRA".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "BRISTOL".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Santiago de Chile".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "New York Area - NY".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Cancun (and vicinity)".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Edinburgh".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Kyoto".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Kyoto".lower() and country == "China".lower(): return "CNX", "CN"
        if area == "Kyoto".lower() and country == "United Kingdom".lower(): return "JPY", "UK"
        if area == "Austrian Alps".lower() and country == "SAUDI ARABIA".lower(): return "EUR", "SA"
        if area == "Austrian Alps".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Washington D.C. - DC".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Savannah - GA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Cocoa Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Sitges Area - Costa del Garraf".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Merida - Yucatan".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Cairo".lower() and country == "UNITED ARAB EMIRATES".lower(): return "EUR", "AE"
        if area == "Cairo".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Cairo".lower() and country == "Germany".lower(): return "EUR", "DE"
        if area == "Tokyo".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "San Antonio - TX".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Seattle - WA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "San Francisco Area - CA".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Antalya".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Varna / Black Sea Resorts".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Abu Dhabi".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Kefalonia".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Amman".lower() and country == "UNITED ARAB EMIRATES".lower(): return "EUR", "AE"
        if area == "Amman".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "London".lower() and country == "SPAIN".lower(): return "GBP", "ES"
        if area == "Bansko".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Los Angeles - CA".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Naples Area - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "LANZAROTE".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Djerba".lower() and country == "FRANCE".lower(): return "EUR", "FR"
        if area == "Reno - NV".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Costa Brava and Costa Barcelona-Maresme".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Myrtle Beach - SC".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "DUBAI".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "DUBAI".lower() and country == "UNITED ARAB EMIRATES".lower(): return "USD", "AE"
        if area == "Navarra".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "MILAN".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Stuttgart".lower() and country == "GERMANY".lower(): return "EUR", "DE"
        if area == "Orlando Area - Florida - FL".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Lake Garda".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Porto and North of Portugal".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "Porto and North of Portugal".lower() and country == "Portugal".lower(): return "EUR", "PT"
        if area == "Riviera Maya / Playa del Carmen".lower() and country == "SPAIN".lower(): return "USD", "ES"
        if area == "BELFAST".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Side".lower() and country == "Germany".lower(): return "EUR", "DE"
        if area == "Memphis - TN".lower() and country == "United Kingdom".lower(): return "USD", "UK"
        if area == "Monterrey".lower() and country == "MEXICO".lower(): return "MXN", "MX"
        if area == "Osaka".lower() and country == "United Kingdom".lower(): return "EUR", "UK"
        if area == "MOSCOW".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "Djerba".lower() and country == "SPAIN".lower(): return "EUR", "ES"
        if area == "SINGAPORE".lower() and country == "China".lower(): return "CNY", "CN"
        if area == "Neapolitan Riviera".lower() and country == "United Kingdom".lower(): return "CNY", "UK"
        if area == "Marseille".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Rimini".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Pyrenees - Aragon".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Vizcaya - Bilbao".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Cadiz / Jerez".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Centre Portugal".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Costa De La Luz (Huelva)".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Cordoba".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "A CoruNa".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Cantabria".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Pontevedra".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Acapulco".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Alava".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Alentejo".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Altinkum - Didim".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Antwerp".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Ankara".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Avignon".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Badajoz".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Basel".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Belgrade".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Bergamo".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Biarritz".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Boracay Island".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Bratislava".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Bremen".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Brighton".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Bruges".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Burgos".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Bursa".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Buzios".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Caceres".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Capri".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Cardiff".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Casablanca".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Castellon".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Cebu".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Chiapas".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Como".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Corsica".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Pacific Central Coast".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Pacific North Coast / Guanacaste".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "County Kerry".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Curitiba".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Djerba".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Djerba".lower() and country == "GERMANY".lower(): return "GBP", "DE"
        if area == "Dortmund".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Essen".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Florianopolis".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Formentera".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Fortaleza".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Gdansk".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Gothenburg".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Grenoble".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Guadalajara and Vicinity".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Guipuzcoa - San Sebastian".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Hannover".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Hawaii - Kauai - HI".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Hawaii - The Big Island - HI".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Hoi An - Danang - Central".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Huelva".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Iguazu Falls".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Innsbruck".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Ixtapa - Zihuatanejo".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Jaen".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Jerusalem Region".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Khao Lak and Phang Nga".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Kuantan and Pahang".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Kvarner Bay".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "La Gomera".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "La Manga - Costa Calida".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "La Palma".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "La Rioja".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Leipzig".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Leon".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Lille".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Lucca".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Lucerne".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Luxembourg".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Maceio".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Manzanillo".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Mazatlan".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Merida - Yucatan".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Montecatini".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Monterrey".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Murcia".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Natal".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Navarra".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Naxos".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Nha Trang - Dalat - Tuy Hoa".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Nottingham".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Nuremberg".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Padova".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Paros".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Pisa".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Reims".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Rotterdam".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Kota Kinabalu and Sabah".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Salamanca".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Salerno".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Salzburg".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Samos".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "San Jose / Central Valley".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Shenzhen".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Sierra Nevada".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Surabaya".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "The Hague".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Toledo".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Trabzon".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Valladolid".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Veracruz".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Vilnius".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Wroclaw".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Yogyakarta".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Zadar-North Dalmatia".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Zagreb".lower() and country == "United Kingdom".lower(): return "GBP", "UK"
        if area == "Northern Mountain Zone / Arenal".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Belo Horizonte".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Medellin".lower() and country == "UNITED STATES - USA".lower(): return "USD", "US"
        if area == "Macau".lower() and country == "United Kingdom".lower(): return "GBP", "UK"


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
        dest_code=html.fromstring(self._html).xpath(self.CONFIG_FILE.hotel_ZoneName)[0]
        dest_code=str(dest_code) + "_" + str(zone_index)
        # hotel_data = hotel.save_html(index,dest_code)
        return hotel.save_html(index,dest_code)

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
                if i == 100:
                    print('Crawled "%s" Hotels' % str(i))
                # for i, hotel_url in enumerate(self._hotels[hotels_count:hotels_count+2]):
                # i += hotels_count
                # time.sleep(1)
                # hotel = self._save_hotel(i, hotel_url)
                # crawled_hotels.append(hotel)
                try:
                    # if i in [1,34,19,38,20,41,29]:
                    #     raise self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']
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
                # if i > 100:
                #     break
            # if i > 100:
            #     break
        return self.request_data


# def crawl_hotels(consumer_data, redelivered):
#     return HotelbedsLandingPage(consumer_data).crawl_hotels(redelivered)


############test bed compatile###############
def crawl_hotels(consumer_data, redelivered):
    import time
    start_time = time.time()
    crawled_data = HotelbedsLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    return crawled_data





