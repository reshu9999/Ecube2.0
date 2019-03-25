import datetime

from Parsing.scripts.Hotelbeds_Availability import parser_ExpediaApp_config
from Parsing.scripts.core.logs import ParsingLogger
from Parsing.scripts.core.base import ParserBase, ParamParser

class ExpediaAppLogger(ParsingLogger):
    NAME = 'lmb9_parsing'


ExpediaAppLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = ExpediaAppLogger
ParserBase.CONFIG_FILE = parser_ExpediaApp_config


class Hotel(ParserBase):
    PROPERTIES = []

    EXTRA_FIELDS = ['starRating', 'hotelName', 'city_zone', 'city', 'index', 'page_path', 'total_hotel', 'adult', 'website_id']

    def __init__(self, parser_data):
        self.hotel_data_html =eval(parser_data['roomTypes']['roomTypeHTML'])
        # self.latitude_html = parser_data['htmls']['latitude_html']['html_element']
        super().__init__(parser_data)

    @property
    def parsed__website_id(self):
        return self.hotel_data_html[-2]

    @property
    def parsed__address(self):
        city_region = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__cityRegion)
        city_region = city_region[0] if city_region else ""
        address = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__address)
        address = address[1].strip() + city_region + " " + address[2].strip() if address else "" + city_region
        return address

    @property
    def parsed__latitude(self):
        lat_start_index = self.latitude_html.find("var lat = '") + len("var lat = '")
        if lat_start_index==len("var lat = '") or lat_start_index < len("var lat = '"):
            lat_start_index = self.latitude_html.find("var lat      = '") + len("var lat      = '")
        lat_end_index = self.latitude_html.find("'", lat_start_index)
        lat = self.latitude_html[lat_start_index:lat_end_index]
        return lat

    @property
    def parsed__longitude(self):
        lng_start_index = self.latitude_html.find("var lng = '") + len("var lng = '")
        if lng_start_index==len("var lng = '") or lng_start_index < len("var lng = '"):
            lng_start_index = self.latitude_html.find("lng      = '") + len("lng      = '")
        lng_end_index = self.latitude_html.find("'", lng_start_index)
        lng = self.latitude_html[lng_start_index:lng_end_index]
        return lng

    @property
    def parsed__starRating(self):
        star_rating = self.hotel_data_html[5]
        if star_rating.replace('-', '.') == '1.5' or star_rating.replace('-', '.') == '2.5' or star_rating.replace('-', '.') == '3.5' or star_rating.replace('-', '.') == '4.5':
            star_rating = star_rating.replace('-', '.')
        else:
            star_rating = str(int(float(star_rating.replace('-', '.'))))

        return star_rating

    @property
    def parsed__hotelName(self):
        hotel_name = self.hotel_data_html[0]
        return hotel_name

    @property
    def parsed__city(self):
        return self.parser_data['city']

    @property
    def parsed__city_zone(self):
        return self.parser_data['city_zone']

    @property
    def parsed__adult(self):
        return self.parser_data['adults'] + ' Adt'

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
        self.room_data_html = eval(parser_data['roomTypes']['roomTypeHTML'])
        super().__init__(parser_data)

    @classmethod
    def get_promotion(cls, room_type):
        if "promo" in room_type.lower():
            return room_type
        else :
            return None

    @classmethod
    def get_board_type(cls, board_type):
        board_type_dict = {
            'no meal': 'RO',
            'half board': 'HB',
            'full board': 'FB',
            'breakfast': 'BB',
        }
        if board_type.lower() in board_type_dict.keys():
            return board_type_dict[board_type.lower()]
        elif "without" in board_type.lower():
            return board_type_dict["no meal"]
        elif "breakfast" in board_type.lower():
            return board_type_dict["breakfast"]
        else:
            return board_type_dict['no meal']

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        checkIn = datetime.datetime.strptime(self.parser_data['checkIn'], "%Y-%m-%d %H:%M:%S")
        checkOut = datetime.datetime.strptime(self.parser_data['checkOut'], "%Y-%m-%d %H:%M:%S")
        no_of_days = (checkOut - checkIn).days

        roomtypes = []
        board_code = "RO"
        room_type = 'Twin'
        self.room_data_html = self.room_data_html
        price = self.room_data_html[3]
        currency = self.room_data_html[4]

        roomtypes.append({
            "type": room_type,
            "board_code": board_code,
            "daily_price": round(float(price) / no_of_days,2),
            "price": price,
            "breakfast": '',
            "currency": currency,
            # "Paxs": self.adults
        })
        return roomtypes


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
    print("mongo_data")
    print(mongo_data)
    print("mongo_data end")
    return mongo_data
