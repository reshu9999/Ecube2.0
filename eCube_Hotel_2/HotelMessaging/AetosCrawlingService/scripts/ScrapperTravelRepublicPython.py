import time
import json
import requests
import pandas as pd

from lxml import etree, html
from copy import deepcopy
from scripts import travel_republic_config
from scripts.core import exceptions
from scripts.core.logs import CrawlingLogger
from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler
from scripts.travel_republic_travellers import travellers_data_dict, city_multi_code, city_mapping, currency


class TravelRepublicLogger(CrawlingLogger):
    NAME = 'travel_republic_crawling'


TravelRepublicLogger.set_logger()
CrawlerBase.TRL = TravelRepublicLogger
CrawlerBase.CONFIG_FILE = travel_republic_config


class TravelRepublicHotel(HotelHandler):

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        pageHtml = html.fromstring(self._html['html_element'])

        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()

    @property
    def _get_cache_page(self):
        return self._html['html_element']

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'hotelHTML': self._html}
        # return {'landingPage': self._landing_page._html, 'hotelHTML': self._html}

    @property
    def _get_room_types(self):
        """
        :return: { 'roomtypehtml': 'page_source_of_roomtype',
                   'pricehtml': 'page_source_of_price_for_roomtype',
                   'boardTypeHTML': 'page_soource_of_promotion_for_boardtype',
                }
        """
        pageHtml = html.fromstring(self._html['html_element'])
        if 'supplier_page' in self._html.keys():
            room_dict = {
                'roomTypeHTML': etree.tostring(deepcopy(pageHtml.xpath(self.CONFIG_FILE.matchHotelRoomDetailsInContainersXpath)[0])).decode('utf-8'),
                'priceHTML': etree.tostring(deepcopy(pageHtml.xpath(self.CONFIG_FILE.matchHotelPricesInContainersXpath)[0])).decode('utf-8'),
                'boardTypeHTML': etree.tostring(deepcopy(pageHtml.xpath(self.CONFIG_FILE.matchHotelRoomBoardType)[0])).decode('utf-8'),
                'paymentTypeHTML': etree.tostring(deepcopy(pageHtml.xpath(self.CONFIG_FILE.matchHotelRoomPaymentType)[0])).decode('utf-8'),
                'promotionTypeHTML': etree.tostring(deepcopy(pageHtml.xpath(self.CONFIG_FILE.matchHotelRoomPromotionType)[0])).decode('utf-8'),
            }
        else:
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


