import re
import ast
import datetime
import numpy as np
import pandas as pd
import csv
from copy import deepcopy
from lxml import html, etree
from codecs import escape_decode
from Parsing.scripts.Hotelbeds_Availability import ParserConfigBookingPython
from Parsing.scripts.core.logs import ParsingLogger
from Parsing.scripts.core.base import ParserBase, ParamParser
import json


class BookingLogger(ParsingLogger):
    NAME = 'booking_availability_parsing'


BookingLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = BookingLogger
ParserBase.CONFIG_FILE = ParserConfigBookingPython

def checkrubbish(textstring):
    textstring = textstring.replace("Ã©", "e")
    textstring = textstring.replace("Ă¨", "e")
    textstring = textstring.replace("â€™", "")
    textstring = textstring.replace("Ă´", "o")
    textstring = textstring.replace("À", "A")
    textstring = textstring.replace("Á", "A")
    textstring = textstring.replace("Â", "A")
    textstring = textstring.replace("Ã", "A")
    textstring = textstring.replace("Ä", "A")
    textstring = textstring.replace("Å", "A")
    textstring = textstring.replace("Æ", "A")
    textstring = textstring.replace("Ç", "C")
    textstring = textstring.replace("È", "E")
    textstring = textstring.replace("É", "E")
    textstring = textstring.replace("Ê", "E")
    textstring = textstring.replace("Ë", "E")
    textstring = textstring.replace("Ì", "I")
    textstring = textstring.replace("Í", "I")
    textstring = textstring.replace("Î", "I")
    textstring = textstring.replace("Ï", "I")
    textstring = textstring.replace("Ð", "D")
    textstring = textstring.replace("Ñ", "N")
    textstring = textstring.replace("Ò", "O")
    textstring = textstring.replace("Ó", "O")
    textstring = textstring.replace("Ô", "O")
    textstring = textstring.replace("Õ", "O")
    textstring = textstring.replace("Ö", "O")
    textstring = textstring.replace("×", "X")
    textstring = textstring.replace("Ø", "O")
    textstring = textstring.replace("Ù", "U")
    textstring = textstring.replace("Ú", "U")
    textstring = textstring.replace("Û", "U")
    textstring = textstring.replace("Ü", "U")
    textstring = textstring.replace("Ý", "Y")
    textstring = textstring.replace("Þ", "P")
    textstring = textstring.replace("ß", "B")
    textstring = textstring.replace("à", "a")
    textstring = textstring.replace("á", "a")
    textstring = textstring.replace("â", "a")
    textstring = textstring.replace("ã", "a")
    textstring = textstring.replace("ä", "a")
    textstring = textstring.replace("å", "a")
    textstring = textstring.replace("æ", "a")
    textstring = textstring.replace("ç", "c")
    textstring = textstring.replace("è", "e")
    textstring = textstring.replace("é", "e")
    textstring = textstring.replace("ê", "e")
    textstring = textstring.replace("ë", "e")
    textstring = textstring.replace("ì", "i")
    textstring = textstring.replace("í", "i")
    textstring = textstring.replace("î", "i")
    textstring = textstring.replace("ï", "i")
    textstring = textstring.replace("ð", "d")
    textstring = textstring.replace("ñ", "n")
    textstring = textstring.replace("ò", "o")
    textstring = textstring.replace("ó", "o")
    textstring = textstring.replace("ô", "o")
    textstring = textstring.replace("õ", "o")
    textstring = textstring.replace("ö", "o")
    textstring = textstring.replace("÷", "o")
    textstring = textstring.replace("ø", "o")
    textstring = textstring.replace("ù", "u")
    textstring = textstring.replace("ú", "u")
    textstring = textstring.replace("û", "u")
    textstring = textstring.replace("ü", "u")
    textstring = textstring.replace("ý", "y")
    textstring = textstring.replace("þ", "P")
    textstring = textstring.replace("\'", "'")
    textstring = textstring.replace("Œ", "u")
    textstring = textstring.replace("œ", "u")
    textstring = textstring.replace("Ÿ", "o")
    textstring = textstring.replace("¿", "")
    textstring = textstring.replace("¢", "c")
    textstring = textstring.replace("¶", "o")
    return textstring


