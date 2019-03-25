import datetime
import json
import requests
import pandas as pd
import math
from lxml import etree, html
from copy import deepcopy
from time import sleep

from Crawling.scripts.Hotelbeds_Availability import scrapper_ExpediaApp_config
from Crawling.scripts.core import exceptions
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, ProxyHandler, RequestHandler


class ExpediaAppLogger(CrawlingLogger):
    NAME = 'expediaApp_crawling'


ExpediaAppLogger.set_logger()
CrawlerBase.TRL = ExpediaAppLogger
CrawlerBase.CONFIG_FILE = scrapper_ExpediaApp_config

class ExpediaAppHotel(HotelHandler):

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        return eval(self._html['html_element'])[0].strip()

    @property
    def _get_cache_page(self):
        return str(self._get_html['landingPage'])

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': self._landing_page._html}

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """

        roomType = self._html['html_element']
        price = None
        return {'roomTypeHTML': roomType, 'priceHTML':price}

    @classmethod
    def get_hotel(cls, hotel_url, latitude_url, landing_page):
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url[7], landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers)

        # from pdb import set_trace; set_trace()
        resp_html, response, _ = '','',''
        html_elem = {'html_element': str(hotel_url), 'latitude_html': ''}
        return cls(landing_page, html_elem)

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
        hotel_data['adults'] = str(self._landing_page.adults)
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
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers)
        hotel_data['meta']['cachePageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cache_page
        )

        self.TRL.debug_log('Hotel Data:%s' % hotel_data)
        print('hotel data: ', hotel_data)
        response = deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)


class ExpediaAppLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.expedia.co.in/'
    HOTEL_HANDLER_CLASS = ExpediaAppHotel
    HOTEL_LIST_DRIVER = True
    PROXY_PAGE_WISE = True

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        all_hotels = []
        for batch in self._html['resp_all_pages']:
            for hotel in batch['hotelList']:
                name = hotel['name']
                roomtype = 'RO'
                type = 'Twin'

                try:
                    price = hotel['lowRateInfo']['priceToShowUsers']
                    price = round(float(price) * self._html['exchange_rate'], 2)
                except:
                    continue

                base_currency, target_currency = self._get_currencies
                star = hotel['hotelStarRatingCssClassName']
                id = hotel['hotelId']
                url = "https://www.expedia.co.in/m/api/hotel/offers/v3?&checkInDate={0}&checkOutDate={1}&room1={2}&hotelId={3}&shopWithPoints=false&sourceType=mobileapp" \
                "&langid=2057 HTTP/1.1".format(self.check_in,self.check_out,self.adults,id)

                all_hotels.append([name, roomtype, type, price, target_currency, star, id, url])
        self.hotel_count = len(all_hotels)
        return all_hotels

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        pass

    @property
    def _get_url_params(self):
        """
        :return: dict of key value to be added in URL
        """

        self.check_in = self.check_in + datetime.timedelta(days=int(self.days))
        self.check_out = self.check_in + datetime.timedelta(days=int(self.nights))
        check_in = self.check_in.date()
        check_out = self.check_out.date()
        region_id, lat, long = self._process_homepage()
        return {
            'pageIndex': '{}',
            'filterUnavailable': 'false',
            'regionId': '{}'.format(region_id),
            'latitude': '{}'.format(lat),
            'longitude': '{}'.format(long),
            'checkInDate': check_in,
            'checkOutDate': check_out,
            'room1': self.adults,
            'shopWithPoints': 'false',
            'sortOrder':'ExpertPicks',
            'enableSponsoredListings':'true',
            'sourceType':'mobileapp',
            'langid':'2057%20HTTP/1.1'
        }

    def _url_maker(self):
        self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id, self.request_run_id)
        self.TRL.debug_log('Params:%s' % self._get_url_params, self.request_id, self.sub_request_id, self.request_run_id)

        return "".join([self.get_domain + '/m/api/hotel/search/v3?resultsPerPage=200'] +
                       ['&%s=%s' % (i, p) for i, p in self._get_url_params.items()])

    @property
    def get_domain(self):
        if self.pos.lower() == 'us' or self.pos.lower() == 'united states' or self.pos.lower() == 'unitedstates':
            domain = 'https://www.expedia.com'
        elif self.pos.lower() == 'uk' or self.pos.lower() == 'united kingdom' or self.pos.lower() == 'unitedkingdom':
            domain = 'https://www.expedia.co.uk'
        elif self.pos.lower() == 'France'.lower() or self.pos.lower() == 'france'.lower() or self.pos.lower() == 'fr':
            domain = 'https://www.expedia.fr'
        elif self.pos.lower() == 'Spain'.lower() or self.pos.lower() == 'spain'.lower() or self.pos.lower() == 'es':
            domain = 'https://www.expedia.es'
        elif self.pos.lower() == 'Australia'.lower() or self.pos.lower() == 'au':
            domain = 'https://www.expedia.com.au'
        elif self.pos.lower() == 'Mexico'.lower() or self.pos.lower() == 'mx':
            domain = 'https://www.expedia.mx'
        elif self.pos.lower() == 'Hongkong'.lower() or self.pos.lower() == 'hk':
            domain = 'https://www.expedia.com.hk'
        elif self.pos.lower() == 'germany' or self.pos.lower() == 'de':
            domain = 'https://www.expedia.de'
        return domain

    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        # from pdb import set_trace; set_trace()
        pass

    def _process_homepage(self):
        flag = True
        counter = 0
        lat_long_headers = {
            "Accept": "application/json",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        lat_long_headers = {'Accept':'application/json',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-US,en;q=0.5',
         'Connection':'keep-alive',
         'Cookie':'linfo=v.4,|0|0|255|1|0||||||||…0-3a16-47ed-bec0-62db3fdc0249',
         'Host':'suggest.expedia.com',
         'Upgrade-Insecure-Requests':'1',
         'User-Agent':'"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"'}
        lat_long_url = "https://suggest.expedia.com/api/v4/typeahead/{0}?regiontype=511&dest=false&features=ta_hierarchy&lob=HOTELS&sourceType=mobileapp&langid=2057&device=mobile&locale=en_IN&siteid=27&client=expedia.app.android.phone HTTP/1.1".format(
            self.city)
        try:
            # res_html, lat_long_resp, driver_obj = self.get_request(lat_long_url, headers=lat_long_headers, proxy=self.proxy)
            res_html, lat_long_resp, driver_obj = self.get_headerless_request(lat_long_url, proxy=self.proxy)
        except:
            while flag and counter < 5:
                try:
                    self.proxy.initiate_new_proxy()
                    res_html, lat_long_resp, driver_obj = self.get_request(lat_long_url, headers=lat_long_headers,
                                                                   proxy=self.proxy)
                    flag = False
                except:
                    flag = True
                    counter += 1

        region_id, lat, long = None, None, None
        if lat_long_resp.status_code == 200:
            # lat_long_json_resp = lat_long_resp.json()
            lat_long_json_resp = eval(lat_long_resp.text[1:-1])
            for result in lat_long_json_resp['sr']:
                if self.country.lower() == 'united states - usa':
                    country = 'United States of America'
                elif self.country.lower() == 'united kingdom' or self.country.lower() == 'uk':
                    country = 'United Kingdom'
                elif self.country.lower() == 'saudi arabia' or self.country.lower() == 'saudi arab':
                    country = 'Saudi Arabia'
                else:
                    country = self.country.capitalize()
                if country in result['hierarchyInfo']['country']['name']:  # ['regionNames']['displayName']:
                    region_id = result['gaiaId']
                    lat, long = result['coordinates']['lat'], result['coordinates']['long']
                    break
        return region_id,lat,long

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
            # self.proxy.check_proxy(link.format(0), self.headers)
            print('Here')
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

        base_currency, target_currency = self._get_currencies
        er_url = "https://www.calculator.net/currency-calculator.html?eamount=1&efrom={}&eto={}&ccmajorccsettingbox=1&type=1&x=53&y=19".format(
            base_currency, target_currency)
        resp_obj_er = requests.get(er_url, self._get_exchange_rate_headers, proxies=self.proxy.to_python('http'),
                                                  allow_redirects=False)
        exchange_rate = float(html.fromstring(resp_obj_er.text).xpath('//*[@class="verybigtext"]/font[1]/b/text()')[0])


        resp, resp_obj, _ = self.get_request(link.format(0), self.headers, self.proxy, driver=self.HOTEL_LIST_DRIVER)
        try:
            total_hotels = resp_obj.json()['totalHotelCount']
        except:
            sleep(3)
            resp, resp_obj, _ = self.get_request(link.format(0), self.headers, self.proxy,
                                                 driver=self.HOTEL_LIST_DRIVER)
            total_hotels = resp_obj.json()['totalHotelCount']
        pages = float(total_hotels) / float(200)
        pages = math.ceil(pages)
        resp_all_pages = []
        for i in range(1, pages+1):
            # hotel_ids_list = [(hotel['hotelId'], hotel['name']) for hotel in eval(resp)['hotelList']]
            resp_all_pages.append(resp_obj.json())
            resp, resp_obj, _ = self.get_request(link.format(i), self.headers, self.proxy, driver=self.HOTEL_LIST_DRIVER)

        self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
        request_type = RequestHandler._get_request_type()
        if request_type['driver']:
            self._set_cookie(_)
        else:
            self._set_cookie(resp_obj)
        self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return {'resp_all_pages': resp_all_pages, 'exchange_rate' : exchange_rate}

    def crawl_hotels(self, redelivered):
        redelivered = False
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

        self.TRL.debug_log('Hotels Found:%s' % len(self._hotels), self.request_id, self.sub_request_id,
                           self.request_run_id)
        crawled_hotels = partial_hotels
        hotels_count = len(crawled_hotels)
        if self.PROXY_PAGE_WISE:
            self.proxy.initiate_new_proxy(page_type='List')
        for i, hotel_url in enumerate(self._hotels):
            # for i, hotel_url in enumerate(self._hotels[:5]):
            try:
                # if i in [3]:
                #     raise self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']
                self._save_hotel(i, hotel_url)
                crawled_hotels.append(i)
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
        return self.request_data

    @property
    def _get_currencies(self):
        domain = self.get_domain
        if domain == 'https://www.expedia.com': base_currency = 'USD'
        elif domain == 'https://www.expedia.co.uk': base_currency = 'GBP'
        elif domain == 'https://www.expedia.fr': base_currency = 'EUR'
        elif domain == 'https://www.expedia.es': base_currency = 'EUR'
        elif domain == 'https://www.expedia.com.au': base_currency ='AUD'
        elif domain == 'https://www.expedia.mx': base_currency = 'MXN'
        elif domain == 'https://www.expedia.com.hk': base_currency = 'HKD'
        elif domain == 'https://www.expedia.de': base_currency = 'EUR'

        if self.city.lower() == "doha" and self.pos.lower() == "united kingdom": target_currency = "QAR"
        elif self.city.lower() == "chicago - il" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "new york area - ny" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "orlando area - fl" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "miami area - fl" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "las vegas - nv" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "los angeles - ca" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "san diego - ca" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "san francisco area - ca" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "krabi" and self.pos.lower() == "united kingdom": target_currency = "THB"
        elif self.city.lower() == "boston - ma" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "new orleans - la" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "washington d.c. - dc" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "fort lauderdale - hollywood area - fl" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "hawaii - oahu - hi" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "nice" and self.pos.lower() == "united kingdom": target_currency = "EUR"
        elif self.city.lower() == "hawaii - maui - hi" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "atlanta - ga" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "california coast - ca" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "dallas - tx" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "gauteng- johannesburg" and self.pos.lower() == "united kingdom": target_currency = "ZAR"
        elif self.city.lower() == "houston - tx" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "phoenix area - az" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "san antonio - tx" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "seattle - wa" and self.pos.lower() == "united kingdom": target_currency = "USD"
        elif self.city.lower() == "almeria coast-almeria" and self.pos.lower() == "spain": target_currency = "EUR"

        return base_currency, target_currency

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = self._get_hotel_list()

    @property
    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    # 'Cookie': 'linfo=v.4,|0|0|255|1|0||||||||…0-3a16-47ed-bec0-62db3fdc0249',
                    'Host': "{}".format(self.get_domain[8:]),
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': ''}
        # headers = {
        # "Accept": "application/json",
        # "Host": "{}".format(self.get_domain[8:]),
        # "Connection": "Keep-Alive",
        # "Accept-Encoding": "gzip"
        # }
        return headers

    @property
    def _get_exchange_rate_headers(self):
        headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.9",
                   "Connection": "close",
                   "Host": "www.exchange-rates.org",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        return headers

    def _save_hotel(self, index, hotel_url):
        try:
            latitude_url = ''
        except exceptions.LatLongNotFountError:
            self.TRL.debug_log('Latitude and Longitude not found in URL', self.request_id, self.sub_request_id, self.request_run_id)
            latitude_url = None

        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url[7], self.request_id, self.sub_request_id, self.request_run_id)

        if self.hotels_id_dict is not None:
            self._set_hotel_web_id(self.hotels_id_dict[index])

        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(hotel_url, latitude_url, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        return hotel.save_html(index)

def crawl_hotels(consumer_data, redelivered):

    import time
    print('starting crawl')
    start_time = time.time()
    crawled_data = ExpediaAppLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    return crawled_data


# def crawl_hotels(self, redelivered):
#         redelivered = False
#         partial_hotels = list()
#         if redelivered:
#             partial_hotels = self.SERVICE_CALLS['get_partial_hotels'](self.sub_request_id)
#             print('crawled_hotels found')
#             print(len(partial_hotels))
#
#         self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
#         try:
#             self._set_html()
#         except (
#             requests.exceptions.ReadTimeout,
#             requests.exceptions.ProxyError
#         ) as e:
#             raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
#
#         self.TRL.debug_log('Hotels Found:%s' % len(self._hotels), self.request_id, self.sub_request_id, self.request_run_id)
#         crawled_hotels = partial_hotels
#         hotels_count = len(crawled_hotels)
#         for i, hotel_url in enumerate(self._hotels):
#         # for i, hotel_url in enumerate(self._hotels[hotels_count:hotels_count+2]):
#         #     i += hotels_count
#             # time.sleep(1)
#             # self._save_hotel(i, hotel_url)
#             # crawled_hotels.append(hotel)
#             try:
#                 self._save_hotel(i, hotel_url)
#                 crawled_hotels.append(i)
#             except (
#                 requests.exceptions.ReadTimeout,
#                 requests.exceptions.ProxyError
#             ) as e:
#                 self.request_data.update({'hotels': crawled_hotels})
#                 self.SERVICE_CALLS['save_partial_hotels'](self.request_data, str(e))
#                 raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
#             except self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']:
#                 pass
#         self.request_data.update({'hotels': crawled_hotels})
#         return self.request_data
#


# sample = {
#     "requestId": "12",
#     "subRequestId": "1",
#     "requestRunId": "",
#     "DomainName": "https://www.expedia.co.in/",
#     "country": "France",
#     "RequestInputs": {
#         "city": "Paris",
#         "children": "",
#         'fromAirport':'',
#         'toAirport':'',
#         'children_age':'',
#         "adults": 2,
#         "room": 1,
#         "board": "",
#         "checkIn": datetime.datetime.now(),
#         "checkOut": "",
#         "nights": 3,
#         "days": 7,
#         "hotelName": "",
#         "starRating": "",
#         "webSiteHotelId": "",
#         "pos": "",
#         "crawlMode": ""
#     }
# }
#
#
# hotels = crawl_hotels(sample, False)
#
# from AetosParsingService.scripts import ParserExpediaAppPython
# parsed_data = ParserExpediaAppPython.crawl_hotels(hotels)


# for h in hotels:
#
#     obj = ParserStarwoodPython.crawl_hotels(h)
#     print(obj)
