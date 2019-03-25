import re
import datetime
import numpy as np
import pandas as pd

from copy import deepcopy
from lxml import html, etree
from scripts import starwood_config
from scripts.core.logs import ParsingLogger
from scripts.core.base import ParserBase, ParamParser


class StarWoodLogger(ParsingLogger):
    NAME = 'starwood_parsing'


StarWoodLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = StarWoodLogger
ParserBase.CONFIG_FILE = starwood_config


class Hotel(ParserBase):
    PROPERTIES = [
        ParamParser('address', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__address, 'single_obj_array'),
        ParamParser('starRating', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__starRating, 'single_obj_array'),
        ParamParser('Latitude', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__Lattitude, 'single_obj_array'),
        ParamParser('Longitude', 'latitude_html', ParserBase.CONFIG_FILE.Hotel__Longitude, 'single_obj_array'),
    ]

    EXTRA_FIELDS = ['hotelName', 'website_id', 'city', 'index', 'page_path', 'total_hotel']

    def __init__(self, parser_data):
        self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['html_element'])
        self.latitude_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['latitude_html']['html_element'])
        super().__init__(parser_data)

    @property
    def parsed__supplier(self):
        return

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
        return self.parser_data['meta']['cachePageURL']


class RoomType(ParserBase):
    PROPERTIES = []

    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):
        self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['html_element'])
        super().__init__(parser_data)

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        roomtypes = []
        containers = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__containers)
        for container in containers:
            roomtype = str(container.xpath(starwood_config.Hotel__roomType)[0]).strip()
            priceblocks = container.xpath(starwood_config.Hotel__priceblocks)
            for priceblock in priceblocks:
                price = priceblock.xpath(starwood_config.Hotel__price)[0]
                promotion = ''
                boardtype = str(priceblock.xpath(starwood_config.Hotel__boardType)[0]).strip()
                roomtypes.append({"RoomType": roomtype, "BoardType": boardtype, "Rate": price, 'promotion': promotion})
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