class TravelRepublicHomePage():
    HOME_PAGE = None  # object of TravelRepublicLandingPage

    @classmethod
    def _get_post_params(cls, query_name, *args, **kwargs):
        """
        :return: dict of key value to be sent in post body
        """
        post_data_dict = {}
        post_data_dict['cityname'] = kwargs['t']
        post_data_dict['countryId'] = kwargs['v']['c']
        post_data_dict['provinceId'] = kwargs['v']['p']
        post_data_dict['locationId'] = kwargs['v']['l']
        post_data_dict['placeId'] = kwargs['v']['pl']
        post_data_dict['estabId'] = kwargs['v']['e']
        post_data_dict['polygonId'] = kwargs['v']['po']
        post_data_dict['checkInDate'] = cls.HOME_PAGE.check_in.strftime('%Y-%m-%d')
        post_data_dict['checkOutDate'] = cls.HOME_PAGE.check_out.strftime('%Y-%m-%d')
        post_data_dict['currencyCode'] = "GBP" if cls.HOME_PAGE.pos == 'United Kingdom' else 'EUR'
        post_data_dict['roomsRequired'] = "1"
        travellers = int(cls.HOME_PAGE.adults) + int(cls.HOME_PAGE.children)
        post_data_dict['rooms'] = [travellers_data_dict[travellers]]
        post_data_dict['hotelearchSubType'] = 1
        post_data_dict['sid'] = "00000000-0000-0000-0000-000000000000"
        post_data_dict['estabTitle'] = ""
        post_data_dict['regionTitle'] = args[0].upper()
        post_data_dict['filterId'] = 0
        post_data_dict['isFlightPlus'] = False
        post_data_dict['isAgentMode'] = False

        return post_data_dict

    @classmethod
    def _get_host_url_for(cls, *args):
        """
        :params: args the page for which the request is made
                city_code, sid_query, hotel_list
        :return: url as string for the page requested
        """
        url_list = [
            lambda: '{0}services/autocompleter.svc/GetHotelDestinations?localeId=10&term={1}&maximumStringDistance=4&maximumResults=15&_=' if args[0] == 'city_code' else None,

            lambda: '{0}include/handlers/HotelSearch.ashx?nc=14820' if args[0] == 'form_page' else None,
        ]

        for each in url_list:
            if each() is not None:
                return each()
        return TravelRepublicLandingPage.HOST

    @classmethod
    def _process_form_data(cls, page_name, *args, **kwargs):
        """
        method to process form data for travellers details
        :return: None
        """
        city_name = args[0]

        if city_name.upper() == "Rome (Province), Italy":
            city_name = "Rome Province, Italy"
        elif city_name.upper() == "LONDON, UNITED KINGDOM":
            city_name = "London United Kingdom"
        elif city_name.upper() == "GATWICK+AIRPORT+(LGW)%2C+LONDON%2C+UNITED+KINGDOM":
            city_name = "Gatwick Airport LGW, West Sussex, United Kingdom"
        elif city_name.upper() == "STANSTED+AIRPORT+STN%2C+HERTFORDSHIRE%2C+UNITED+KINGDOM":
            city_name = "Stansted Airport STN, Hertfordshire, United Kingdom"

        url = cls._get_host_url_for(page_name).format(TravelRepublicLandingPage.HOST)
        body = cls._get_post_params(page_name, city_name, **kwargs)
        res_html, res_obj, driver_obj = cls.HOME_PAGE.post_request(url, body=body, 
                                                    body_type='json', headers=cls.HOME_PAGE._get_json_headers, proxy=cls.HOME_PAGE.proxy)
        return res_html, res_obj, driver_obj

    @classmethod
    def _get_city_code(cls, city):
        """
        make city based calls for processing hotel list query
        :return: get response from the city_code_url
                res_html,res_obj, driver_obj
        """
        if not isinstance(city, dict):
            city = {1: city}

        for each in city.values():
            tmp_city = each.replace(' ', '%20')
            tmp_city = tmp_city.replace("'", '%27')
            tmp_city = tmp_city.replace('ô', '')
            tmp_city = tmp_city.replace('í', '')

            if each.upper() == 'GATWICK AIRPORT (LGW), LONDON, UNITED KINGDOM':
                each = 'GATWICK+AIRPORT+(LGW)%2C+LONDON%2C+UNITED+KINGDOM'
            elif each.upper() == 'STANSTED AIRPORT (STN), LONDON, UNITED KINGDOM':
                each = 'STANSTED AIRPORT (STN), LONDON, UNITED KINGDOM'

            city_code_url = cls._get_host_url_for('city_code').format(TravelRepublicLandingPage.HOST, each.upper())

            res_html, res_obj, driver_obj = cls.HOME_PAGE.get_request(city_code_url,
                                                                      headers=cls.HOME_PAGE._get_json_headers,
                                                                      proxy=cls.HOME_PAGE.proxy)
            res_out = json.loads(res_html)
            if res_out["s"] == True:
                city_name = each
                return res_html, res_obj, driver_obj, city_name

    @classmethod
    def _process(cls, landing_page):
        # process url for city code
        city = city_mapping[landing_page.city.upper()]
        res_html, res_obj, driver_obj, city_name = cls._get_city_code(city)
        cls.HOME_PAGE._set_city_zone(city_name)
        code_dict = json.loads(res_html)

        # get request sid
        for each in code_dict["d"]:
            if each["t"].startswith(cls.HOME_PAGE.city):
                city_codes = each
                res_html, res_obj, driver_obj = cls._process_form_data("form_page", city_name, **city_codes)
                return res_html, res_obj, driver_obj


