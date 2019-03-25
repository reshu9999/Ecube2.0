import datetime
from scripts import starwood_config
from lxml import html

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
        pageHtml = html.fromstring(self._html['html_element'])

        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        # from pdb import set_trace; set_trace()
        return {'landingPage': self._landing_page._html.text, 'hotelHtml': self._html}

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """
        hotel_html = html.fromstring(self._html['html_element'])
        return [
            {'roomTypeHTML': self._html['html_element'], 'priceHTML': hotel_html.xpath(self.CONFIG_FILE.pricesInContainersXpath)},
            {'roomTypeHTML': self._html['html_element'], 'priceHTML': hotel_html.xpath(self.CONFIG_FILE.pricesInContainersXpath2)},
        ]


class StarWoodLandingPage(HotelLandingPageHandler):

    HOST = 'www.starwoodhotels.com'
    CHILD_CLASSES = {
        'HotelHandler': StarWoodHotel
    }

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
        # inSplit = str(self.check_in).split('/')
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
            'Host': self.HOST,
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng*/*;q=0.8',
            'User-Agent': self.user_agent.strip()}
        return headers


def crawl_hotels(consumer_data):
    # import json
    # import time
    # hotels = StarWoodLandingPage(consumer_data).crawl_hotels()
    # hotel_file_data = json.dumps(hotels)
    # file_name = '/home/ironeagle/Code/eCube_Hotel_2/HotelMessaging/Ecube2.0MessagingQueueLatest/ScrappingConsumer/starwood_response_%s.txt' % time.time()
    # with open(file_name, 'w+') as response_file:
    #     response_file.write(hotel_file_data)
    # return hotels
    return StarWoodLandingPage(consumer_data).crawl_hotels()


# Testing Code
# import json
#
# consume_data = {'DomainID': 21, 'RequestInputs': {'webSiteHotelId': '', 'adults': 1, 'checkIn': '2018-06-25',
#                                                   'checkOut': '2018-07-25', 'CompetitorName': 'Starwood',
#                                                   'starRating': '5,4,3',
#                                                   'board': 'Ram,Business class,Lower,ABC,sljdfsjsflksjfskl,jsdlkfkjdsklj,dfca,dfca,wer',
#                                                   'RentalLength': 1, 'hotelName': '', 'city': 'Bombay', 'children': '1',
#                                                   'CrawlMode': 'All Hotel / City',
#                                                   'room': 'SuperDeluxe,Deluxe,Makaan', 'RequestUrl': '',
#                                                   'CountryName': 'India', 'pos': 'India'},
#                 'ParserScript': 'StarwoodPython', 'PointOfSale': '', 'DomainName': 'Starwood',
#                 'ScraperScript': 'ScrapperStarwoodPython', 'requestRunId': 120, 'RequestUrl': '',
#                 'BusinessType': 'Hotel', 'IsCategory': None, 'requestId': 2178, 'call_func': '', 'subRequestId': 2,
#                 'GroupName': 'RS', 'country': 'India'}
#
# hotels = crawl_hotels(consume_data)
# # from pdb import set_trace; set_trace()
# hotel_file_data = json.dumps(hotels)
# with open('/home/ironeagle/Code/eCube_Hotel_2/HotelMessaging/Ecube2.0MessagingQueueLatest/ScrappingConsumer/starwood_response.txt', 'w+') as response_file:
#     response_file.write(hotel_file_data)
