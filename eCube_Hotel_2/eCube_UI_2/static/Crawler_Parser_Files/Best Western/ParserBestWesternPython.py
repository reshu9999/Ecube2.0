import json
from lxml import html
import re
import datetime
from Parsing.scripts.Hotelbeds import ParserConfigBestWesternPython
from Parsing.scripts.core.logs import ParsingLogger
from Parsing.scripts.core.base import ParserBase, ParamParser


class BW_Logger(ParsingLogger):
    NAME = 'BW_parsing'


BW_Logger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = BW_Logger
ParserBase.CONFIG_FILE = ParserConfigBestWesternPython


class Hotel(ParserBase):
    PROPERTIES = []
    EXTRA_FIELDS = ['hotelName','hotelcode','starRating','address','city', 'city_zone', 'index', 'page_path', 'total_hotel','adult']

    def __init__(self, parser_data):
        self.parser_data = parser_data
        abc=parser_data['htmls']['hotel_html'].split('|')
        self.hotel_data_html = json.loads(abc[0])
        super().__init__(parser_data)

    @property
    def parsed__hotelName(self):
        return self.parser_data['hotelName']

    @property
    def parsed__starRating(self):
        abc=self.parser_data['htmls']['landingPage']
        starrating =re.findall('starRating\W+([\d].*)STAR",', abc)[0]
        print("starrating :" +starrating)
        return starrating

    @property
    def parsed__hotelcode(self):
        abc = self.parser_data['htmls']['hotel_html'].split('|')
        hotelcode=abc[1].replace("hotelprofile::",'').strip()
        print("hotelcode :" + str(hotelcode))
        return hotelcode.strip()

    @property
    def parsed__address(self):
        result = self.parser_data['htmls']['hotel_html'].split('||')[2].split('|')
        print("Address :" + str(result[0]))
        return str(result[0]).strip()

    @property
    def parsed__city(self):
        print("parsed__city " +str(self.parser_data['city']))
        return self.parser_data['city']

    @property
    def parsed__city_zone(self):
        print("parsed__city_zone "+ str(self.parser_data['city_zone']) )
        return self.parser_data['city_zone']

    @property
    def parsed__index(self):
        print("parsed__index " +str(self.parser_data['index']))
        return self.parser_data['index']

    @property
    def parsed__adult(self):
        # print("Adults :"+ str(self.parser_data['adults']))
        return self.parser_data['adults']

    @property
    def parsed__total_hotel(self):
        print("parsed__total_hotel " + str(self.parser_data['hotel_count']))
        return self.parser_data['hotel_count']

    @property
    def parsed__page_path(self):
        print("parsed__page_path " + str(self.parser_data['meta']['cachePageURL']))
        return self.parser_data['meta']['cachePageURL']

class RoomType(ParserBase):
    PROPERTIES = []
    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):

        self.room_data =parser_data['htmls']['room_html']
        abc = parser_data['htmls']['hotel_html'].split('|')
        self.hotel_data_html = json.loads(abc[0])

        super().__init__(parser_data)

    def get_board_type(self, promotion_str):
        board_type = "RO"
        if "BREAKFAST" in promotion_str.upper():
            board_type = "BB"
        return board_type

    def get_promotion(self, promotion_str):
        isPromotion = True

        return isPromotion

    def parsed__room_codes(self):
        print("parsed__Roomcodes " + str(self.parser_data['meta']['cachePageURL']))
        return self.room_data['room_html']['roomCode']

    @property
    def parsed__room_types(self):

        roomtypes = []
        policy=''
        promodesc=''
        board_type = "RO"
        breakfast = 'N'
        dp=''
        # itemdict = json.loads(self.room_data)
        for j in range(0,len(self.room_data)):
            roomdict= json.loads(self.room_data[j])
            for k in range(0,len(roomdict['roomDetailsList'])):
                roomcode=roomdict['roomDetailsList'][k]['roomId']
                roomName=roomdict['roomDetailsList'][k]['description']
                rate_plan=roomdict['rateCode']

                for rc in range(0, len(self.hotel_data_html)):
                    if rate_plan == self.hotel_data_html[rc]['rateCode']:
                        promodesc = self.hotel_data_html[rc]['shortName']
                        break

                if 'BW REWARDS' in promodesc :
                    if promodesc=='BW REWARDS ADVANCE PURCHASE' and rate_plan=="RACK":
                        promodesc = "FLEXIBLE RATE"
                    else:
                        continue

                if rate_plan=='VR':
                    continue
                if promodesc== "AAA AND CAA MEMBERS":
                    continue

                priceind=list(roomdict['roomDetailsList'][k]['dailyPriceMap'])[0]
                if len (list(roomdict['roomDetailsList'][k]['dailyPriceMap']))>1:
                    priceind2=list(roomdict['roomDetailsList'][k]['dailyPriceMap'])[1]
                    price= roomdict['roomDetailsList'][k]['dailyPriceMap'][priceind]+ roomdict['roomDetailsList'][k]['dailyPriceMap'][priceind2]
                else:
                    price = roomdict['roomDetailsList'][k]['dailyPriceMap'][priceind] * int(self.parser_data['nights'])

                dp= price/int(self.parser_data['nights'])
                roomtypeName=roomdict['roomDetailsList'][k]['additionalDescription']
                abc = self.parser_data['htmls']['landingPage']
                currency = re.findall('currencyCode\W+([\w].*?)",', abc)[0]
                amenitieslist = roomName.split(',')
                amenities=[]
                for am in range(1,len(amenitieslist)):
                    if amenitieslist[am] in roomdict['roomDetailsList'][k]['roomDescrQualifier']:
                        amenities.append(roomdict['roomDetailsList'][k]['roomDescrQualifier'][amenitieslist[am]])
                if 'Breakfast' in amenities or 'Full Breakfast' in amenities:
                    board_type = 'BB'
                    breakfast = 'Y'
                if promodesc != "":
                    promotion = 'Y'

                roomtypes.append({
                    'roomcode': roomcode.strip(),
                    'type': roomtypeName +" "+roomName.split(',')[0].strip(),
                    'rate_plan': rate_plan,
                    'board_code': board_type,
                    'rcode': 0,
                    'breakfast': breakfast,
                    'promotionDescription': promodesc,
                    'promotion':promotion,
                    "price": price,
                    "daily_price":dp,
                    # "taxes" :taxes,
                    'currency': currency,
                    "cancellation_policy": policy,
                    "availability": "Available",
                })

            # taxes=  self.room_data[j]['charges']['serviceCharges']
            # if 'NON_REFUNDABLE' in self.ratecode_data[rate_plan]['rateTags']:
            #     policy = 'NON_REFUNDABLE'
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
    # response['hotel'] = crawl_hotel(parser_data['hotel'])
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
