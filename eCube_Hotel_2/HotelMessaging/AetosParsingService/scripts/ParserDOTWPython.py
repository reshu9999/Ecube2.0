import numpy as np
import pandas as pd
import json
import datetime

from copy import deepcopy
from lxml import html, etree
from scripts import dotw_config
from scripts.core.logs import ParsingLogger
from scripts.core.base import ParserBase, ParamParser


class DOTWLogger(ParsingLogger):
    NAME = 'dotw_parsing'


DOTWLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = DOTWLogger
ParserBase.CONFIG_FILE = dotw_config


class Hotel(ParserBase):
    PROPERTIES = [
        ParamParser('address', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__address, 'single_obj_array'),
        ParamParser('latitude', 'hotel_elem', ParserBase.CONFIG_FILE.Hotel__latitude, 'single_obj_array'),
        ParamParser('longitude', 'hotel_elem', ParserBase.CONFIG_FILE.Hotel__longitude, 'single_obj_array'),
    ]

    EXTRA_FIELDS = ['hotelName', 'website_id', 'starRating', 'city',
                    'index', 'total_hotel', 'page_path', 'supplier', 'city_zone']

    def __init__(self, parser_data):
        self.hotel_data_html = html.fromstring(parser_data['htmls']['hotelHTML']['html_element'])
        self.hotel_elem = html.fromstring(parser_data['htmls']['hotel_elem'])
        super().__init__(parser_data)

    @property
    def parsed__starRating(self):
        return self.hotel_elem.attrib['data-rate']

    @property
    def parsed__hotelName(self):
        return self.parser_data['hotelName']

    @property
    def parsed__website_id(self):
        return self.parser_data['hotel_id']

    @property
    def parsed__city(self):
        return self.parser_data['city']

    @property
    def parsed__index(self):
        return self.parser_data['index']

    @property
    def parsed__total_hotel(self):
        return self.parser_data['hotel_count']

    @property
    def parsed__pos(self):
        return self.parser_data['pos']

    @property
    def parsed__page_path(self):
        return self.parser_data['meta']['cachePageURL']

    @property
    def parsed__supplier(self):
        return 'dotwconnect'

    @property
    def parsed__city_zone(self):
        return self.parser_data['city_zone']


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
        self.days = nights.days
        super().__init__(parser_data)

    def board_code_func(self, row):
        room_only = ['breakfast is available for a fee', 'breakfast excl', 'brkfast excl', 'no breakfast', 'offers on-site dining for breakfast at affordable prices', 'self-catering', "room Only(includes 2 breakfasts)", "solo alojamiento(wi-fi Gratis)", "solo habitacion", "solo habitaci?n", "solo alojamiento con cocina", "solo alojamiento", "solo alojamiento(ro)", "room only"]

        bed_brkfst = ['bed & breakfast', 'breakfast', 'english breakfast included', 'buffet breakfast', 'breakfast included', 'brkfast', 'cold breakfast', 'bed and breakfast', "alojamiento y desayuno", "habitaci?n y desayuno", "habitacion y desayuno", "alojamiento y desayuno(wi-fi gratis)", "desayuno Buffet", "desayuno Buffet Fr?o", "desayuno continental"]

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

    def _get_promotions(self, board):
        """
        process promotions for each room if any
        :param board: list of room elements for the hotel
        :return: list of promotion description and promotion status
        """
        promo_status = []
        promo_desc_lst = []
        for i in board:
            val = i.xpath(ParserBase.CONFIG_FILE.RoomType__promotion)
            if len(val) > 0:
                promos = json.loads(val[0])[1]
                promo_desc = ''
                for k in promos.keys():
                    if k.startswith('h'):
                        promo_desc += promos[k]
                else:
                    promo_status.append('Y')
                    promo_desc_lst.append(promo_desc)
            else:
                promo_status.append('N')
                promo_desc_lst.append('')

        return promo_status, promo_desc_lst

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        types = self.room_type_html.xpath(ParserBase.CONFIG_FILE.RoomType__type)

        prices = [ i.attrib['data-roomformattedprice.1']
                   for i in self.room_price_html.xpath(ParserBase.CONFIG_FILE.RoomType__price) ]

        currency = [i.attrib['data-currency.1']
                    for i in self.room_price_html.xpath(ParserBase.CONFIG_FILE.RoomType__currency)]

        boards = self.room_boardtype_html.xpath(ParserBase.CONFIG_FILE.RoomType__boardType)

        payload = dict()
        payload['type'] = [i.strip() for i in types if len(i.strip()) > 0]
        payload['price'] = [i.strip() for i in prices if len(i.strip()) > 0]
        payload['boardType'] = [i.strip() for i in boards if len(i.strip()) > 0]
        payload['currency'] = [i.strip() for i in currency if len(i.strip()) > 0]

        board = deepcopy(self.room_type_html.xpath(ParserBase.CONFIG_FILE.RoomType__board))
        payload['promotion'], payload['promotionDesc'] = self._get_promotions(board)

        room_df = pd.DataFrame(payload, columns=list(payload.keys()))
        room_df['board_code'], room_df['board_name'] = zip(*room_df['boardType'].apply(self.board_code_func))
        days = self.days
        room_df['price'] = room_df['price'].str.replace(',', '')
        room_df['price'] = np.array(room_df['price'], dtype='str').astype(np.float)
        room_df['daily_price'] = room_df['price'].apply(lambda row: row / days)
        room_df['direct_payment'] = 'N'
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
