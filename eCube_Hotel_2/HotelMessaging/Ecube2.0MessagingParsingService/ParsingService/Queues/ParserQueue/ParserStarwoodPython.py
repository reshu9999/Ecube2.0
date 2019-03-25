from lxml import html
from param_parser import starwood_config
from param_parser.core.logs import ParsingLogger
from param_parser.core.base import ParserBase, ParamParser


class StarWoodLogger(ParsingLogger):
    NAME = 'starwood_parsing'


StarWoodLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = StarWoodLogger
ParserBase.CONFIG_FILE = starwood_config


class LandingPage(ParserBase):
    PROPERTIES = [
        ParamParser('hotelName', 'landing_page_html', ParserBase.CONFIG_FILE.LP__hotelName, 'empty_if_None')
    ]

    def __init__(self, parser_data):
        super().__init__(parser_data)
        self.landing_page_html = html.document_fromstring(parser_data['LandingPage'])


class Hotel(ParserBase):
    PROPERTIES = [
        ParamParser('name', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__name, 'single_obj_array'),
        ParamParser('roomType', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__roomType, 'empty_if_None'),
        ParamParser('promotion', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__promotion, 'empty_if_None'),
        ParamParser('price', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__price, 'empty_if_None'),
        ParamParser('boardType', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__boardType, 'empty_if_None'),
        ParamParser('address', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__address, 'empty_if_None'),
        ParamParser('starRating', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__starRating, 'empty_if_None'),
        ParamParser('LattitudeNLongitude', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__LattitudeNLongitude,
                    'empty_if_None'),
    ]

    def __init__(self, parser_data):
        super().__init__(parser_data)
        self.hotel_data_html = html.document_fromstring(parser_data['HotelData'])
        self.latitude_html = html.document_fromstring(parser_data['LatitudePage'])

    def parsed__details(self):
        part_1 = ParamParser.return_func__single_obj_array(
            self.latitude_html.xpath(ParserBase.CONFIG_FILE.Hotel__details1)
        )
        if not part_1:
            return part_1

        part_2 = ParamParser.return_func__empty_if_None(
            self.latitude_html.xpath(ParserBase.CONFIG_FILE.Hotel__details2)
        )
        if not part_2:
            return part_1
        return part_1 + part_2


class RoomType(ParserBase):

    PROPERTIES = [
        ParamParser('name', 'room_type_1_html', ParserBase.CONFIG_FILE.RoomType__name, 'empty_if_None'),
        ParamParser('price', 'room_type_1_html', ParserBase.CONFIG_FILE.RoomType__price, 'empty_if_None'),
    ]

    def __init__(self, parser_data):
        super().__init__(parser_data)
        self.room_type_1_html = html.document_fromstring(parser_data['Roomtype1'])
        self.room_type_2_html = html.document_fromstring(parser_data['Roomtype2'])


def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """
    landing_page = LandingPage(parser_data).complete_parsed_values
    hotel = Hotel(parser_data).complete_parsed_values
    room_type = RoomType(parser_data).complete_parsed_values
    mongo_data = dict()
    mongo_data.update(landing_page)
    mongo_data.update(hotel)
    mongo_data.update(room_type)
    return ParserBase.save_parsed_data(mongo_data)
