import datetime
import json
import requests
import pandas as pd

from lxml import etree, html
from copy import deepcopy
from scripts import starwood_config
from scripts.core import exceptions
from scripts.core.logs import CrawlingLogger
from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler


class StarWoodLogger(CrawlingLogger):
    NAME = 'starwood_crawling'


StarWoodLogger.set_logger()
CrawlerBase.TRL = StarWoodLogger
CrawlerBase.CONFIG_FILE = starwood_config


class StarWoodHotel(HotelHandler):

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        page_html = html.fromstring(self._html['html_element'])
        return str(page_html.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()

    @property
    def _get_cache_page(self):
        return self._html['html_element']

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': etree.tostring(self._landing_page._html).decode('utf-8'), 'hotelHTML': self._html}

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """
        # from pdb import set_trace; set_trace()
        page_html = html.fromstring(self._html['html_element'])

        return [
            {'roomTypeHTML': page_html.xpath(self.CONFIG_FILE.roomDetailsInContainersXpath),
             'priceHTML': page_html.xpath(self.CONFIG_FILE.pricesInContainersXpath)},
            {'roomTypeHTML': page_html.xpath(self.CONFIG_FILE.roomDetailsInContainersXpath),
             'priceHTML': page_html.xpath(self.CONFIG_FILE.pricesInContainersXpath2)},
        ]


class StarWoodLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.starwoodhotels.com'
    HOTEL_HANDLER_CLASS = StarWoodHotel
    HOTEL_LIST_DRIVER = True

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        return self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        return [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]

    @property
    def _get_url_params(self):
        """
        :return: dict of key value to be added in URL
        """
        inDate = datetime.datetime.now() + datetime.timedelta(days=int(self.days))
        inDate = inDate.strftime("%m/%d/%Y")
        inSplit = str(inDate).split('/')
        #inSplit = str(self.check_in).split('/')
        inMonth, inDay, inYear = inSplit[0], inSplit[1], inSplit[2]

        checkOut = datetime.datetime.now() + datetime.timedelta(days=int(self.days) + int(self.nights))
        checkOut = checkOut.strftime("%m/%d/%Y")
        outSplit = str(checkOut).split('/')
        outMonth, outDay, outYear = outSplit[0], outSplit[1], outSplit[2]

        return {
            'iataNumber': '',
            'complexSearchField': self.city + '%2C+' + self.country,
            'searchType': 'location',
            'propertyIds': '',
            'arrivalDate': inMonth + '%2F' + inDay + '%2F' + inYear,
            'departureDate': outMonth + '%2F' + outDay + '%2F' + outYear,
            # 'numberOfRooms': self.room,
            'numberOfAdults': self.adults,
            'numberOfChildren': self.children,

        }

    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        # from pdb import set_trace; set_trace()
        cookies_list = cookie_object.get_cookies()
        while len(cookies_list) < 17:
            cookie_object.get(self._url_maker())
            cookies_list = cookie_object.get_cookies()
        cookie_object.quit()
        for cookie in cookies_list:
            if cookie['name'] == 'aOmIj1jm':
                self.cookie = {'aOmIj1jm': cookie['value']}
                break

    def _process_homepage(self):
        pass

    @property
    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """

        headers = {
            "Host": "www.starwoodhotels.com",
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng*/*;q=0.8',
            'User-Agent': self.user_agent.strip(),
            "Proxy-Connection": "Keep-Alive"
        }

        return headers


def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    crawled_data = StarWoodLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    # file_distincter = time.time()
    # with open('crawled_data_%s.json' % file_distincter, 'w+') as file_obj:
    #     print("file_distincter")
    #     print(file_distincter)
    #     file_obj.write(json.dumps(crawled_data))
    return crawled_data
