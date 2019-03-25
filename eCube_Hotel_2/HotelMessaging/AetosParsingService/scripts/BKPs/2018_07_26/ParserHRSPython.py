import pandas as pd

from lxml import html, etree
from copy import deepcopy
from scripts import hrs_config
from scripts.core.logs import ParsingLogger
from scripts.core.base import ParserBase, ParamParser


class HRSLogger(ParsingLogger):
    NAME = 'hrs_parsing'


HRSLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = HRSLogger
ParserBase.CONFIG_FILE = hrs_config


class LandingPage(ParserBase):
    # PROPERTIES = [
        # # ParamParser('hotelName', 'landing_page_html', ParserBase.CONFIG_FILE.LP__hotelName, 'empty_if_None')
    # ]

    def __init__(self, parser_data):
        # self.landing_page_html = html.document_fromstring(parser_data['LandingPage'])
        super().__init__(parser_data)


class Hotel(ParserBase):
    PROPERTIES = [
        ParamParser('address', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__address, 'single_obj_array'),
        ParamParser('starRating', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__starRating, 'single_obj_array'),
        ParamParser('latitude', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__latitude, 'single_obj_array'),
        ParamParser('longitude', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__longitude, 'single_obj_array'),
    ]

    EXTRA_FIELDS = ['hotelName', 'hotel_id', 'website_id', 'city', 'index', 'total_hotel', 'page_path']

    def __init__(self, parser_data):
        self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHtml']['html_element'])
        super().__init__(parser_data)

    @property
    def parsed__hotelName(self):
        # from pdb import set_trace; set_trace();
        return self.parser_data['hotelName']

    @property
    def parsed__hotel_id(self):
        return self.parser_data['hotel_id']

    @property
    def parsed__city(self):
        return self.parser_data['city']

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

    PROPERTIES = []

    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):
        self.room_name_html = html.fromstring(parser_data['roomTypes']['roomTypeHTML'])
        self.room_type_html = html.fromstring(parser_data['roomTypes']['roomTypeHTML'])
        self.room_price_html = html.fromstring(parser_data['roomTypes']['priceHTML'])
        self.room_promotion_html = html.fromstring(parser_data['roomTypes']['promotionHTML'])
        self.room_boardtype_html = html.fromstring(parser_data['roomTypes']['boardTypeHTML'])

        super().__init__(parser_data)

    def board_code_func(self, row):
        """
        method to return board code of room types
        :return: board code and board name
        """
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

    @property
    def parsed__room_types(self):
        """
        parse room details and save in database
        :return: list of dictionary of room types
        """
        # names = self.room_name_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__name)
        # types = self.room_type_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__type)
        # prices = self.room_price_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__price)
        # boards = self.room_boardtype_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__boardType)
        # promotion = self.room_promotion_html[0].xpath(ParserBase.CONFIG_FILE.RoomType__promotion)
        names = self.room_name_html.xpath(ParserBase.CONFIG_FILE.RoomType__name)
        types = self.room_type_html.xpath(ParserBase.CONFIG_FILE.RoomType__type)
        prices = self.room_price_html.xpath(ParserBase.CONFIG_FILE.RoomType__price)
        boards = self.room_boardtype_html.xpath(ParserBase.CONFIG_FILE.RoomType__boardType)
        promotion = self.room_promotion_html.xpath(ParserBase.CONFIG_FILE.RoomType__promotion)
        payload = dict()

        payload['type'] = [i.strip() for i in types if len(i.strip()) > 0]
        payload['price'] = [i.strip() for i in prices if len(i.strip()) > 0]
        payload['boardType'] = [i.strip() for i in boards if len(i.strip()) > 0]
        payload['name'] = [i.strip() for i in names if len(i.strip()) > 0]
        # need to check when Promotion is found
        if len(promotion) == 0:
            payload['promotion'] = ['N' for _ in prices]
        else:
            payload['promotion'] = [i.strip() for i in promotion if len(i.strip()) > 0]
        # from pdb import set_trace; set_trace();
        room_df = pd.DataFrame(payload, columns=list(payload.keys()))
        room_df['types'] = room_df.apply(lambda row: '{0} {1}'.format(row['name'], row['type']), axis=1)
        room_df.drop(['name', 'type'], inplace=True, axis=1)
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
    with open('/home/tech/Desktop/BhavinDhimmar/hrstest.json','w') as fo: #Bhavin
        import json; json.dump(room_types_payload, fo) #bhavin
    mongo_data = dict()
    mongo_data.update(hotel_payload)
    mongo_data.update(room_types_payload)
    mongo_data.update({'meta': hotel_meta})
    return mongo_data
