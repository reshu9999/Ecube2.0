import numpy as np
import pandas as pd
import re
import datetime

from copy import deepcopy
from lxml import etree
from scripts import gta_config
from scripts.core.logs import ParsingLogger
from scripts.core.base import ParserBase, ParamParser
from pdb import set_trace;



class GTALogger(ParsingLogger):
    NAME = 'gta_crawling'


GTALogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = GTALogger
ParserBase.CONFIG_FILE = gta_config


class Hotel(ParserBase):
    PROPERTIES = []

    EXTRA_FIELDS = ['starRating', 'latitude', 'longitude', 'address', 'hotelName', 'website_id', 'city', 'city_zone', 'index', 'total_hotel', 'page_path']

    def __init__(self, parser_data):
        with open('tmp.xml', 'w') as fo:
            fo.write(parser_data['htmls']['hotelHtml']['html_element'])

        self.hotel_data_html = None
        with open('tmp.xml') as fo:
            self.hotel_data_html = etree.parse(fo)

        super().__init__(parser_data)

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
    def parsed__starRating(self):
        star_rating = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__starRating)
        return star_rating[0]

    @property
    def parsed__address(self):
        addr = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__address)
        return ', '.join(addr)

    @property
    def parsed__latitude(self):
        latitude = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__latitude)
        return latitude[0]

    @property
    def parsed__longitude(self):
        longitude = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__longitude)
        return longitude[0]
        
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
        return etree.tostring(self.hotel_data_html).decode('utf-8')


class RoomType(ParserBase):
    PROPERTIES = [
    ]

    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):
        self.room_type_html = etree.fromstring(parser_data['roomTypes']['roomTypeHTML'])
        self.room_price_html = etree.fromstring(parser_data['roomTypes']['priceHTML'])
        self.room_boardtype_html = etree.fromstring(parser_data['roomTypes']['boardTypeHTML'])
        with open('tmp.xml', 'w') as fo:
            fo.write(parser_data['htmls']['landingPage']['cost_price_page'])

        self.competitor_xml = None
        with open('tmp.xml') as fo:
            self.competitor_xml = etree.parse(fo)

        # set_trace()
        check_in = datetime.datetime.strptime(parser_data['checkIn'], '%Y-%m-%d %H:%M:%S')
        check_out = datetime.datetime.strptime(parser_data['checkOut'], '%Y-%m-%d %H:%M:%S')
        nights = check_out - check_in
        self.days = nights.days

        super().__init__(parser_data)

    def board_code_func(self, row):
        if row == 'B':
            return 'BB', 'Breakfast'
        elif row == 'D' or row == 'L':
            return 'HB', 'Half Board'
        elif row == 'F':
            return 'FB', 'Full Board'
        elif row == 'I':
            return 'AI', 'All Inclusive'
        else:
            return 'RO', 'Room Only'

    def get_promotions(self, elem_lst):
        promotion = []
        promotionDesc = []
        for i in elem_lst:
            if 'GrossWithoutDiscount' in i.attrib:
                promotion.append('Y')
                attr = i.attrib
                promotionDesc.append(attr['GrossWithoutDiscount'])
            else:
                promotion.append('N')
                promotionDesc.append('')

        return promotion, promotionDesc
    
    def parse__cost_price(self, room_df):
        hotel_elems = self.competitor_xml.xpath(ParserBase.CONFIG_FILE.Hotel__elems)
        for i in deepcopy(hotel_elems):
            cost_category_id = i.xpath(ParserBase.CONFIG_FILE.RoomType__category_id)
            cost_price = i.xpath(ParserBase.CONFIG_FILE.RoomType__price)
            for i, j in enumerate(cost_category_id):
                room_df.loc[room_df['room_id']==j, 'cost_price' ] = cost_price[i]
    
    @property
    def parsed__room_types(self):
        """
        :return:
        """
        types = self.room_type_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__type)
        prices = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__price)
        boards = self.room_boardtype_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__boardType)
        currency = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__currency)
        room_id = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__category_id)
        promotion, promotionDesc = self.get_promotions(self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__promotion))

        payload = dict()
        payload['type'] = [ i.strip() for i in types if len(i.strip()) > 0 ]
        payload['price'] = [ i.strip() for i in prices if len(i.strip()) > 0 ]
        payload['promotion'] = promotion
        payload['promotionDesc'] = promotionDesc
        payload['currency'] = [ i.strip() for i in currency if len(i.strip()) > 0 ]
        payload['boardType'] = [ i.strip() for i in boards if len(i.strip()) > 0 ]
        payload['room_id'] = [ i.strip() for i in room_id if len(i.strip()) > 0 ]
        
        room_df = pd.DataFrame(payload, columns=list(payload.keys()))
        room_df['price'] = room_df['price'].str.slice(start=1)
        room_df['price'] = room_df['price'].str.replace(',', '')
        room_df['price'] = np.array(room_df['price'], dtype='str').astype(np.float)
        days = self.days
        room_df['daily_price'] = room_df['price'].apply(lambda row: row / days)
        room_df['board_code'], room_df['board_name'] = zip(*room_df['boardType'].apply(self.board_code_func))
        room_df['payment_options'] = ''
        room_df['cost_price'] = 0
        self.parse__cost_price(room_df)
        room_details = room_df.T.to_dict()

        return list(room_details.values())


def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """
    response = parser_data.copy()
    # from pdb import set_trace; set_trace()
    # response['hotels'] = [crawl_hotel(hotel_data) for hotel_data in parser_data['hotels']]
    response['hotel'] = crawl_hotel(parser_data['hotel'])
    return response


def crawl_hotel(hotel_data):
    # from pdb import set_trace; set_trace()
    hotel_meta = hotel_data['meta'].copy()
    hotel_payload = Hotel(hotel_data).complete_parsed_values
    room_types_payload = RoomType(hotel_data).complete_parsed_values
    mongo_data = dict()
    mongo_data.update(hotel_payload)
    mongo_data.update(room_types_payload)
    mongo_data.update({'meta': hotel_meta})
    return mongo_data