class Hotel(ParserBase):
    PROPERTIES=[]
    EXTRA_FIELDS = ['hotelName','adult','starRating', 'hotel_id','city', 'city_zone', 'index', 'page_path','website_id','total_hotel','latitude','longitude']

    def __init__(self, parser_data):
        self.parser_data  = parser_data
        self.textdata = parser_data['htmls']

        # self.latitude_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['latitude_html']['html_element'])
        # self.hotel_data_html = html.document_fromstring(parser_data['roomTypes']['roomTypeHTML']['html_element'])
        # self.latitude_html = parser_data['roomTypes']['roomTypeHTML']['latitude_html']

        htmlElements=escape_decode(parser_data['htmls'])[0].decode('utf-8')
        self.hotel_data_html = html.document_fromstring(htmlElements)

        self.POS ='Spain' #parser_data['POS']
        super().__init__(parser_data)

    @property
    def parsed__hotelName(self):

        result = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__name)
        if not result:
            return ''
        else:
            hotel_name=result[0].replace('\\n','').replace('\n','').strip()
            hotel_name=checkrubbish(hotel_name)
            # print(result)
            return hotel_name

    @property
    def parsed__adult(self):
        return '2 Adt'
        # return self.parser_data['adults']

    @property
    def parsed__website_id(self):
        result = re.findall('data-hotelid=([\W\d]*)"\s', self.textdata)
        if not result:
            return ''
        else:
            hotelid = result[0].strip().replace('"', '').replace('\\n','').replace('\n','').replace('\\', '')
            return hotelid.strip()

    @property
    def parsed__hotel_id(self):

        result =re.findall('data-hotelid=([\W\d]*)"\s',self.textdata)
        if not result:
            return ''
        else:
            hotelid=result[0].strip().replace('\\n','').replace('\n','').replace('"','').replace('\\','')
            return hotelid
    @property
    def parsed__starRating(self):
        star_rating =[]
        result = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__starRating)
        if not result:
            return 'PENDI'
        else:
            star1= result[0].strip().split('-')
            if len(star1)>1:
                star= star1[0].strip()

            else:
                star= result[0].replace('stars', '').replace('star', '').strip()

            return star

    @property
    def parsed__nights(self):
        return 1
        # stay = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__stay)[0]
        # stay = stay.split('-')[0]
        # stay = int(stay)
        # return stay

    @property
    def parsed__Room_Availablility(self):
        containers = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__priceblocks)
        rooms_available = len(containers)
        return rooms_available

    @property
    def parsed__Company(self):
        return 'Booking'

    @property
    def parsed__Status(self):
        return 'Completed'

    @property
    def parsed__Type_of_event(self):
        return 'Fixed'

    @property
    def parsed__POS(self):
        return self.POS

    @property
    def parsed__supplier(self):
        return ''


    @property
    def parsed__latitude(self):
        lat=''
        stringlat = self.textdata.split('||')
        if len(stringlat)>1:
            lat=stringlat[1].replace('Latitude','').replace(':','').strip()

        return lat

    @property
    def parsed__longitude(self):
        stringlat = self.textdata.split('||')
        long=''
        if len(stringlat) >2:
            long = stringlat[2].replace('Longitude', '').replace(':', '').strip()

        return long

    @property
    def parsed__city(self):
        return self.parser_data['city']

    @property
    def parsed__city_zone(self):
        return self.parser_data['city_zone']
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

        self.country = parser_data['country']
        self.city = parser_data['city']
        self.textdata=parser_data['htmls']


        htmlElements=escape_decode(parser_data['htmls'])[0].decode('utf-8')
        self.hotel_data_html = html.document_fromstring(htmlElements)

        super().__init__(parser_data)

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        roomtypes= []
        room_type=""
        mealplan=""
        breakfastincluded=""
        is_directPayment=""

        containers = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__roomType)
        if len(containers)>0:
            room_type = containers[0].replace('\\n','').replace('\n','').replace('\\','').strip() ##.text_content()
            meal=self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.RoomType_details)
            if len(meal)>0:
                if "Breakfast included" in str(meal[0]).strip():
                    mealplan= "BB"
                    breakfastincluded= str(meal[0]).strip()
                else:
                    mealplan="EP"
            else:
                mealplan="EP"

        board_code = self.__class__.get_board_code(mealplan)
        if board_code=="RO":
            breakfastincluded='N'
        else:
            breakfastincluded='Y'
        directpay1 =self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.RoomType__directpay)
        if len(directpay1)>0:
            # if directpay1[0].strip() == "Payment at the hotel":
            if "Payment at the hotel" in directpay1[0].strip():
                is_directPayment = True
            elif "No prepayment needed" in directpay1[0].strip():
                is_directPayment = True
            else:
                is_directPayment = False

        hotelpricelist=self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__price)
        currency=""
        price = ""
        if not hotelpricelist:
            price=""
        else:

            price= str(hotelpricelist[0]).replace("\\xe2\\x82\\xac\\xc2\\xa0","").replace('€','').replace(',','').strip()
            price=price.replace('\\n','').replace('\n','').replace('Â','').strip()

            price1= re.findall("([\d,].*)",price)
            if len(price1)>0:
                price = price1[0]

            try:
                currency=self.parser_data['htmls'].split('|')[1]
                currency=currency.replace('Currency ::','').strip()
            except Exception as e:
                raise self.EXCEPTIONS['currency not found'](str(e))

        roomtypes.append({
            "type": room_type,
            "board_code": board_code,
            "paymentOption": "Y" if is_directPayment else "N",
            "price": price,
            "currency": currency,
        })

        return roomtypes

    @classmethod
    def get_board_code(self, board_type):
        '''
        EP = Breakfast not included,
        BB = Breakfast included,
        HB = Half board included,
        '''
        # board_type1=self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.RoomType_details)

        if board_type in ["EP"]:
            return "RO"
        elif board_type in ["BB"]:
            return "BB"
        elif board_type in ["HB"]:
            return "HB"
        elif board_type in ["FB"]:
            return "FB"
        elif board_type in ["AI"]:
            return "AI"
        else:
            return "RO"

def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """
    # from pdb import set_trace; set_trace()
    # parser_data=ast.literal_eval(parser_data)
    response = parser_data.copy()
    # response['hotels'] = [crawl_hotel(hotel_data) for hotel_data in parser_data['hotels'][0:]]
    response['hotel'] = crawl_hotel(parser_data['hotel'])
    # response['hotel'] = [crawl_hotel(hotel_data) for hotel_data in parser_data['hotel'][0:]]
    return response

""
def crawl_hotel(hotel_data):

    hotel_meta = hotel_data['meta'].copy()
    ##loop
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
