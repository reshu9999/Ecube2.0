import time
import json
import requests

from lxml import etree, html
from copy import deepcopy
from Queues.ScraperQueue import gta_config
from Queues.ScraperQueue.core import exceptions
from Queues.ScraperQueue.core.logs import CrawlingLogger
from Queues.ScraperQueue.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler


class GTALogger(CrawlingLogger):
    NAME = 'gta_crawling'


GTALogger.set_logger()
CrawlerBase.TRL = GTALogger
CrawlerBase.CONFIG_FILE = gta_config


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
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        city_code = self._landing_page.city_zone
        landing_page = self._landing_page.landing_pages.get(city_code, None)
        return {'landingPage': landing_page, 'hotelHtml': self._html,
                'hotel_element': etree.tostring(self._landing_page.hotel_elem).decode('utf-8')}

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

        resp_html, response, _ = cls.post_request(hotel_url, headers, proxy, body=hotel_request)
        html_elem = {'html_element': resp_html, 'latitude_html': cls._get_latitude(latitude_url, proxy, headers, cookie=cookie)}
        return cls(landing_page, html_elem)


class GTARequestFactory(object):
    OBJ = None # object of GTALangindPage

    @classmethod
    def _get_source_elem(cls, count):
        source_elem = etree.Element('Source')
        requestor_id_elem = None
        if count == 0:
            requestor_id_elem = etree.Element('RequestorID', Client="45120", EMailAddress="XML@HOTELBEDS.COM", Password="HBGPRSEP17")
        else:
            requestor_id_elem = etree.Element('RequestorID', Client="45073", EMailAddress="XML@HOTELBEDS.COM", Password="HBGPRSEP17")

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
        pax_rooms = etree.Element('PaxRooms')
        pax_room = etree.Element('PaxRoom', Adults=str(cls.OBJ.adults), Cots='0', RoomIndex='1')

        pax_rooms.append(pax_room) 
        search_hotel.append(item_destination)    
        search_hotel.append(period_stay)
        search_hotel.append(price_break_down)
        search_hotel.append(charge_conditions)
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
                res_xml, res_obj, _ = cls.OBJ.post_request(url, headers=cls.OBJ._get_headers, proxy=cls.OBJ.proxy, body=body)
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

    HOTEL_HANDLER_CLASS = GTAHotel

    __slots__ = 'landing_pages'

    def __init__(self, request_data):
        self.city_zone = None
        self.city_zones = None
        self.landing_pages = None
        super().__init__(request_data)
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

        return hotel_elems

    @property
    def _get_currency(self):
        if self.pos == "United Kingdom":
            return "GBP"
        elif self.pos == "UNITED STATES - USA":
            return "USD"
        elif self.pos == "Spain":
            return "EUR"
        elif self.pos == "UAE":
            return "AED"
        else:
            return "EUR"

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
            # city_zone_text = "|Nantes = (CHOL^CLIA^NTE)|Zwolle = (ZWOL)"
            city_zone_text = self.SERVICE_CALLS['get_city_zone']()

            # city_zone_text = self.SERVICE_CALLS['get_city_matching_zone']()
            if isinstance(city_zone_text.split('|'), list):
                city_zone_text = city_zone_text[1:] if city_zone_text[0] == '|' else city_zone_text
                city_zone = dict()
                for i in city_zone_text.split('|'):
                    city, zone = i.split('=')
                    city = city.strip()
                    zone = zone.strip().strip('(').strip(')').split('^')
                    city_zone[city] = zone
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


"""
def crawl_hotels(request_data):
    return GTALandingPage(request_data).crawl_hotels()

import datetime

sample = {
    "requestId": "1",
    "subRequestId": "2",
    "requestRunId": "3",
    "domainName": "https://rs.gta-travel.com/",
    "country": "France",
    "RequestInputs": {
        "city": "Nantes",
        "children": "0",
        "adults": 2,
        "room": 1,
        "board": "",
        "checkIn": datetime.datetime.strptime('2018-08-08', '%Y-%m-%d'),
        "checkOut": datetime.datetime.strptime('2018-08-08', '%Y-%m-%d') + datetime.timedelta(days=1),
        "nights": 1,
        "days": 2,
        "hotelName": "",
        "starRating": "",
        "webSiteHotelId": "",
        "pos": "Spain",
        "crawlMode": "",
    },
}


hotels = crawl_hotels(sample)
print('CRAWL COMPLETE')

from param_parser import ParserGTAPython

for i in hotels:
    obj = ParserGTAPython.crawl_hotels(i) 
"""

