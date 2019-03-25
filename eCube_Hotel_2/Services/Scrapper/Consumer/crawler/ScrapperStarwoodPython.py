from crawler import starwood_config
from core.logs import CrawlingLogger
from core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler


class StarWoodLogger(CrawlingLogger):
    NAME = 'starwood'


StarWoodLogger.set_logger()
CrawlerBase.TRL = StarWoodLogger
CrawlerBase.CONFIG_FILE = starwood_config


class StarWoodLandingPage(HotelLandingPageHandler):

    HOST = 'www.starwood.com'

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        raise self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)

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
        inSplit = str(self.check_in).split('/')
        inMonth, inDay, inYear = inSplit[0], inSplit[1], inSplit[2]

        outSplit = str(self.check_out).split('/')
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


class StarWoodHotel(HotelHandler):

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        return self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': self._landing_page._html}

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """
        room_details = self._html.xpath(self.CONFIG_FILE.roomDetailsInContainersXpath)
        return [
            {'roomTypeHTML': room_details, 'priceHTML': room_details.xpath(self.CONFIG_FILE.pricesInContainersXpath)},
            {'roomTypeHTML': room_details, 'priceHTML': room_details.xpath(self.CONFIG_FILE.pricesInContainersXpath2)},
        ]
