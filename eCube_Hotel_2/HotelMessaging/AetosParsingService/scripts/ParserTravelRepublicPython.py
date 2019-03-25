import re
import datetime
import numpy as np
import pandas as pd

from copy import deepcopy
from lxml import html, etree
from scripts import travel_republic_config
from scripts.core.logs import ParsingLogger
from scripts.core.base import ParserBase, ParamParser


class TravelRepublicLogger(ParsingLogger):
    NAME = 'travel_republic_crawling'


TravelRepublicLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = TravelRepublicLogger
ParserBase.CONFIG_FILE = travel_republic_config


class Hotel(ParserBase):
    PROPERTIES = [
        ParamParser('address', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__address, 'single_obj_array'),
        ParamParser('starRating', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__starRating, 'single_obj_array'),
    ]

    EXTRA_FIELDS = ['latitude', 'longitude', 'supplier', 'hotelName', 'website_id',
                    'city', 'city_zone', 'index', 'total_hotel', 'page_path']

    def __init__(self, parser_data):
        self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['html_element'])
        self.supplier_data = None
        if 'supplier_page' in parser_data['htmls']['hotelHTML']:
            self.supplier_data = parser_data['htmls']['hotelHTML']['supplier_page']
        super().__init__(parser_data)

    @property
    def parsed__latitude(self):
        latitude = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__latitude)
        for l in latitude:
            i = l.text
            if i and i.find('latitude') != -1:
                lat = i[i.find('latitude'): i.find('longitude')]
                lat = lat.split(':')[1].strip(',"').strip()
                return lat

    @property
    def parsed__longitude(self):
        longitude = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__longitude)
        for l in longitude:
            i = l.text
            if i and i.find('longitude') != -1:
                longi = i[i.find('longitude'):i.find(',', i.find('longitude'))]
                longi = longi.split(':')[1].strip()
                return longi

    @property
    def parsed__supplier(self):
        if self.supplier_data is not None:
            grp = re.search(ParserBase.CONFIG_FILE.Hotel__supplier, self.supplier_data)
            if grp is not None:
                supp_string = self.supplier_data[grp.end() + 2: self.supplier_data.find(',', grp.end())]
                supp_string = supp_string.strip('"')
                if supp_string.find('Travelscape') != -1:
                    supp_string = 'Expedia'
                return supp_string
            return ''
        else:
            return ''

    @property
    def parsed__city(self):
        return self.parser_data['city']

    @property
    def parsed__city_zone(self):
        return self.parser_data['city_zone']

    @property
    def parsed__hotelName(self):
        return self.parser_data['hotelName']

    @property
    def parsed__website_id(self):
        return self.parser_data['hotel_id']

    @property
    def parsed__index(self):
        return self.parser_data['index']

    @property
    def parsed__total_hotel(self):
        return self.parser_data['hotel_count']

    @property
    def parsed__page_path(self):
        return self.parser_data['meta']['cachePageURL']


