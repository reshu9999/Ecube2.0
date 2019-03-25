import re
import datetime
import requests
from lxml import html
from scripts.core import utils
from scripts import tripadvisor_config

from scripts.core.logs import CrawlingLogger
from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler


class TripadvisorLogger(CrawlingLogger):
    NAME = 'TripAdvisor_Crawling'


TripadvisorLogger.set_logger()
CrawlerBase.TRL = TripadvisorLogger
CrawlerBase.CONFIG_FILE = tripadvisor_config


class TripAdvisorLandingPage(HotelLandingPageHandler):

    HOST = 'http://www.tripadvisor.co.uk'

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        # check = self._html['lxmlELEM']
        # return self._html['lxmlELEM'].xpath(self.CONFIG_FILE.hotelLinksXpath)
        return self._html

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        return [self._clean_host_url + lt for lt in self._html['lxmlELEM'].xpath(self.CONFIG_FILE.latLongXpath)]

    @property
    def _get_url_params(self):
        """
        :return: dict of key value to be added in URL
        """
        inDate = datetime.datetime.now() + datetime.timedelta(days=int(self.days))
        inDate = inDate.strftime("%m/%d/%Y")
        inSplit = str(inDate).split('/')
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
        self.cookie = cookie_object.get_dict()


    @classmethod
    def get_formatted_date(cls,checkIn_dt, checkOut_dt):
        in_datetime = datetime.datetime.strptime(checkIn_dt, "%d-%m-%Y")
        out_datetime = datetime.datetime.strptime(checkOut_dt, "%d-%m-%Y")
        in_day, in_month, in_year = in_datetime.day, in_datetime.month, in_datetime.year
        out_day, out_month, out_year = out_datetime.day, out_datetime.month, out_datetime.year

        in_day = "0" + str(in_day) if in_day < 10 else str(in_day)  # prefixing 0 if day is a single digit
        in_month = "0" + str(in_month) if in_month < 10 else str(in_month)  # prefixing 0 if month is a single digit
        out_day = "0" + str(out_day) if out_day < 10 else str(out_day)
        out_month = "0" + str(out_month) if out_month < 10 else str(out_month)

        # formated date example : 2018_08_20_2018_08_22
        formatted_date = str(in_year) + "_" + in_month + "_" + in_day + "_" + str(
            out_year) + "_" + out_month + "_" + out_day
        print("formatted date ===", formatted_date)
        return formatted_date

    @classmethod
    def get_cityId_fallbackURL(cls,resp):
        for result in resp.json():
            if result['type'] == 'GEO':
                city_id = result['value']
                fallback_url = "https://www.tripadvisor.co.uk" + result['url']
                return city_id,fallback_url


    @classmethod
    def get_uid_sessID(cls,resp):
        uid_start_index = resp.text.find('"uid":"') + len('"uid":"')
        uid_end_index = resp.text.find(',', uid_start_index) - 1
        uid = resp.text[uid_start_index:uid_end_index]

        search_index = resp.text.find('name="searchSessionId"')
        start_index = resp.text.find('value="', search_index) + len('value="')
        end_index = resp.text.find('">', start_index)
        search_session_id = resp.text[start_index:end_index]
        return uid,search_session_id

    @classmethod
    def get_slOpp_plSeed_params(cls,resp):
        search_index = resp.text.find('sl_opp_json')
        start_index = resp.text.find('{', search_index)
        end_index = resp.text.find('}', start_index) + 1

        sl_opp_json_param = resp.text[start_index:end_index]
        sl_opp_json_param = sl_opp_json_param.replace("\\", '')

        plSeed_search_index = resp.text.find('plSeed')
        start_index = resp.text.find(':', plSeed_search_index)
        end_index = resp.text.find(',', start_index)
        plSleed_param = resp.text[start_index:end_index]
        plSleed_param = re.findall(r'[0-9]', plSleed_param)
        plSleed_param = "".join(plSleed_param)
        return sl_opp_json_param, plSleed_param


    def _process_homepage(self):
        _, response, _ = self.get_request(self._clean_host_url, self._get_headers, self.proxy, timeout=10)
        puid, search_session_id = self.__class__.get_uid_sessID(response)

        location_headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US",
            "Host": self.HOST,
            "Cache-Contral": "no-cache",
            "Connection": "Keep-Alive",
            "Referer": self._clean_host_url,
            "X-Puid": puid,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        location_url = self._clean_host_url+"/TypeAheadJson?action=API&types=geo%2Cnbrhd%2Chotel%2Ctheme_park&filter=&legacy_format=true&urlList=true&strictParent=true&query={0}&max=6&name_depth=3&interleaved=true&scoreThreshold=0.5&strictAnd=false&typeahead1_5=true&disableMaxGroupSize=true&geoBoostFix=true&geoPages=&injectList=&neighborhood_geos=true&details=true&link_type=hotel%2Cvr%2Ceat%2Cattr&rescue=true&uiOrigin=trip_search_Hotels&source=trip_search_Hotels&startTime={1}&searchSessionId={2}&nearPages=true&supportedSearchTypes=".format(
            self.city, int(datetime.datetime.now().timestamp()), search_session_id)

        _, location_resp, _ = self.get_request(location_url, location_headers, self.proxy, timeout=10)
        city_id, fallback_url = self.__class__.get_cityId_fallbackURL(location_resp)
        print(city_id, fallback_url)



        set_date_headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": self.HOST,
            "Pragma": "no-cache",
            "Proxy-Connection": "Keep-Alive",
            "Referer": fallback_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        set_date_url = self._clean_host_url + "/UpdateSessionDatesAjax"
        foramtted_date = self.__class__.get_formatted_date(self.check_in, self.check_out)
        post_data = {"staydates": foramtted_date}

        _, set_date_resp, _ = self.__class__.post_request(set_date_url, set_date_headers, self.proxy, post_data, body_type='url_string')

        first_page_headers = {
            "Accept": "text/html,application/xhtml+xml,*/*",
            "Accept-Language": "en-US",
            "Cookie": set_date_resp.headers['Set-Cookie'],
            "Proxy-Connection": "Keep-Alive",
            "Refer": self._clean_host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
        }

        _, list_home_page_resp, _ = self.get_request(fallback_url, first_page_headers, self.proxy,timeout=10)

        # with open("list_home_page.html", 'w', encoding='utf-8') as file:
        #     file.write(list_home_page_resp.text)


        sl_opp_param, plSeed_param = self.__class__.get_slOpp_plSeed_params(list_home_page_resp)

        tree = html.fromstring(list_home_page_resp.text)
        no_of_hotelsPerPage = tree.xpath(tripadvisor_config.hotels_perpage_xpath)

        no_of_pages = tree.xpath(tripadvisor_config.pagination_xpath1)
        if len(no_of_pages) < 1:
            no_of_pages = tree.xpath(tripadvisor_config.pagination_xpath2)
        no_of_pages = int(no_of_pages[0]) if no_of_pages else 0

        list_page_headers = {
            "Accept": "text/html, */*",
            "Accept-Language": "en-US",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "www.tripadvisor.co.uk",
            "Pragma": "no-cache",
            "Proxy-Connection": "Keep-Alive",
            "Referer": fallback_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
            "X-Puid": puid,
            "cookie": list_home_page_resp.headers['Set-Cookie'],
            'x-requested-with': 'XMLHttpRequest',
        }

        offset = 0
        hotel_urls_list = []

        for page in range(no_of_pages):
            # time.sleep(random.choice([1, 2, 3, 4, 5]))
            payload_data = {
                "sl_opp_json": sl_opp_param,
                'staydates': foramtted_date,
                "plSeed": plSeed_param,
                "showSnippets": False,
                "offset": offset,
                "reqNum": "1",
                "changeSet": 'TRAVEL_INFO',  # "MAIN_META,PAGE_OFFSET", #
                "puid": puid,
            }

            _, list_page_resp, _ = self.__class__.post_request(fallback_url, list_page_headers, self.proxy, payload_data,
                                                              body_type='url_string')

            # filename = "tripadvisor_listpage{0}.html".format(page)
            # with open(filename, 'w', encoding='utf-8') as file:
            #     file.write(list_page_response.text)

            hotel_headers = {
                "Authority": "www.tripadvisor.co.uk",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "max-age=0",
                "Cookie": list_page_resp.headers['Set-Cookie'],
                "Referer": fallback_url,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            }

            tree = html.fromstring(list_page_resp.text)
            partial_urls_list = tree.xpath(tripadvisor_config.hotel_urls_xpath)

            hotel_urls = ["https://www.tripadvisor.co.uk" + partial_url for partial_url in partial_urls_list]
            hotel_urls = list(set(hotel_urls))  # remove duplicates hotel urls if any
            url_header = (hotel_urls, hotel_headers)

            hotel_urls_list.append(url_header)

            offset += len(no_of_hotelsPerPage)

        return hotel_urls_list

    @property
    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """

        headers = {
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US',
            "Connection": "Keep-Alive",
            'Host': self.HOST,
            'User-Agent': self.user_agent.strip(),
        }

        return headers


class TripadvisorHotel(HotelHandler):

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


def crawl_hotels(consumer_data, redelivered):
    return TripAdvisorLandingPage(consumer_data).crawl_hotels(redelivered)


sample = {
    "requestId": "12",
    "subRequestId": "1",
    "requestRunId": "",
    "domainName": "https://www.tripadvisor.co.uk/",
    "country": "United Kingdom",
    "RequestInputs": {
        "city": "London",
        "children": "",
        "adults": 2,
        "room": 1,
        "board": "",
        "checkIn": datetime.datetime.now(),
        "checkOut": "",
        "nights": 3,
        "days": 7,
        "hotelName": "",
        "starRating": "",
        "webSiteHotelId": "",
        "pos": "",
        "crawlMode": ""
    }
}

#
#
#
# hotels = crawl_hotels(sample)
#
# from param_parser import ParserTripadvisorPython
#
# for h in hotels:
#
#     obj = ParserTripadvisorPython.crawl_hotels(h)
#     print(obj)
#