class TravelRepublicSupplierDetail(object):
    OBJ = None

    @classmethod
    def _get_host_url_for(cls, *args):
        """
        :params: args the page for which the request is made
                city_code, sid_query, hotel_list
        :return: url as string for the page requested
        """
        url_list = [
            lambda: '{0}hotels/hotel-details.aspx?sid={1}&estabid={2}&rooms={3}' if args[0] == 'rooms' else None,
            lambda: '{0}/include/controls/transactional/ajax/gethoteldetails.aspx?bookingId={1}&searchId={2}&estabId={3}&roomIds={4}&selectedBags=0&locationId=&_=' if args[0] == 'hotel_data' else None,
        ]

        for each in url_list:
            if each() is not None:
                return each()

        return TravelRepublicLandingPage.HOST

    @classmethod
    def get_hotel_room_detail(cls, room_row_attribs):
        room_url = cls._get_host_url_for('rooms')
        room_url = room_url.format(TravelRepublicLandingPage.HOST, room_row_attribs['data-search'],
                room_row_attribs['data-estab'], room_row_attribs['data-id'])

        var_headers = {
            "Accept": "image/jpeg, image/gif, image/pjpeg, application/vnd.ms-excel, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*",
            "Accept-Language": "en-us",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322)",
            "Host": "www.travelrepublic.es",
            "Proxy-Connection": "Keep-Alive",
        }

        res_html, res_obj, _ = cls.OBJ.get_headerless_request(room_url, proxy=cls.OBJ.proxy)
        # res_html, res_obj, _ = cls.OBJ.get_request(room_url, headers=var_headers, proxy=cls.OBJ.proxy)

        def get_hotel_details(response_html, room_row_attribs):
            hotel_attrib_str = response_html[response_html.find('HotelDetails('):response_html.find('}',
                                                                                                    response_html.find(
                                                                                                        'HotelDetails(') + 1) + 1].strip(
                'HotelDetails(')
            hotel_attribs = json.loads(hotel_attrib_str)
            hotel_url = cls._get_host_url_for('hotel_data')
            hotel_url = hotel_url.format(TravelRepublicLandingPage.HOST,
                                         hotel_attribs['bookingId'],
                                         hotel_attribs['searchId'],
                                         room_row_attribs['data-estab'],
                                         room_row_attribs['data-id'])
            hotel_headers = {
                "Accept": "*/*",
                "Accept-Language": "en-us",
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",
                "Host": "www.travelrepublic.es",
                "Referer": room_url,
                "x-requested-with": "XMLHttpRequest",
                "Connection": "Keep-Alive",
            }

            res_html, res_obj, _ = cls.OBJ.get_request(hotel_url, headers=hotel_headers, proxy=cls.OBJ.proxy)

            return hotel_attribs, hotel_url

        # from pdb import set_trace; set_trace()
        hotel_attribs, hotel_url = get_hotel_details(res_html, room_row_attribs)
        return room_url, hotel_url, hotel_attribs

    @classmethod
    def get_supplier_detail(cls, room_url, booking_id):
        postroom = "book=1&bid={0}&translatedInfo=".format(booking_id)
        var_headers = {
            "Accept": "image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, application/vnd.ms-excel, application/msword, */*",
            "Accept-Language": "en-us",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322)",
            "Host": "www.travelrepublic.co.uk",
            "Referer": room_url,
            "Content-Type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
            "Proxy-Connection": "Keep-Alive",
        }

        res_html, res_obj, _ = cls.OBJ.post_request(room_url, body=postroom, body_type='url_string', headers=var_headers, proxy=cls.OBJ.proxy)

        supplier_url = "https://www.travelrepublic.co.uk/services/booking/webclient.svc/GetBasketDetails?basketId={0}&_=1438770764390".format(booking_id)

        res_html, res_obj, _ = cls.OBJ.get_request(supplier_url,
                                            headers=cls.OBJ._get_json_headers,
                                            proxy=cls.OBJ.proxy)
        return res_html, res_obj

    @classmethod
    def _process(cls, hotel_data):
        page_html = html.document_fromstring(hotel_data._html['html_element'])
        room_row = page_html.xpath('//table//tr[contains(@class, "room-row roomRow roomSelector")]')[0]
        room_row_attribs = room_row.attrib
        room_url, hotel_url, hotel_attribs = cls.get_hotel_room_detail(room_row_attribs)

        res_html, res_obj = cls.get_supplier_detail(room_url, hotel_attribs['bookingId'])

        return res_html, res_obj


class TravelRepublicLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.travelrepublic.co.uk/'
    HOTEL_HANDLER_CLASS = TravelRepublicHotel
    HOTEL_LIST_DRIVER = False

    def __init__(self, request_data):
        self.city_zone = None
        super().__init__(request_data)
        self.EXCEPTIONS.update({
            'HOTEL_MATCHING_NOT_AVAILABLE': requests.exceptions.ConnectionError,
        })

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        url_string = self._get_host_url_for_url_maker('hotel_data')
        hotels = self._html['searchData']['hotels']
        hotel_urls = []
        hotel_id_lst = []
        for each in hotels:
            hotel_id = each['id']
            hotel_urls.append(url_string.format(TravelRepublicLandingPage.HOST, hotel_id, self.sid))
            hotel_id_lst.append(hotel_id)
        else:
            # for fetching hotel id to process room details
            self.hotels_id_dict = dict(enumerate(hotel_id_lst))
        self.hotel_count = len(hotel_urls)

        return hotel_urls

    @property
    def _get_hotel_count(self):
        return len(self._html['searchData']['hotels'])

    @property
    def _get_currency(self):
        return "EUR"

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
        url_list = [
            lambda: '{0}hotels/availability/HotelAvailabilityOptions.ashx?nc=57612&sid={1}&isHoliday=false&_=1440163620317' if
            args[0] == 'hotel_list' else None,

            lambda: '{0}hotels/hotel-availability-details.aspx?id={1}&sid={2}' if args[0] == 'hotel_data' else None,

            lambda: '{0}include/controls/transactional/ajax/getinlinehotelresult.aspx?id={1}&sid={2}&isHoliday=false&showPerPersonPrices=true&showAllRows=true&bags=0&bagprice=0&isRebookSearch=false&rebookExistingTotal=0&_=1420186419321' if
            args[0] == 'room_data' else None,
        ]

        for each in url_list:
            if each() is not None:
                return each()

        return TravelRepublicLandingPage.HOST

    @property
    def _get_headers(self, ):
        """
        headers for making requests
        :return: var_headers
        """
        var_headers = {
            "Accept": "image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/xaml+xml, application/vnd.ms-xpsdocument, application/x-ms-xbap, application/x-ms-application, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-shockwave-flash, */*",
            "Accept-Language": "en-us",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
            "Host": "www.travelrepublic.co.uk",
            "Proxy-Connection": "Keep-Alive"
        }

        return var_headers

    @property
    def _get_json_headers(self):
        """
        headers for making json requests
        :return: var_headers
        """
        var_headers = {}

        var_headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
        var_headers[
            "User-Agent"] = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322)"
        var_headers["Host"] = "www.travelrepublic.co.uk"
        var_headers["Connection"] = "Keep-Alive"
        var_headers["Referer"] = "https://www.travelrepublic.co.uk/"
        var_headers["Accept-Language"] = "en-us"
        var_headers["Content-Type"] = "application/json"
        var_headers["x-requested-with"] = "XMLHttpRequest"

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

    def _get_hotel_list(self):
        url = self._get_host_url_for_url_maker('hotel_list').format(
            TravelRepublicLandingPage.HOST,
            self.sid)
        return super()._get_hotel_list(url)

    def _get_matching_hotels(self):
        try:
            hotel_data_text = self.SERVICE_CALLS['get_matching_hotel'](self.country, self.city)
            hotel_tree = etree.fromstring(hotel_data_text)
            if hotel_tree.xpath('//nvcrWebSiteHotelId/text()'):
                return hotel_tree.xpath('//nvcrWebSiteHotelId/text()')
            else:
                raise TravelRepublicLandingPage.EXCEPTIONS['INVALID_URL']
            # process for json
            # hotel_data = json.loads(hotel_data_text)
            # if len(hotel_data['data']['data']) > 0:
                # cols = list(hotel_data['data']['data'][0].keys())
                # match_hotels_df = pd.DataFrame(hotel_data['data']['data'], columns=cols)
                # return match_hotels_df['WebSite_Hotel_ID'].tolist()
            # else:
                # raise TravelRepublicLandingPage.EXCEPTIONS['INVALID_URL']
            
        except TravelRepublicLandingPage.EXCEPTIONS['INVALID_URL']:
            self.TRL.debug_log('Unable to find matching hotels', self.request_id, self.sub_request_id, self.request_run_id)
        except TravelRepublicLandingPage.EXCEPTIONS['HOTEL_MATCHING_NOT_AVAILABLE']:
            self.TRL.debug_log('Matching Hotels Service Down', self.request_id, self.sub_request_id, self.request_run_id)

        return list()

    def _process_homepage(self):
        """
        method to process homepage, get cookies and make post
        form data call
        :return: None
        """
        # set HOST
        self.HOST = 'https://www.travelrepublic.co.uk/' if self.pos == 'United Kingdom' else 'https://www.travelrepublic.es/'

        # get matching hotel ids
        self.match_hotel_list = self._get_matching_hotels()

        TravelRepublicHomePage.HOME_PAGE = self
        res_html, res_obj, driver_obj = TravelRepublicHomePage._process(self)
        res_dict = json.loads(res_html)
        self.sid = res_dict['sid']

    def update_hotel_html(self, room_html, hotel_obj):
        hotel_html = hotel_obj._html['html_element']
        if hotel_html.find('<div class="chunky-tabs-footer') != -1:
            hotel_html = '{0}{1}'.format(hotel_html[0:hotel_html.find('<div     class="chunky-tabs-footer')], room_html)
        elif hotel_html.find('Seleccione Habitación') != -1:
            hotel_html = '{0}{1}'.format(hotel_html[0:hotel_html.find('Seleccione Habitación')], room_html)
        hotel_html = hotel_html.replace('="/', '="{0}'.format(self.HOST))
        hotel_html = hotel_html.replace("='/", "='{0}".format(self.HOST))

        hotel_obj._html['html_element'] = hotel_html

    def _get_booking_conditions(self, res_html):
        suppplier_dict = json.loads(res_html)
        url = '{0}{1}'.format(self.HOST, suppplier_dict['BookingConditionsLink'])
        res_html, res_obj, _ = self.get_request(url, headers=self._get_headers,
                                proxy=self.proxy)
        return res_html, res_obj

    def _process_room_page(self, hotel_id, hotel_obj):
        """
        :param: hotel_id of hotel
        :param: hotel_obj of ScrapperTravelRepublicPython.TravelRepublicHotel
        """
        room_url = self._get_host_url_for_url_maker('room_data').format(
            TravelRepublicLandingPage.HOST,
            hotel_id, self.sid)

        res_html, res_obj, _ = self.get_request(room_url, headers=self._get_headers,
                                                proxy=self.proxy)
        if res_html.find('roomcost') != -1:
            self.update_hotel_html(res_html, hotel_obj)
            if hotel_id in self.hotels_id_dict.values():
                TravelRepublicSupplierDetail.OBJ = self
                res_html, res_obj = TravelRepublicSupplierDetail._process(hotel_obj)
                hotel_obj._html['supplier_page'] = res_html
                booking_html, booking_obj = self._get_booking_conditions(res_html)
                hotel_obj._html['booking_page'] = booking_html

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = json.loads(self._get_hotel_list())

    def _save_hotel(self, index, hotel_url):
        try:
            latitude_url = self._lat_long_links[self._hotels.index(str(hotel_url))]
        except exceptions.LatLongNotFountError:
            self.TRL.debug_log('Latitude and Longitude not found in URL', self.request_id, self.sub_request_id,
                               self.request_run_id)
            latitude_url = None
        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url, self.request_id, self.sub_request_id,
                           self.request_run_id)
        self._set_hotel_web_id(self.hotels_id_dict[index])
        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(hotel_url, latitude_url, self)

        # process room page for the hotel specified
        self.TRL.debug_log('Making Hotel room type call for URL:%s' % hotel_url, self.request_id, self.sub_request_id,
                           self.request_run_id)
        self._process_room_page(self.hotels_id_dict[index], hotel)

        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        hotel_data = hotel.save_html(index)
        return hotel_data


def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    crawled_data = TravelRepublicLandingPage(consumer_data).crawl_hotels(redelivered)
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

