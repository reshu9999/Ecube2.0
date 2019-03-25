import time
import json
import requests
import copy
from pdb import set_trace
from datetime import timedelta  
from lxml import etree, html
from copy import deepcopy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# from scripts import gta_config
# from scripts.core import exceptions
# from scripts.core.logs import CrawlingLogger
# from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler

from Crawling.scripts.Hotelbeds import ScrapperConfigGTACHAINPython
from Crawling.scripts.core import exceptions
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler


class GTALogger(CrawlingLogger):
    NAME = 'gta_crawling'


GTALogger.set_logger()
CrawlerBase.TRL = GTALogger
CrawlerBase.CONFIG_FILE = ScrapperConfigGTACHAINPython

class GTARequestHandler(RequestHandler):

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

            res_html = response.text
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj


class GTAHotel(HotelHandler):

    @property
    def _get_name(self):
        # hotelNameXpath
        with open('tmp.xml', 'w') as fo:
            fo.write(self._html['html_element'])

        with open('tmp.xml') as fo:
            pageHtml = etree.parse(fo)
        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()

    @property
    def _get_cache_page(self):
        return self._html['html_element']

    @property
    def _get_selling_page(self):
        city_code = self._landing_page.city_zone
        landing_page = self._landing_page.landing_pages.get(city_code, None)
        selling_price_html = landing_page['selling_price_page']
        # cost_price_html = landing_page['cost_price_page']

        return selling_price_html

    @property
    def _get_cost_page(self):
        city_code = self._landing_page.city_zone
        landing_page = self._landing_page.landing_pages.get(city_code, None)
        # selling_price_html = landing_page['selling_price_page']
        cost_price_html = landing_page['cost_price_page']

        return cost_price_html

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        city_code = self._landing_page.city_zone
        landing_page = self._landing_page.landing_pages.get(city_code, None)
        selling_price_html=landing_page['selling_price_page']
        cost_price_html=landing_page['cost_price_page']
        return {'landingPage': landing_page, 'hotelHtml': self._html,
                'hotel_element': etree.tostring(self._landing_page.hotel_elem).decode('utf-8')+selling_price_html}

    @property
    def _get_room_types(self):
        """
        :return: { 'roomtypehtml': 'page_source_of_roomtype',
                   'pricehtml': 'page_source_of_price_for_roomtype',
                   'boardTypeHTML': 'page_soource_of_promotion_for_boardtype',
                }
        """
        pageHtml = self._landing_page.hotel_elem
        room_dict = {
            'roomTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomDetailsInContainersXpath)[0]).decode('utf-8'),
            'priceHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.pricesInContainersXpath)[0]).decode('utf-8'),
            'boardTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomBoardType)[0]).decode('utf-8'),
            'paymentTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.paymentType)[0]).decode('utf-8'),
            'promotionTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.promotionType)[0]).decode('utf-8'),
        }

        return room_dict

    @property
    def _get_city_zone(self):
        return self._landing_page.city_zone

    @classmethod
    def complete_hotel_url(cls, hotel_url, domain):
        """
        :param: hotel_url as string
        :return: complete hotel url if partial
        """
        if not hotel_url.startswith(domain):
            hotel_url = '{0}{1}'.format(domain, hotel_url)
        return hotel_url

    @classmethod
    def get_hotel(cls, hotel_request, latitude_url, landing_page):
        hotel_url = cls.CONFIG_FILE.hotel_url
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers)

        hotel_url = cls.complete_hotel_url(hotel_url, landing_page.domain)

        resp_html, response, _ = GTARequestHandler.post_request_without_proxy(hotel_url, headers, body=hotel_request)
        html_elem = {'html_element': resp_html, 'latitude_html': cls._get_latitude(latitude_url, proxy, headers, cookie=cookie)}
        return cls(landing_page, html_elem)

    def save_html(self, index):
        hotel_data = dict()
        meta_data = dict()
        if self._landing_page.adults==2:
            adultvalue='2 Adt'
        # Crawler Output
        # Properties from Parent
        hotel_data['index'] = index
        hotel_data['hotel_count'] = self.hotel_count
        hotel_data['city'] = self.city
        hotel_data['country'] = self.country
        hotel_data['city_zone'] = self._get_city_zone
        hotel_data['checkIn'] = str(self.check_in)
        hotel_data['checkOut'] = str(self.check_out)
        hotel_data['POS'] = self._landing_page.pos
        hotel_data['nights'] = self._landing_page.nights
        hotel_data['adults'] = adultvalue
        # Crawler Output
        hotel_data['htmls'] = self._get_html
        hotel_data['selling'] = self._get_selling_page
        try:
            hotel_data['hotelName'] = self._get_name
        except Exception as e:
            raise self.EXCEPTIONS['HOTEL_NOT_FOUND'](str(e))
        hotel_data['roomTypes'] = self._get_room_types
        hotel_data['cachePageHTML'] = self._get_cost_page
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


        self.TRL.debug_log(
            'Saving Hotel:%s' % self._get_name, self._landing_page.request_id, self._landing_page.sub_request_id,
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers)
        hotel_data['meta']['sellingPageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_selling_page
        )
        # return self.SERVICE_CALLS['save_html'](hotel_data)

        response = copy.deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)


