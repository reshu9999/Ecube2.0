import numpy as np
import pandas as pd
import re
import datetime  

from copy import deepcopy
from lxml import etree, html
# from AetosParsingService.scripts import gta_parser_config as gta_config
# from AetosParsingService.scripts.core.logs import ParsingLogger
# from AetosParsingService.scripts.core.base import ParserBase, ParamParser
from pdb import set_trace;
from Parsing.scripts.Hotelbeds import ParserConfigGTACHAINPython as gta_parser_config1
from Parsing.scripts.core.logs import ParsingLogger
from Parsing.scripts.core.base import ParserBase, ParamParser


class GTALogger(ParsingLogger):
    NAME = 'gta_crawling'


GTALogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = GTALogger
ParserBase.CONFIG_FILE = gta_parser_config1


class Hotel(ParserBase):
    PROPERTIES = []

    EXTRA_FIELDS = ['starRating', 'latitude', 'longitude', 'address', 'hotelName', 'website_id', 'city', 'city_zone', 'index', 'total_hotel', 'page_path','supplier_hotel_url','adult']

    def __init__(self, parser_data):
        # with open('tmp.xml', 'w') as fo:
        #     fo.write(parser_data['htmls']['hotelHtml']['html_element'])
        #
        # self.hotel_data_html = None
        # with open('tmp.xml') as fo:
        #     self.hotel_data_html = etree.parse(fo)
        self.hotel_data_html=etree.fromstring(parser_data['htmls']['hotelHtml']['html_element'].encode('utf-8'))
        super().__init__(parser_data)

    @property
    def parsed__city(self):
        return self.parser_data['city']

    @property
    def parsed__city_zone(self):
        city_zone = self.hotel_data_html.xpath("//ItemDetails//ItemDetail//City/text()")
        return city_zone[0]

    @property
    def parsed__adult(self):
        return self.parser_data['adults']

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
        #return latitude[0]
        return 0

    @property
    def parsed__longitude(self):
        longitude = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__longitude)
        #return longitude[0]
        return 0
        
    @property
    def parsed__website_id(self):
        HOTEL_ID=self.parser_data['city_zone'] + "_" +self.parser_data['hotel_id']
        return HOTEL_ID

    @property
    def parsed__index(self):
        return self.parser_data['index']

    @property
    def parsed__total_hotel(self):
        return self.parser_data['hotel_count']

    @property
    def parsed__page_path(self):
        # return etree.tostring(self.hotel_data_html).decode('utf-8')
        return self.parser_data['meta']['cachePageURL']

    @property
    def parsed__supplier_hotel_url(self):
        # return etree.tostring(self.hotel_data_html).decode('utf-8')
        return self.parser_data['meta']['sellingPageURL']

    # @property
    # def parsed__POS(self):
    #     return self.parser_data['POS']