class RoomType(ParserBase):
    PROPERTIES = []

    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):
        self.room_type_html = html.fromstring(parser_data['roomTypes']['roomTypeHTML'])
        self.room_price_html = html.fromstring(parser_data['roomTypes']['priceHTML'])
        self.room_boardtype_html = html.fromstring(parser_data['roomTypes']['boardTypeHTML'])

        check_in = datetime.datetime.strptime(parser_data['checkIn'].split(' ')[0], '%Y-%m-%d')
        check_out = datetime.datetime.strptime(parser_data['checkOut'].split(' ')[0], '%Y-%m-%d')
        nights = check_out - check_in

        self.days = nights.days + 1
        super().__init__(parser_data)

    def board_code_func(self, row):
        room_only = ['breakfast is available for a fee', 'breakfast excl', 'brkfast excl', 'no breakfast', 'offers on-site dining for breakfast at affordable prices', 'self-catering', "room Only(includes 2 breakfasts)", "solo alojamiento(wi-fi Gratis)", "solo habitacion", "solo habitaci?n", "solo alojamiento con cocina", "solo alojamiento", "solo alojamiento(ro)"]

        bed_brkfst = ['bed & breakfast', 'breakfast', 'english breakfast included', 'buffet breakfast', 'breakfast included', 'brkfast', 'cold breakfast', 'bed and breakfast', "alojamiento y desayuno", "habitaci?n y desayuno", "habitacion y desayuno", "alojamiento y desayuno(wi-fi gratis)", "desayuno Buffet", "desayuno Buffet Fr?o", "desayuno continental", ""]

        half_board = ['half board', 'breakfast and dinner', "media pensi?n", "media pension", "media pensi?n(wi-fi gratis)", "media pension(wi-fi gratis)"]

        full_board = ['full board', 'full board beverages included', "pensi?n completa", "pension completa"]

        all_incl = ['inclusive', "todo incluido"]

        others = ['other']

        for i in room_only:
            if i in row.lower():
                return 'RO', 'Room Only'

        for i in bed_brkfst:
            if i in row.lower():
                return 'BB', 'Bed and Breakfast'

        for i in half_board:
            if i in row.lower():
                return 'HB', 'Half Board'
        
        for i in full_board:
            if i in row.lower():
                return 'FB', 'Full Board'
        
        for i in all_incl:
            if i in row.lower():
                return 'AI', 'All Inclusive'
        
        for i in others:
            if i in row.lower():
                return 'OX', 'Others'

    def get_payment_option(self, payment_opt_lst):
        """
        returns a list of payment at hotel option as Y or N
        :param payment_opt_lst:
        :return: list of 'Y' or 'N'
        """
        payment_lst = list()
        for each in deepcopy(payment_opt_lst):
            if len(each.xpath(ParserBase.CONFIG_FILE.RoomType__payAtHotel)) > 0:
                payment_lst.append('Y')
            else:
                payment_lst.append('N')

        return payment_lst

    def get_currency(self, prices):
        """
        :param prices: list of prices for each room
        :return:
        """
        currency_lst = list()
        for i in prices:
            if i.startswith('\xA3'):    # check for pound
                currency_lst.append('GBP')
            elif i.startswith(chr(8364)):   # check for euro
                currency_lst.append('EUR')
            elif i.startswith('$'):     # check for USD
                currency_lst.append('USD')

        return currency_lst

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        types = self.room_type_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__type)
        prices = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__price)
        boards = self.room_boardtype_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__boardType)
        paymentOptions = self.get_payment_option(self.room_boardtype_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__payment))

        payload = dict()
        payload['type'] = [i.strip() for i in types if len(i.strip()) > 0]
        payload['price'] = [i.strip() for i in prices if len(i.strip()) > 0]
        payload['currency'] = self.get_currency(payload['price'])
        payload['boardType'] = [i.strip() for i in boards if len(i.strip()) > 0]
        payload['paymentOption'] = paymentOptions

        room_df = pd.DataFrame(payload, columns=list(payload.keys()))
        room_df['price'] = room_df['price'].str.slice(start=1)
        room_df['price'] = room_df['price'].str.replace(',', '')
        room_df['price'] = np.array(room_df['price'], dtype='str').astype(np.float)
        days = self.days
        room_df['daily_price'] = room_df['price'].apply(lambda row: row / days)
        room_df['board_code'], room_df['board_name'] = zip(*room_df['boardType'].apply(self.board_code_func))

        room_details = room_df.T.to_dict()

        return list(room_details.values())


def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """
    # from pdb import set_trace; set_trace()
    response = parser_data.copy()
    # response['hotels'] = [crawl_hotel(hotel_data) for hotel_data in parser_data['hotels']]
    response['hotel'] = crawl_hotel(parser_data['hotel'])
    return response


def crawl_hotel(hotel_data):
    hotel_meta = hotel_data['meta'].copy()
    hotel_payload = Hotel(hotel_data).complete_parsed_values
    room_types_payload = RoomType(hotel_data).complete_parsed_values
    mongo_data = dict()
    mongo_data.update(hotel_payload)
    mongo_data.update(room_types_payload)
    mongo_data.update({'meta': hotel_meta})
    return mongo_data