class GTARequestFactory(object):
    OBJ = None # object of GTALangindPage

    @classmethod
    def _get_source_elem(cls, count):
        source_elem = etree.Element('Source')
        requestor_id_elem = None
        if count == 0:
            requestor_id_elem = etree.Element('RequestorID', Client="45371", EMailAddress="XML@HOTELBEDS.COM", Password="HBGPRSEP17")
        else:
            requestor_id_elem = etree.Element('RequestorID', Client="45370", EMailAddress="XML@HOTELBEDS.COM", Password="HBGPRSEP17")

        requestor_pref = etree.Element("RequestorPreferences", Country=cls.OBJ._get_pos_country_code, Currency=cls.OBJ._get_currency, Language="en")
        request_mode = etree.Element('RequestMode')
        request_mode.text = 'SYNCHRONOUS'

        requestor_pref.append(request_mode)
        source_elem.append(requestor_id_elem)
        source_elem.append(requestor_pref)

        return source_elem
            
    @classmethod
    def _get_request_details(cls, city_zone):
        request_details = etree.Element('RequestDetails')
        search_hotel = etree.Element('SearchHotelPricePaxRequest')
        item_destination = etree.Element('ItemDestination', DestinationCode=city_zone, DestinationType='city')

        period_stay = etree.Element('PeriodOfStay')
        check_in = etree.Element('CheckInDate')
        check_in.text = cls.OBJ.check_in.strftime('%Y-%m-%d')
        duration = etree.Element('Duration')
        duration.text = str(cls.OBJ.nights)

        period_stay.append(check_in)
        period_stay.append(duration)

        price_break_down = etree.Element('IncludePriceBreakdown')
        charge_conditions = etree.Element('IncludeChargeConditions')
        opaque_cond = etree.Element('ShowPackageRates')
        pax_rooms = etree.Element('PaxRooms')
        pax_room = etree.Element('PaxRoom', Adults=str(cls.OBJ.adults), Cots='0', RoomIndex='1')

        pax_rooms.append(pax_room) 
        search_hotel.append(item_destination)    
        search_hotel.append(period_stay)
        search_hotel.append(price_break_down)
        search_hotel.append(charge_conditions)
        search_hotel.append(opaque_cond)
        search_hotel.append(pax_rooms)

        request_details.append(search_hotel)

        return request_details


    @classmethod
    def create_selling_request(cls):
        landing_page = dict()

        for city_code in cls.OBJ.city_zones:
            page_dict = dict()
            for i in range(2):
                root_elem = etree.Element('Request')
                source_elem = cls._get_source_elem(i)
                request_details = cls._get_request_details(city_code)
                root_elem.append(source_elem)
                root_elem.append(request_details)

                doc = etree.ElementTree(root_elem)
                body = etree.tostring(doc)
                url = CrawlerBase.CONFIG_FILE.request_listener_url
                res_xml, res_obj, _ = GTARequestHandler.post_request_without_proxy(url, headers=cls.OBJ._get_headers,  body=body)
                if i == 0:
                    page_dict['selling_price_page'] = res_xml
                else:
                    page_dict['cost_price_page'] = res_xml
            landing_page[city_code] = page_dict

        return landing_page

    @classmethod
    def _get_hotel_request(cls, hotel_code, city_zone):
        root_elem = etree.Element('Request')
        source_elem = cls._get_source_elem(0)
        request_details = etree.Element('RequestDetails')
        search_item = etree.Element('SearchItemInformationRequest', ItemType="hotel")
        item_destination = etree.Element('ItemDestination', DestinationType="city", DestinationCode=city_zone)
        item_code = etree.Element('ItemCode')
        item_code.text = hotel_code

        search_item.append(item_destination)
        search_item.append(item_code)
        request_details.append(search_item)
        
        root_elem.append(source_elem)
        root_elem.append(request_details)

        doc = etree.ElementTree(root_elem)
        hotel_doc = etree.tostring(doc)
        return hotel_doc

    @classmethod
    def _process_list(cls):
        hotel_lists = cls.create_selling_request()
        return hotel_lists

    @classmethod
    def _process_hotel(cls, hotel_code, city_code):
        return cls._get_hotel_request(hotel_code, city_code)