class RoomType(ParserBase):
    PROPERTIES = [
    ]

    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):
        self.room_type_html = etree.fromstring(parser_data['roomTypes']['roomTypeHTML'])
        self.room_price_html = etree.fromstring(parser_data['roomTypes']['priceHTML'])
        self.room_boardtype_html = etree.fromstring(parser_data['roomTypes']['boardTypeHTML'])
        # with open('tmp.xml', 'w') as fo:
        #     fo.write(parser_data['htmls']['landingPage']['cost_price_page'])
        # #
        # self.competitor_xml = None
        # with open('tmp.xml') as fo:
        self.competitor_xml =etree.fromstring(str(parser_data['htmls']['landingPage']['cost_price_page']).encode('utf-8'))

        # set_trace()
        check_in = datetime.datetime.strptime(parser_data['checkIn'], '%Y-%m-%d %H:%M:%S')
        # check_out = datetime.datetime.strptime(parser_data['checkOut'], '%Y-%m-%d %H:%M:%S')
        # nights = check_out - check_in
        # self.days = nights.days
        nights=parser_data['nights']
        self.days=nights


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
    
    def parse__cost(self, room_df):
        hotel_elems = self.competitor_xml.xpath(ParserBase.CONFIG_FILE.Hotel__elems)
        for i in deepcopy(hotel_elems):
            cost_category_id = i.xpath(ParserBase.CONFIG_FILE.RoomType__category_id)
            cost = i.xpath(ParserBase.CONFIG_FILE.RoomType__price)
            for i, j in enumerate(cost_category_id):
                room_df.loc[room_df['room_id']==j, 'cost' ] = cost[i]

    def get_dynamic_property(self, elem_lst):
        dynamic_propety = []
        for i in elem_lst:
            if '001' in i:
                dynamic_propety.append('N')
            else:
                dynamic_propety.append('Y')

        return dynamic_propety

    def get_Opaquerate(self, elem_lst):
        Opaquerate = []
        for i in elem_lst:
            if 'true' in i:
                Opaquerate.append('Y')
            else:
                Opaquerate.append('N')

        return Opaquerate

    def get_daily_price(self, price):
        daily_price=float(price)/self.days
        return daily_price

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        room_id = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__category_id)

        types = self.room_type_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__type)
        prices = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__price)
        cancellation_policy1 = self.room_type_html[0].xpath(ParserBase.CONFIG_FILE.strNRF)
        if len(cancellation_policy1) != len(prices):
            cancellation_policy1 = [x for x in cancellation_policy1 if x == "999" or x == "1"]
        cancellation_policy = []
        for i in cancellation_policy1:
            if i == '999':
                cancellation_policy.append('1')
            else:
                cancellation_policy.append('0')
        boards = self.room_boardtype_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__boardType)
        currency = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__currency)
        Opaquerate = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.Opaque_rate)

        promotion, promotionDesc = self.get_promotions(
            self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__promotion))
        dynamic_propety = self.get_dynamic_property(room_id)
        Opaquerate = self.get_Opaquerate(Opaquerate)
        zip_types = list(zip(types,room_id,prices,cancellation_policy,boards,currency,Opaquerate,promotion,promotionDesc,dynamic_propety,room_id))
        types = [tup for tup in zip_types if str(tup[-1]).find("001")==-1 and str(tup[-1]).find("007")==-1]

        roomtypes=[]

        for record in types:
            roomtypes.append({
                "type": record[0],
                "room_id":record[1],
                "price": record[2],
                "cancellation_policy": record[3],
                "boards": record[4],
                "currency": record[5],
                "Opaquerate": record[6],
                "promotion": record[7],
                "promotionDesc": record[8],
                "dynamic_propety": record[9],
                "contractName": record[1],
                "costCurrency": record[5],
                "rcode": '0',
                "board_code": "RO",
                # "supplier": supplier,
                "daily_price": self.get_daily_price(record[2]), #float(price),
                # 'price': float(price) * adults,
                # 'tax': float(tax), #Goes null from our side
                "cost":"0",
                "breakfast": 0,
                # "currency": currency[0] if currency else None,
                "paymentOption": "N",
                "availability": "Available",

            })



            # payload = dict()
            # payload['type'] = record[0]
            # payload['Cancellation_Policy'] = [i.strip() for i in cancellation_policy if len(i.strip()) > 0]
            # payload['price'] = [ i.strip() for i in prices if len(i.strip()) > 0 ]
            # payload['promotion'] = promotion
            # payload['promotionDescription'] = promotionDesc
            # payload['dynamic_property'] = dynamic_propety
            # payload['Opaquerate'] = Opaquerate
            # payload['currency'] = [ i.strip() for i in currency if len(i.strip()) > 0 ]
            # payload['boardType'] = [ i.strip() for i in boards if len(i.strip()) > 0 ]
            # payload['room_id'] = [ i.strip() for i in room_id if len(i.strip()) > 0  ]
            # payload['contractName'] = [ i.strip() for i in room_id if len(i.strip()) > 0 ]
            #
            # payload['availability'] = ['Available' for i in room_id if len(i.strip()) > 0]
            # payload['breakfast'] = [ 0 for i in room_id if len(i.strip()) > 0]
            # payload['rcode'] = [ 0 for i in room_id if len(i.strip()) > 0]
            # room_df = pd.DataFrame(payload, columns=list(payload.keys()))
            # # room_df['price'] = room_df['price'].str.slice(start=1)
            # room_df['price'] = room_df['price'].str.replace(',', '')
            # room_df['price'] = np.array(room_df['price'], dtype='str').astype(np.float)
            # days = self.days
            # room_df['daily_price'] = room_df['price'].apply(lambda row: row / days)
            # room_df['board_code'], room_df['board_name'] = zip(*room_df['boardType'].apply(self.board_code_func))
            # room_df['payment_options'] = ''
            # room_df['cost'] = 0
            # room_df['costCurrency'] = [ i.strip() for i in currency if len(i.strip()) > 0 ]
            # self.parse__cost(room_df)
            # room_details = room_df.T.to_dict()

        return roomtypes



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
