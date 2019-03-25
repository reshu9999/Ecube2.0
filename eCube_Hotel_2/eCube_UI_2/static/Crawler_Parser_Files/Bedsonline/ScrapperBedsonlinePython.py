import datetime
import math
import requests
import copy
import json
import hashlib
import time
from lxml import html,etree
from Crawling.scripts.Hotelbeds_Availability import ScrapperConfigBedsonlinePython
#from Crawling.scripts import ScrapperBedsOnlineCurrencyMaster

from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler



# from scripts import scrapper_bedsonline_config,ScrapperBedsOnlineCurrencyMaster
#
# from scripts.core.logs import CrawlingLogger
# from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler

class BedsOnlineLogger(CrawlingLogger):
    NAME = 'bedsonline_crawling'


BedsOnlineLogger.set_logger()
CrawlerBase.TRL = BedsOnlineLogger
CrawlerBase.CONFIG_FILE = ScrapperConfigBedsonlinePython

class BedsOnlineRequestHandler(RequestHandler):

    @classmethod
    def post_request_without_proxy(cls, url, headers, body, body_type='url_string', cookie=None, timeout=60,
                                   driver=False):
        """
        :param url:
        :param headers:
        :param body: Post body
        :param body_type: url_string or json
        :param cookie:
        :param timeout:
        :return: response html and response object
        """
        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, headers=headers)
        driver_obj = None
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            # options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            # driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:
            param_dict = {
                'url': url,
                'data': json.dumps(body) if body_type == 'json' else body,
                'headers': headers,
                'timeout': timeout,
            }
            if cookie:
                param_dict['cookies'] = cookie

            response = requests.post(**param_dict)

            res_html = response.content
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj



class BedsOnlineHotel(HotelHandler):

    @property
    def _get_cache_page(self):
        return self._html['hotel_html']

    @classmethod
    def get_hotel(cls, index, hotel_element, landing_page):

        html_elem = {'hotel_html': str(etree.tostring(hotel_element).decode("utf-8")),
                     'latitude_html': None}
        return cls(landing_page, html_elem)

    def save_html(self, index,dest_code,hotelchain_val):
        hotel_data = dict()
        meta_data = dict()
        if self._landing_page.adults == 2:
            Adult_val = "2 Adt"
        elif self._landing_page.adults == 4:
            Adult_val = "2 Adt 2 Child"
        elif self._landing_page.adults == 3:
            Adult_val = "3 Adt"
        else:
            Adult_val = "1 Adt"
        # Properties from Parent
        hotel_data['index'] = index
        hotel_data['hotel_count'] = self.hotel_count
        hotel_data['city'] = self.city
        hotel_data['country'] = self.country
        hotel_data['city_zone'] = str(dest_code)
        hotel_data['checkIn'] = str(self.check_in)
        hotel_data['checkOut'] = str(self.check_out)
        hotel_data['adults'] = str(Adult_val)
        hotel_data['HotelChain_value'] = str(hotelchain_val)

        # Crawler Output
        hotel_data['htmls'] = self._get_html
        try:
            hotel_data['hotelName'] = self._get_name
        except Exception as e:
            raise self.EXCEPTIONS['HOTEL_NOT_FOUND'](str(e))
        hotel_data['roomTypes'] = self._get_room_types
        hotel_data['cachePageHTML'] = self._get_cache_page
        hotel_data['hotel_id'] = self._landing_page.hotel_web_id

        # Meta Data
        meta_data['requestId'] = self._landing_page.request_id
        meta_data['cachePageToken'] = self._get_cache_filename
        meta_data['subRequestId'] = self._landing_page.sub_request_id
        meta_data['requestRunId'] = self._landing_page.request_run_id
        meta_data['startDT'] = str(self.start_time)
        meta_data['endDT'] = str(datetime.datetime.now())
        hotel_data['meta'] = meta_data

        self.TRL.debug_log(
            'Saving Hotel:%s' % self._get_name, self._landing_page.request_id, self._landing_page.sub_request_id,
            self._landing_page.request_run_id, proxy=None, headers=self._landing_page.headers)
        hotel_data['meta']['cachePageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cache_page
        )
        # return self.SERVICE_CALLS['save_html'](hotel_data)
        response = copy.deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        pageHtml = html.fromstring(self._html['hotel_html'])
        print("hotel_name=====",pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath))
        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()


    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': self._html}

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """
        # room_details = html.fromstring(str(self._html['html_element'])).xpath(self.CONFIG_FILE.roomDetailsInContainersXpath)

        return {'roomTypeHTML': self._html['hotel_html'], 'priceHTML': None}



class BedsOnlineLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.hotelopia.com'
    HOTEL_HANDLER_CLASS = BedsOnlineHotel
    # PROXY_VENDOR_WISE = None
    # PROXY_POS_WISE = None
    PROXY_LESS_HIT = True

    # def __init__(self, requeset_data):
    #     super(BedsOnlineLandingPage, self).__init__(requeset_data)
    #     proxy = BedsOnlineProxyHandler()
    #     proxy.initiate_new_proxy(self.domain_name, self.country)
    #     self.proxy = proxy

    def _url_maker(self):
        # self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id, self.request_run_id)
        return "https://api.hotelbeds.com/hotel-api/1.0/hotels"



    @classmethod
    def get_formatted_date(cls, datetime_obj):
        # print("datetime_obj====", datetime_obj)
        year = str(datetime_obj.year)
        month = datetime_obj.month
        month = "0" + str(month) if month < 10 else str(month)
        day = datetime_obj.day
        day = "0" + str(day) if day < 10 else str(day)
        date_str = year +"-"+ month +"-"+ day
        return date_str


    def get_payload(self):
        # url = "https://ecxus301.eclerx.com/HotelBedsAvailibilityReport/ui/matchingdll/primaryhotel.aspx?strCountry={0}&strCity={1}".format(
        #     self.country.upper(), self.city.upper())
        url = "https://192.168.6.1/HotelBedsAvailibilityReport/ui/matchingdll/primaryhotel.aspx?strCountry={0}&strCity={1}".format(
                self.country.upper(), self.city.upper())

        # url = "http://10.100.18.86:8001/api/v1/GetMatchingPrimaryHotels?city={0}&country={1}".format(
        #     self.city.upper(), self.country.upper())
        resp_text = requests.get(url, verify=False)
        resp_text1 = resp_text.text.replace('{"ResultData":"', '').replace(
            '<?xml version=\\"1.0\\" encoding=\\"UTF-8\\" ?>', '').replace('","StatusCode":200}', '')
        resp_text1=resp_text1.replace("<nvcrHotelChain />","<nvcrHotelChain>None</nvcrHotelChain>")

        self.hotel_ids = etree.fromstring(resp_text1).xpath(self.CONFIG_FILE.hotelCodesXpath)
        self.hotelchain_val = etree.fromstring(resp_text1).xpath(self.CONFIG_FILE.Hotel_chainXpath)
        hotel_str = "".join(["<hotel>{0}</hotel>".format(hotelId) for hotelId in self.hotel_ids])
        # print("hotel_str===",hotel_str)

        # currency, sourceMarket = ScrapperBedsOnlineCurrencyMaster.getMasterCurrency(self.city, self.pos)
        currency, sourceMarket = ScrapperConfigBedsonlinePython.getMasterCurrency(self.city, self.pos)

        formatted_checkIn = self.get_formatted_date(self.check_in)
        formatted_checkOut = self.get_formatted_date(self.check_out)

        head_str = """<availabilityRQ
            xmlns="http://www.hotelbeds.com/schemas/messages"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" sourceMarket="{0}" Currency="{1}">
            <stay checkIn="{2}" checkOut="{3}" />""".format(sourceMarket, currency, formatted_checkIn,
                                                            formatted_checkOut)

        occupancy_str = """<occupancies>
                <occupancy rooms="{0}" adults="{1}" children="{2}"></occupancy>
            </occupancies>""".format(self.room or 1, self.adults, self.children)

        body_str = occupancy_str + "<hotels>{0}</hotels>".format(hotel_str)

        tail_str = "</availabilityRQ>"

        payload_data = head_str + body_str + tail_str

        return payload_data


    # def getSHASignature(self, APIKey, secretKey):
    #     epochTime = int(datetime.datetime.now().timestamp())
    #     signature_temp = APIKey + secretKey + str(epochTime)
    #
    #     sha_url = "http://www.convertstring.com/Hash/SHA256"
    #     sha_post_data = "InputOptions.Salt=&InputOptions.Type=ConvertString.Model.Tool.Options.HashInputOptions&InputOptions.Type=ConvertString.Model.Tool.Options.HashInputOptions&input={0}&outputtype=outputstring".format(
    #         signature_temp)
    #     sha_headers = {
    #         "Host": "www.convertstring.com",
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    #     }
    #
    #     sha_resp_text, resp_obj, _ = BedsOnlineRequestHandler.post_request(sha_url, sha_headers, self.proxy, sha_post_data, driver=self.HOTEL_LIST_DRIVER)
    #
    #     # print("sha_response====\n\n", sha_resp_text)
    #     sha_signature = html.fromstring(sha_resp_text).xpath(self.CONFIG_FILE.shaSignatureXpath)[0]
    #     return sha_signature


    def getSHASignature(self, APIKey, secretKey):
        epochTime = int(datetime.datetime.now().timestamp())
        signature_temp = APIKey + secretKey + str(epochTime)
        sha_signature = hashlib.sha256(signature_temp.encode('utf-8')).hexdigest()

        return sha_signature



    @property
    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """

        headers = {
            "Accept": "application/xml",
            "Content-Type": "application/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }

        return headers


    def _get_hotel_list(self, url=None):
        if not url:
            link = self._url_maker()
        elif isinstance(url, str):
            link = url
        elif callable(url):
            link = url(self)
        else:
            self.TRL.error_log('Invalid URL to get Hotel List', self.request_id, self.sub_request_id, self.request_run_id)
            raise self.EXCEPTIONS['INVALID_URL']

        # from pdb import set_trace; set_trace()
        # print("self.proxy.address")
        # print(self.proxy.address)
        payload = self.get_payload()

        APIKey, secretKey = ScrapperConfigBedsonlinePython.getAPIKey(self.pos)
        sha_signature = self.getSHASignature(APIKey, secretKey)

        headers = {
            "Api-Key": APIKey,
            "X-Signature": sha_signature,
            "Accept": "application/xml",
            "Content-Type": "application/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }

        # try:
        #     self.proxy.check_proxy(link, headers, payload)
        # except (
        #     ProxyHandler.EXCEPTIONS['SERVER_DOWN_ERROR'],
        #     ProxyHandler.EXCEPTIONS['SERVER_ERROR'],
        #     ProxyHandler.EXCEPTIONS['PNF_ERROR'],
        #     ProxyHandler.EXCEPTIONS['PROXY_AUTH_ERROR'],
        #     ProxyHandler.EXCEPTIONS['REQUEST_ERROR']
        # ) as e:
        #     self.TRL.error_log(
        #         'No Working Proxy Found:%s' % str(e), self.request_id, self.sub_request_id, self.request_run_id,
        #         headers=self.headers)
        #     raise ProxyHandler.EXCEPTIONS['NOT_WORKING']

        resp_xml, resp_obj, _ = BedsOnlineRequestHandler.post_request_without_proxy(link, headers, payload, driver=self.HOTEL_LIST_DRIVER)

        self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
        request_type = RequestHandler._get_request_type()
        if request_type['driver']:
            self._set_cookie(_)
        else:
            self._set_cookie(resp_obj)

        self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return resp_xml


    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        # partial_links_list = self._html['lxmlELEM'].xpath(self.CONFIG_FILE.hotelLinksXpath) #old template code
        hotels = self._html.xpath(self.CONFIG_FILE.hotelXpath)
        print("len hotels====",len(hotels))
        self.hotel_count = len(hotels)
        return hotels


    def _save_hotel(self, index, hotel_element,zone_index,hotelchain_val):
        # self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url, self.request_id, self.sub_request_id, self.request_run_id)
        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(index, hotel_element, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        dest_code = self._html.xpath(self.CONFIG_FILE.hotel_ZoneName)[0]
        dest_code = str(dest_code) + "_" + str(zone_index)
        #hotel_data = hotel.save_html(index, dest_code)
        # hotel_data = hotel.save_html(index)
        return hotel.save_html(index, dest_code,hotelchain_val)


    classmethod
    def get_hotel_chain_val(cls, hotelid, hotel_data_val):
        for hotel_id, chain_val in hotel_data_val:
            if hotel_id == hotelid:
                return chain_val
        return None


    def crawl_hotels(self, redelivered):
        # redelivered = False
        partial_hotels = list()
        if redelivered:
            partial_hotels = self.SERVICE_CALLS['get_partial_hotels'](self.sub_request_id)
            print('crawled_hotels found')
            print(len(partial_hotels))

        self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
        # self._set_html()
        try:
            self._set_html()
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ProxyError
        ) as e:
            print("Ecrrrrrrrrrrrrrrr\n",e,"\n-----------------------")
            raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
        hotels = self._hotels
        self.TRL.debug_log('Hotels Found:%s' % len(hotels), self.request_id, self.sub_request_id, self.request_run_id)
        crawled_hotels = partial_hotels
        hotels_count = len(crawled_hotels)
        # crawled_hotels = [self._save_hotel(i, hotel_url) for i, hotel_url in enumerate(self._hotels[:1])]
        hotel_data_val = list(zip(self.hotel_ids, self.hotelchain_val))

        # for i, hotel_element in enumerate(hotels[hotels_count:]):
        zone_count = math.ceil(len(self._hotels) / 200)
        zone_count = zone_count + 1
        i = 0
        for zone_index in range(zone_count):
            zone_index = zone_index + 1
            if zone_index > 1:
                hotels_count = xx
            xx = 200 * zone_index
            # for i, hotel_url in enumerate(self._hotels[hotels_count:xx]):
            for hote_data in self._hotels[hotels_count:xx]:
            # i += hotels_count
            # hotel = self._save_hotel(i, hotel_url)
            # crawled_hotels.append(hotel)
                hotelid = hote_data.xpath(self.CONFIG_FILE.hotelCodeXpath)[0]
                hotel_chain_val =  self.get_hotel_chain_val(hotelid, hotel_data_val)
                hotel_chain_val = str(hotel_chain_val) if hotel_chain_val!='None' else None
                try:
                    print(i)
                    hotel = self._save_hotel(i, hote_data,zone_index,str(hotel_chain_val))
                    crawled_hotels.append(i)
                    self.SERVICE_CALLS['increase_completed_hotel_count']()
                except (
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.ProxyError
                ) as e:
                    self.request_data.update({'hotels': crawled_hotels})
                    self.SERVICE_CALLS['save_partial_hotels'](self.request_data, str(e))
                    raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
                except self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']:
                    pass
                self.request_data.update({'hotels': crawled_hotels})
                i= i+1
        return self.request_data


    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        self.cookie = cookie_object.cookies.get_dict()


############test bed compatile###############
def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    crawled_data = BedsOnlineLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    return crawled_data


########for debugging normaly##################
# def crawl_hotels(consumer_data, redelivered):
#     import time
#     print('starting crawl')
#     start_time = time.time()
#     checkIn_date = (consumer_data['RequestInputs']['checkIn'] + datetime.timedelta(int(consumer_data['RequestInputs'].get('days', 0))))
#     checkOut_date = checkIn_date + datetime.timedelta(int(consumer_data['RequestInputs']['nights']))
#     consumer_data['RequestInputs']['checkIn'] = checkIn_date
#     consumer_data['RequestInputs']['checkOut'] = checkOut_date
#     crawled_data = BedsOnlineLandingPage(consumer_data).crawl_hotels(redelivered)
#     end_time = time.time()
#     print('total time "%s"' % (end_time - start_time))
#     crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
#     crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
#     crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
#     print('\ncrawling hotels')
#     print(type(crawled_data))
#     return crawled_data


# sample = {
#     "requestId": "12",
#     "subRequestId": "1",
#     "requestRunId": "",
#     "DomainName": "https://api.hotelbeds.com/hotel-api/1.0/hotels",
#     "country": "Spain",
#     "RequestInputs": {
#         "city": "Seville",
#         "children": "",
#         "adults": 2,
#         "room": 1,
#         "board": "",
#         "checkIn": datetime.datetime.now(),
#         "checkOut": "",
#         "nights": 2,
#         "days": 7,
#         "hotelName": "",
#         "starRating": "",
#         "fromAirport": "",
#         "toAirport": "",
#         "webSiteHotelId": "",
#         "pos": "Spain",
#         "crawlMode": ""
#     }
# }



# crawled_hotels = crawl_hotels(sample,False)
# with open("BedsOnlineCrawledData.json","w", encoding="utf-8") as file:
#     file.write(json.dumps(crawled_hotels,indent=4))
# print("Crawled_Data===",crawled_hotels)

#
# with open("BedsOnlineCrawledData.json", 'r') as f:
#     crawled_data = json.load(f)
#
# from AetosParsingService.scripts import ParserBedsOnlinePython
# parsed_data = ParserBedsOnlinePython.crawl_hotels(crawled_data)
# with open("BedsOnlineParsedData.json", "w", encoding="utf-8") as file:
#     file.write(json.dumps(parsed_data, indent=4))
# print("Parsed_data ====",parsed_data)