class GTALandingPage(HotelLandingPageHandler):
    HOST = 'https://rs.gta-travel.com/'
    PROXY_LESS_HIT = True

    HOTEL_HANDLER_CLASS = GTAHotel

    __slots__ = 'landing_pages'

    def __init__(self, request_data):
        self.city_zone = None
        self.city_zones = None
        self.landing_pages = None

        super().__init__(request_data)
        # parameter = self._get_url_params
        self.EXCEPTIONS.update({
            'INVALID_URL': exceptions.InvalidURL,
            'HOTEL_MATCHING_NOT_AVAILABLE': requests.exceptions.ConnectionError,
        })

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        hotel_elems = []
        cities = list(self.landing_pages.keys())
        for city_code in cities:
            each = self.landing_pages[city_code]['selling_price_page']
            with open('tmp.xml', 'w') as fo:
                fo.write(each)
            
            with open('tmp.xml') as fo:
                elem = etree.parse(fo)

            hotel = elem.xpath(CrawlerBase.CONFIG_FILE.hotelLinksXpath)
            hotel_elems.extend(hotel)

        self.hotel_count = len(hotel_elems)
        return hotel_elems

    @property
    def _get_currency(self):
        # if self.pos == "United Kingdom":
        #     return "GBP"
        # elif self.pos == "UNITED STATES - USA":
        #     return "USD"
        # elif self.pos == "Spain":
        #     return "EUR"
        # elif self.pos == "UAE":
        #     return "AED"
        # else:
        #     return "EUR"
        if (self.country).upper() == "TUNISIA" and (self.pos).upper() == "GERMANY":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "AUSTRALIA" and (self.pos).upper() == "AUSTRALIA":
            ReqCurrency = "AUD"
        elif (self.country).upper() == "AUSTRALIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "AUSTRIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "BAHRAIN" and (self.pos).upper() == "SAUDI ARABIA":
            ReqCurrency = "USD"
        elif (self.country).upper() == "BELGIUM" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "BELGIUM" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "CANADA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "CANADA" and (self.pos).upper() == "UNITED STATES - USA":
            ReqCurrency = "USD"
        elif (self.country).upper() == "CHINA" and (self.pos).upper() == "CHINA":
            ReqCurrency = "CNY"
        elif (self.country).upper() == "CHINA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "CROATIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "CZECH REPUBLIC" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "DENMARK" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "EGYPT" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "FRANCE" and (self.pos).upper() == "FRANCE":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "FRANCE" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "FRANCE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "GERMANY" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "GERMANY" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "GREECE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "HONG KONG" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "HUNGARY" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ICELAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "INDIA" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "INDIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "INDONESIA" and (self.pos).upper() == "AUSTRALIA":
            ReqCurrency = "USD"
        elif (self.country).upper() == "INDONESIA" and (self.pos).upper() == "INDONESIA":
            ReqCurrency = "USD"
        elif (self.country).upper() == "INDONESIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "IRELAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ISRAEL" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ITALY" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ITALY" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "JAPAN" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "KUWAIT" and (self.pos).upper() == "UNITED ARAB EMIRATES":
            ReqCurrency = "USD"
        elif (self.country).upper() == "LATVIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "LEBANON" and (self.pos).upper() == "UNITED ARAB EMIRATES":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "LITHUANIA" and (self.pos).upper() == "Russia":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "LUXEMBOURG" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MALAYSIA" and (self.pos).upper() == "INDONESIA":
            ReqCurrency = "USD"
        elif (self.country).upper() == "MALAYSIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MALDIVES" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MALTA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MAURITIUS ISLAND" and (self.pos).upper() == "FRANCE":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MAURITIUS ISLAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MOROCCO" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "NETHERLANDS" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "NETHERLANDS" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "NEW ZEALAND" and (self.pos).upper() == "AUSTRALIA":
            ReqCurrency = "AUD"
        elif (self.country).upper() == "NORWAY" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "OMAN" and (self.pos).upper() == "UNITED ARAB EMIRATES":
            ReqCurrency = "USD"
        elif (self.country).upper() == "PHILIPPINES" and (self.pos).upper() == "UNITED STATES - USA":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "POLAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "PORTUGAL" and (self.pos).upper() == "PORTUGAL":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "PORTUGAL" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "QATAR" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ROMANIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "RUSSIA" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "RUSSIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SAUDI ARABIA" and (self.pos).upper() == "UNITED ARAB EMIRATES":
            ReqCurrency = "USD"
        elif (self.country).upper() == "SINGAPORE" and (self.pos).upper() == "INDONESIA":
            ReqCurrency = "SGD"
        elif (self.country).upper() == "SINGAPORE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SOUTH AFRICA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SOUTH KOREA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SPAIN" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SPAIN" and (self.pos).upper() == "Spain":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SRI LANKA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SWEDEN" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SWEDEN" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SWITZERLAND" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SWITZERLAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "TAIWAN" and (self.pos).upper() == "HONG KONG":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "TAIWAN" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "THAILAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "TUNISIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "TURKEY" and (self.pos).upper() == "SPAIN":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "TURKEY" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "UKRAINE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "UNITED ARAB EMIRATES" and (self.pos).upper() == "SAUDI ARABIA":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "UNITED ARAB EMIRATES" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "UNITED KINGDOM" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "GBP"
        elif (self.country).upper() == "UNITED STATES - USA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "UNITED STATES - USA" and (self.pos).upper() == "Spain":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "UNITED STATES - USA" and (self.pos).upper() == "UNITED STATES - USA":
            ReqCurrency = "USD"
        elif (self.country).upper() == "VIETNAM" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "BRAZIL" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "BRL"
        elif (self.country).upper() == "COSTA RICA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "DOMINICAN REPUBLIC" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "MACAU" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "JORDAN" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MEXICO" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "BARBADOS" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.county).upper() == "CUBA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "JAMAICA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "ALGERIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "CAPE VERDE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "KENYA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "MOZAMBIQUE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SENEGAL" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SEYCHELLES ISLANDS" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "TANZANIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SLOVAKIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ANDORRA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "PUERTO RICO" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "ARGENTINA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "COLOMBIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "MONACO" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "CYPRUS" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "SERBIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "CHILE" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "PERU" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "URUGUAY" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "ARUBA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "BAHAMAS" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "PANAMA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "USD"
        elif (self.country).upper() == "BULGARIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "ESTONIA" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "FINLAND" and (self.pos).upper() == "UNITED KINGDOM":
            ReqCurrency = "EUR"
        elif (self.country).upper() == "LITHUANIA" and (self.pos).upper() == "Russia":
            ReqCurrency = "EUR"
        elif (self.country).upper()() == "TAIWAN" and (self.pos).upper() == "HONG KONG":
            ReqCurrency = "USD"
        return ReqCurrency


    @property
    def _get_pos_country_code(self):
        if self.pos == "United Kingdom":
            return "GB"
        elif self.pos == "UNITED STATES - USA":
            return "US"
        elif self.pos == "Spain":
            return "ES"
        elif self.pos == "UAE":
            return "AE"
        else:
            return "ES"


    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        if len(self.CONFIG_FILE.latLongXpath) == 0:
            raise exceptions.LatLongNotFountError
        return [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]

    @property
    def _get_url_params(self):
        """
        :return: dict of key value to be added in URL
        """
        # inDate = datetime.datetime.now() + datetime.timedelta(days=int(self.days))
        # inDate = inDate.strftime("%m/%d/%Y")
        # inSplit = str(inDate).split('/')
        # # inSplit = str(self.check_in).split('/')
        # inMonth, inDay, inYear = inSplit[0], inSplit[1], inSplit[2]

        checkOut = datetime.datetime.now() + datetime.timedelta(days=int(self.days) + int(self.nights))
        checkOut = checkOut.strftime("%m/%d/%Y")
        outSplit = str(checkOut).split('/')
        outMonth, outDay, outYear = outSplit[0], outSplit[1], outSplit[2]

        # sessionID = self._process_homepage()

        return {
            'iataNumber': '',
            'complexSearchField': self.city + '%2C+' + self.country,
            'searchType': 'location',
            'propertyIds': '',
            'arrivalDate': inMonth + '%2F' + inDay + '%2F' + inYear,
            'departureDate': outMonth + '%2F' + outDay + '%2F' + outYear,
            # 'numberOfRooms': self.room,
            'numberOfAdults': self.adults,
            'numberOfChildren': self.children,

        }

    def _get_host_url_for_url_maker(self, *args):
        """
        :params: args the page for which the request is made
                city_code, sid_query, hotel_list
        :return: url as string for the page requested
        """
        return GTALandingPage.HOST

    @property
    def _get_headers(self, ):
        """
        headers for making requests
        :return: var_headers
        """
        var_headers = {}
        var_headers[
            "Accept"] = "image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/xaml+xml, application/vnd.ms-xpsdocument, application/x-ms-xbap, application/x-ms-application, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-shockwave-flash, */*"
        var_headers["Accept-Language"] = "en-us"
        var_headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
        var_headers["Host"] = "rs.gta-travel.com"
        var_headers["Proxy-Connection"] = "Keep-Alive"
        var_headers["Content-Type"] = "application/xml"

        return var_headers

    def _set_headers(self, res_obj):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        pass

    def _set_cookie(self, resp_object):
        """
        :param cookie_object: either response or driver object to get cookie and set in self.cookie
        :return:
        """
        pass

    def _set_hotel_web_id(self, hotel_id):
        """
        set hotel web id
        :param: hotel_id
        :return: None
        """
        self.hotel_web_id = hotel_id

    def _set_city_zone(self, city_zone):
        self.city_zone = city_zone.upper()

    def _set_hotel_element(self, hotel_elem):
        self.hotel_elem = deepcopy(hotel_elem)

    def _get_hotel_list(self):
        # make_request_factory
        GTARequestFactory.OBJ = self
        hotel_list_dict = GTARequestFactory._process_list()
        return hotel_list_dict

    def _get_city_zone(self):
        try:
            # set_trace()
            #city_zone_text = "|Dubrovnik-South Dalmatia = (CATV^DBV)|Nantes = (CHOL^CLIA^NTE)|Zwolle = (ZWOL)|Aarhus = (AAR^HOLT^VIBO)"
            # city_zone_text = self.SERVICE_CALLS['get_city_zone']()
            url = "https://10.100.18.88/connector_files/GTA_Destination_mapping.html"
            # updated url here

            city_zone_text = requests.get(url, verify=False)
            city_zone_text = city_zone_text.text

            # city_zone_text = self.SERVICE_CALLS['get_city_matching_zone']()
            if isinstance(city_zone_text.split('|'), list):
                city_zone_text = city_zone_text[1:] if city_zone_text[0] == '|' else city_zone_text
                city_zone = dict()
                for i in city_zone_text.split('|'):
                    city, zone = i.split('=')
                    city = city.strip().lower()
                    zone = zone.strip().strip('(').strip(')').split('^')
                    city_zone[city.lower()] = zone
                return city_zone
            else:
                raise GTALandingPage.EXCEPTIONS['INVALID_URL']
        except GTALandingPage.EXCEPTIONS['INVALID_URL']:
            self.TRL.debug_log('Unable to find matching hotels', self.request_id, self.sub_request_id, self.request_run_id)
        except GTALandingPage.EXCEPTIONS['HOTEL_MATCHING_NOT_AVAILABLE']:
            self.TRL.debug_log('Matching Hotels Service Down', self.request_id, self.sub_request_id, self.request_run_id)

        return list()

    def _process_homepage(self):
        """
        method to process homepage, get cookies and make post
        form data call
        :return: None
        """
        # get matching hotel ids
        self.city=self.city.lower()
        self.city_zones = self._get_city_zone()[self.city]
        if self.pos == 'Afghanistan':
            self.pos = 'SPAIN'

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self.landing_pages = self._get_hotel_list()

    def _save_hotel(self, index, hotel_elem):
        hotel_elem = deepcopy(hotel_elem)
        latitude_url = None
        self.TRL.debug_log('Latitude and Longitude not found in URL', self.request_id, self.sub_request_id, self.request_run_id)

        hotel_code = hotel_elem.xpath(CrawlerBase.CONFIG_FILE.hotelCodeXpath)[0]
        city_code = hotel_elem.xpath(CrawlerBase.CONFIG_FILE.hotelCityCodeXpath)[0]

        self._set_hotel_web_id(hotel_code)
        self._set_city_zone(city_code)
        self._set_hotel_element(hotel_elem)

        GTARequestFactory.OBJ = self
        hotel_request = GTARequestFactory._process_hotel(hotel_code, city_code)

        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_code, self.request_id, self.sub_request_id, self.request_run_id)
        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(hotel_request, latitude_url, self)

        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        hotel_data = hotel.save_html(index)
        return hotel_data


