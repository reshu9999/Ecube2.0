from lxml import html
import pandas as pd
from param_parser import tripadvisor_config
from param_parser.core.logs import ParsingLogger
from param_parser.core.base import ParserBase, ParamParser


class TripadvisorLogger(ParsingLogger):
    NAME = 'tripadvisor_parsing'


TripadvisorLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = TripadvisorLogger
ParserBase.CONFIG_FILE = tripadvisor_config


class LandingPage(ParserBase):
    PROPERTIES = [
        ParamParser('hotelName', 'landing_page_html', ParserBase.CONFIG_FILE.LP__hotelName, 'empty_if_None')
    ]

    def __init__(self, parser_data):

        # self.landing_page_html = html.document_fromstring(parser_data['htmls']['landingPage']['landingPageHTML'])
        self.landing_page_html = html.document_fromstring(parser_data['htmls']['hotelHtml']['html_element'])
        super().__init__(parser_data)


class Hotel(ParserBase):
    PROPERTIES = [
        ParamParser('hotelId', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__id, 'empty_if_None'),
        ParamParser('name', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__name, 'empty_if_None'),
        ParamParser('roomType', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__roomType, 'empty_if_None'),
        ParamParser('containers', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__containers, 'empty_if_None'),
        ParamParser('price', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__price, 'empty_if_None'),
        ParamParser('boardType', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__boardType, 'empty_if_None'),
        ParamParser('address', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__address, 'empty_if_None'),
        ParamParser('starRating', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__starRating, 'empty_if_None'),
        ParamParser('Latitude', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__Lattitude,
                    'empty_if_None'),
        ParamParser('Longitude', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__Longitude,
                    'empty_if_None'),
        ParamParser('promotion', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__promotion, 'empty_if_None'),

        ParamParser('suppliers', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__supplier, 'empty_if_None'), #added by krishna
        ParamParser('taxes', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__tax, 'empty_if_None'), #added by krishna
    ]

    def __init__(self, parser_data):
        self.hotel_data_html = html.document_fromstring(parser_data['roomTypes']['roomTypeHTML']['html_element'])
        # self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHtml']['html_element'])
        self.latitude_html = html.document_fromstring(parser_data['htmls']['hotelHtml']['html_element'])
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
        ParamParser('name', 'room_type_html', ParserBase.CONFIG_FILE.Hotel__roomType, 'empty_if_None'),
        ParamParser('price', 'price_html', ParserBase.CONFIG_FILE.Hotel__price, 'empty_if_None'),
    ]

    def __init__(self, parser_data):
        self.room_type_html = html.document_fromstring(parser_data['roomTypes']['roomTypeHTML']['html_element'])
        try:
            self.price_html = html.document_fromstring(parser_data['roomTypes']['roomTypeHTML']['html_element'])
        except:
            self.price_html = None
        super().__init__(parser_data)

def get_room_data_list(adults,suppliers_list,prices_list):
    '''Method is added by krishna, freely customise this method as per requirement if method is required
    Can change no. and type of arguments as per requirement
    '''
    room_data_list = []
    for supplier, price in zip(suppliers_list,prices_list):
        rec = {
            'type':"Twin",
            'board_type':"RO",
            'supplier':supplier,
            'avg_price':float(price),
            'total_price': float(price) * adults,
            'promotion':"",
            'promo_desc':"",
            'direct_payment':"NULL",

        }
        room_data_list.append(rec)
    return room_data_list


def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """

    landing_page = LandingPage(parser_data).complete_parsed_values
    hotel = Hotel(parser_data).complete_parsed_values

    # Fixed for a hotel
    requestID = hotel['requestId']
    subRequestId = hotel['subRequestId']
    startDT = hotel['startDT']
    endDT = hotel['endDT']
    hotel_id = hotel['payload']['hotelId'][0] if hotel['payload']['hotelId'] else None
    hotelname = str(hotel['payload']['name'][0]).strip()
    rating = hotel['payload']['starRating'][0] if type(hotel['payload']['starRating']) is list else hotel['payload']['starRating']
    rating = float(rating[-2:])/10 if rating else 0

    suppliers_list = hotel['payload']['suppliers']
    prices_list = hotel['payload']['price']
    taxes_list = hotel['payload']['taxes']

    address_list = hotel['payload']['address']
    address = ''
    for a in address_list:
        address += a + ' '
    address = address.strip()
    city = parser_data['city']
    country = parser_data['country']
    nights = parser_data['nights']
    adults = parser_data['adults']
    checkin = parser_data['checkIn']
    checkout = parser_data['checkOut']
    POS = parser_data['POS']

    # Container values change
    hotel_data = {}

    # df = pd.DataFrame({'suppliers': suppliers, 'price': prices})
    room_types = get_room_data_list(adults,suppliers_list,prices_list)

    hotel_data['requestId'] = requestID
    hotel_data['subRequestId'] = subRequestId
    hotel_data['startDT'] = startDT
    hotel_data['endDT'] = endDT
    hotel_data["hotelId"] = hotel_id
    hotel_data['name'] = hotelname
    hotel_data['address'] = address
    hotel_data['city'] = city
    hotel_data['country'] = country
    hotel_data['POS'] = POS
    hotel_data['nights'] = nights
    hotel_data['checkin'] = checkin
    hotel_data['checkout'] = checkout
    hotel_data['adults'] = adults
    hotel_data['name'] = hotelname
    hotel_data['rating'] = rating
    hotel_data['latitude'] = ''
    hotel_data['longitude'] = ''
    hotel_data['roomtypes'] = room_types

    mongo_data = dict()
    # mongo_data.update(landing_page)
    mongo_data.update(hotel_data)
    # mongo_data.update(room_type)
    return mongo_data
    # return ParserBase.save_parsed_data(mongo_data)
