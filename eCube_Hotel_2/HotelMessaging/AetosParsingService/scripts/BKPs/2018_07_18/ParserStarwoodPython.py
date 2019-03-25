from lxml import html
from scripts import starwood_config
from scripts.core.logs import ParsingLogger
from scripts.core.base import ParserBase, ParamParser


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
        # self.landing_page_html = html.document_fromstring(parser_data['htmls']['landingPage'])
        super().__init__(parser_data)


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
        # from pdb import set_trace; set_trace()
        self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHtml']['html_element'])
        self.latitude_html = html.document_fromstring(parser_data['htmls']['hotelHtml']['latitude_html']['html_element'])
        super().__init__(parser_data)

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
        ParamParser('name', 'room_type_html', ParserBase.CONFIG_FILE.RoomType__name, 'empty_if_None'),
        # ParamParser('price', 'price_html', ParserBase.CONFIG_FILE.RoomType__price, 'empty_if_None'),
    ]

    def __init__(self, room_type_data):
        # from pdb import set_trace; set_trace()
        self.room_type_html = html.document_fromstring(room_type_data['roomTypeHTML'])
        # self.price_html = html.document_fromstring(room_type_data['priceHTML'])
        super().__init__(room_type_data)


def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """
    landing_page = LandingPage(parser_data).complete_parsed_values
    hotel = Hotel(parser_data).complete_parsed_values
    room_types = list()
    for room_type_data in parser_data['roomTypes']:
        room_type_data['meta'] = parser_data['meta'].copy()
        room_type = RoomType(room_type_data).complete_parsed_values
        room_types.append(room_type['payload'])
    mongo_data = landing_page
    mongo_data['payload'].update(hotel['payload'])
    mongo_data['payload'].update({'room_types': room_types})
    print("mongo_data")
    print(mongo_data['payload'])
    return mongo_data


# # Test Code
# import json
# with open('/home/ironeagle/Code/eCube_Hotel_2/HotelMessaging/Ecube2.0MessagingQueueLatest/ScrappingConsumer/starwood_response_1529670779.9690967.txt', 'r') as response_file:
#     file_data = response_file.read()
#     # print('file_data')
#     # print(file_data)
#     crawl_data = json.loads(file_data)
#     for data in crawl_data:
#         print(crawl_hotels(data))