def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    crawled_data = GTALandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    # file_distincter = time.time()
    # with open('crawled_data_%s.json' % file_distincter, 'w+') as file_obj:
    #     print("file_distincter")
    #     print(file_distincter)
    #     file_obj.write(json.dumps(crawled_data))
    return crawled_data




# def crawl_hotels(request_data):
#     return GTALandingPage(request_data).crawl_hotels()
import datetime

# sample = {
#     "requestId": "1",
#     "subRequestId": "2",
#     "requestRunId": "3",
#     "DomainName": "https://rs.gta-travel.com/",
#     "country": "CROATIA",
#     "RequestInputs": {
#         "city": "Dubrovnik-South Dalmatia",
#         "children": "0",
#         "adults": 2,
#         "room": 1,
#         "board": "",
#         "days":0 ,
#         "checkIn": datetime.datetime.now()+timedelta(days=7),
#         "checkOut": "",
#         "nights": 4,
#
#         "hotelName": "",
#         "fromAirport": "",
#         "toAirport": "",
#
#         "starRating": "",
#         "webSiteHotelId": "",
#         "pos": "United Kingdom",
#         "crawlMode": "",
#     },
# }
#
#
# hotels = crawl_hotels(sample,False)
# print('CRAWL COMPLETE')
# print(hotels)
# with open('gtacrawl.json','w')as file:
#     json.dump(hotels,file)
# with open('gtacrawl.json','r')as f:
#     hotels=json.load(f)
#
# from AetosParsingService.scripts import ParserGTAPython
# parsed_data = ParserGTAPython.crawl_hotels(hotels)
# # # for i in hotels:
# # #     obj = ParserGTAPython.crawl_hotels(i)
# # #
# # # with open('gta.json', 'w') as outfile:
# # #     json.dump(parsed_data, outfile,indent=4)
# with open('gta.json', 'w') as outfile:
#     json.dump(parsed_data, outfile)
#
