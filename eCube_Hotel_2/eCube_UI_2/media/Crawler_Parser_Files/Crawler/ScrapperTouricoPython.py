import datetime
import json
import requests
import pandas as pd
import time
import re
import string
from datetime import timedelta
from lxml import etree, html
from copy import deepcopy
import copy
# from scripts import tourico_config
# from scripts.core import exceptions
# from scripts.core.logs import CrawlingLogger
# from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler

from Crawling.scripts.Hotelbeds import tourico_config
from Crawling.scripts.core import exceptions
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler


class TouricoLogger(CrawlingLogger):
    NAME = 'tourico_crawling'

TouricoLogger.set_logger()
CrawlerBase.TRL = TouricoLogger
CrawlerBase.CONFIG_FILE = tourico_config


class TouricoHotel(HotelHandler):

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        pageHtml = html.fromstring(self._html['html_element'].encode('utf-8'))

        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0])

    @property
    def _get_cache_page(self):
        selling_page=self._html['html_element']
        return selling_page

    @property
    def _get_cost_page(self):
        cost_page = self._html['cost_page_html_element']
        return cost_page

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': self._landing_page._html}

    @property
    def _get_room_types(self):
        roomType = self._html
        price = None
        return {'roomTypeHTML': roomType, 'priceHTML':price}

    @classmethod
    def get_hotel(cls, hotel_url, latitude_url, landing_page):
        cost_elem=hotel_url[1]
        hotel_url=hotel_url[0]
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers())

        # from pdb import set_trace; set_trace()
        # resp_html, response, _ = cls.get_request(cls.complete_hotel_url(hotel_url, landing_page.domain), headers, proxy, cookie=cookie)
        resp_html = str(etree.tostring(hotel_url))
        if cost_elem == 'Not found':
            html_elem = {'html_element': resp_html, 'latitude_html': None, 'cost_page_html_element': None}
        else:
            html_elem = {'html_element': resp_html, 'latitude_html': None, 'cost_page_html_element':str(etree.tostring(cost_elem))}
        return cls(landing_page, html_elem)

    def save_html(self, index):
        hotel_data = dict()
        meta_data = dict()
        if self._landing_page.adults==2:
            adultvalue='2 Adt'
        # Properties from Parent
        hotel_data['index'] = index
        hotel_data['hotel_count'] = self.hotel_count
        hotel_data['city'] = self.city
        hotel_data['country'] = self.country
        hotel_data['city_zone'] = self._get_city_zone
        hotel_data['checkIn'] = str(self.check_in)
        hotel_data['checkOut'] = str(self.check_out)
        hotel_data['pos'] = self._landing_page.pos
        hotel_data['adults'] = adultvalue

        # Crawler Output
        hotel_data['htmls'] = self._get_html
        try:
            hotel_data['hotelName'] = self._get_name
        except Exception as e:
            raise self.EXCEPTIONS['HOTEL_NOT_FOUND'](str(e))
        hotel_data['roomTypes'] = self._get_room_types
        hotel_data['cachePageHTML'] = self._get_cache_page
        hotel_data['supplier_costpage'] = self._get_cost_page
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
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers())
        hotel_data['meta']['cachePageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cache_page
        )
        self.TRL.debug_log(
            'Saving Hotel:%s' % self._get_name, self._landing_page.request_id, self._landing_page.sub_request_id,
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers())
        hotel_data['meta']['supplier_hotel_url'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cost_page
        )

        # return self.SERVICE_CALLS['save_html'](hotel_data)
        response = copy.deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)


class TouricoLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.Hotelbeds.com'
    HOTEL_HANDLER_CLASS = TouricoHotel
    HOTEL_LIST_DRIVER = False
    PROXY_LESS_HIT = True


    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        # No hotel links are returned, hence passing a blank list
        all_hotels_selling=[]
        all_hotels_cost=[]

        dict={}
        for xml_c in self._html['cost']:
            lxml__elem_cost = etree.fromstring(xml_c)
            hotels_cost = lxml__elem_cost.xpath(self.CONFIG_FILE.hotelLinksXpath)
            for hotel_c in hotels_cost:
                hotel_code_c = hotel_c.xpath(self.CONFIG_FILE.hotelcodeXpath)[0]
                dict[hotel_code_c]=hotel_c

        for xml in self._html['selling']:
            lxml__elem_selling = etree.fromstring(xml)
            hotels_selling = lxml__elem_selling.xpath(self.CONFIG_FILE.hotelLinksXpath)
            for hotel in hotels_selling:
                hotel_code = hotel.xpath(self.CONFIG_FILE.hotelcodeXpath)[0]
                all_hotels_selling.append(hotel)
                if hotel_code in dict:
                    all_hotels_cost.append(dict[hotel_code])
                else:
                    all_hotels_cost.append('Not found')

            # all_hotels_selling.extend(hotels_selling)
            # all_hotels_cost.extend(hotels_cost)
        self.hotel_count = len(all_hotels_selling)
        all_hotels={'selling':all_hotels_selling, 'cost':all_hotels_cost}
        return all_hotels

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        return [self._clean_host_url + lt for lt in html.fromstring(str(self._html)).xpath(self.CONFIG_FILE.latLongXpath)]

    @property
    def _get_url_params(self):

        return {}

    def _url_maker(self):
        self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id, self.request_run_id)
        self.TRL.debug_log('Params:%s' % self._get_url_params, self.request_id, self.sub_request_id, self.request_run_id)
        return 'http://thfwsv3.touricoholidays.com/HotelFlow.svc/bas'


    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        # from pdb import set_trace; set_trace()
        pass


    def _process_homepage(self):
        pass

    # @property
    def _get_headers(self, encrypt=False):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        headers = {"SOAPAction": "http://tourico.com/webservices/hotelv3/IHotelFlow/SearchHotelsByDestinationIds",
                   "Content-Type": "text/xml;charset=UTF-8",
                   "Host": "demo-hotelws.touricoholidays.com",
                   "User-Agent": "Apache-HttpClient/4.1.1 (java 1.5)"}
        return headers

    def _get_hotel_list(self, url=None):
        if not url:
            link = self._url_maker()
        elif isinstance(url, str):
            link = url
        elif callable(url):
            link = url(self)
        else:
            self.TRL.error_log('Invalid URL to get Hotel List', self.request_id, self.sub_request_id,
                               self.request_run_id)
            raise self.EXCEPTIONS['INVALID_URL']

        # from pdb import set_trace; set_trace()
        # print("self.proxy.address")
        # print(self.proxy.address)

        pos = self.pos
        # outAirport = self.toAirport
        # inAirport = self.fromAirport

        xmls_selling=[]
        xmls_cost=[]
        payloads = self.get_request_xml_string
        for payload in payloads['selling_price']:
            resp, resp_obj, _ = self.post_request_without_proxy(link, self._get_headers(), body=payload, driver=self.HOTEL_LIST_DRIVER)
            xmls_selling.append(resp)
            costprice_payload = list(payloads['cost_price'])[list(payloads['selling_price']).index(payload)]
            resp, resp_obj, _ = self.post_request_without_proxy(link, self._get_headers(), body=costprice_payload,
                                                  driver=self.HOTEL_LIST_DRIVER)
            xmls_cost.append(resp)

        xmls_dict={'selling':xmls_selling, 'cost':xmls_cost}
        self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
        request_type = RequestHandler._get_request_type()
        if request_type['driver']:
            self._set_cookie(_)
        else:
            self._set_cookie(resp_obj)

        self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return xmls_dict

    @classmethod
    def post_request(cls, url, headers, proxy, body, body_type='url_string', cookie=None, timeout=10, driver=False):

        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, proxy=proxy, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, proxy=proxy, headers=headers)
        driver_obj = None
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:
            param_dict = {
                'url': url,
                'data': json.dumps(body) if body_type == 'json' else body,
                # 'proxies': proxy.to_python('http'),
                'headers': headers,
                # 'timeout': timeout,
            }
            if cookie:
                param_dict['cookies'] = cookie

            response = requests.post(**param_dict)
            res_html = response.content
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj


    @classmethod
    def get_request(cls, url, headers, proxy, cookie=None, timeout=10, driver=False):

        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, proxy=proxy, headers=headers)
        cls.TRL.debug_log('Request Type:%s' % request_type, proxy=proxy, headers=headers)
        driver_obj = None

        # from pdb import set_trace; set_trace()
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:

            if '192.168.6.1' in url:
                response = requests.get(url, timeout=timeout)
            else:
                if cookie:
                    response = requests.get(url, proxies=proxy.to_python('http'), timeout=timeout)
                else:
                    response = requests.get(url, proxies=proxy.to_python('http'), timeout=timeout)

            res_html = response.content
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj

    @property
    def get_request_xml_string(self):
        mapping = self.get_destID_mapping


        for mapped_city in mapping:
            # print(mapped_city)
            if self.city.lower() == mapped_city.lower():
                dest_ids = str(mapping[mapped_city]).split('|')
        # self.check_out=self.check_in + timedelta(self.nights)
        # self.check_out=(datetime.datetime.strptime(self.check_in, '%Y-%m-%d') + timedelta(self.nights))
        # self.check_in1=datetime.datetime.strptime(self.check_in,'%Y-%m-%d')

        yy1, mm1, dd1 = self.set_checkIn(inDate=self.check_in)
        yy2, mm2, dd2 = self.set_checkOut(outDate=self.check_out)
        if len(str(mm1)) == 1:
            mm1 = "0" + str(mm1)
        if len(str(dd1)) == 1:
            dd1 = "0" + str(dd1)
        if len(str(mm2)) == 1:
            mm2 = "0" + str(mm2)
        if len(str(dd2)) == 1:
            dd2 = "0" + str(dd2)

        payload_selling_price=[]
        payload_cost_price=[]
        for dest_id in dest_ids:
            payload = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ' \
                  'xmlns:aut="http://schemas.tourico.com/webservices/authentication" ' \
                  'xmlns:hot="http://tourico.com/webservices/hotelv3" ' \
                  'xmlns:hot1="http://schemas.tourico.com/webservices/hotelv3">' \
                  '<soapenv:Header>' \
                  '<aut:AuthenticationHeader>' \
                  '<aut:LoginName>{}</aut:LoginName>' \
                  '<aut:Password>{}</aut:Password>' \
                  '<aut:Culture>en_US</aut:Culture>' \
                  '<aut:Version>8</aut:Version></aut:AuthenticationHeader></soapenv:Header>' \
                  '<soapenv:Body><hot:SearchHotelsByDestinationIds><!--Optional:--><hot:request>' \
                  '<hot1:DestinationIdsInfo>' \
                  '<hot1:DestinationIdInfo id="{}"/></hot1:DestinationIdsInfo>' \
                  '<hot1:CheckIn>{}-{}-{}</hot1:CheckIn>' \
                  '<hot1:CheckOut>{}-{}-{}</hot1:CheckOut>' \
                  '<hot1:RoomsInformation><hot1:RoomInfo>' \
                  '<hot1:AdultNum>{}</hot1:AdultNum>' \
                  '<hot1:ChildNum>{}</hot1:ChildNum>' \
                  '<hot1:ChildAges><hot1:ChildAge age="{}"/></hot1:ChildAges></hot1:RoomInfo></hot1:RoomsInformation>' \
                  '<hot1:MaxPrice>0</hot1:MaxPrice><hot1:StarLevel>0</hot1:StarLevel>' \
                  '<hot1:AvailableOnly>true</hot1:AvailableOnly>' \
                  '<hot1:PropertyType>Hotel</hot1:PropertyType>' \
                  '<hot1:ExactDestination>true</hot1:ExactDestination></hot:request></hot:SearchHotelsByDestinationIds>' \
                  '</soapenv:Body></soapenv:Envelope>'
            payload_selling_price.append(payload.format('Hot10736','uGpbS8d@',dest_id, yy1, mm1, dd1, yy2, mm2, dd2, self.adults, self.children,
                                                              0))
            payload_cost_price.append(payload.format('Hot10735','W9T@tCms',dest_id, yy1, mm1, dd1, yy2, mm2, dd2, self.adults, self.children,
                                                              0))
        payload_dict = {'selling_price':payload_selling_price, 'cost_price':payload_cost_price}

        return payload_dict

    @property
    def get_destID_mapping(self):
        # url = 'https://192.168.4.217/hotelbeds/TouricoXML_Destinations.html'
        url='http://10.100.18.88/connector_files/TouricoXML_Destinations.html'
        # proxies = {'http': 'http://216.227.130.3:80',
        #            'https': 'https://216.227.130.3:80'}
        res = requests.get(url, verify=False)
        # res=self.get_request_without_proxy(RequestHandler,url=url)
        resp = res.text.replace('=', ':').replace(")", '"').replace('(', '"')
        resp_new = re.sub(r'\n', ', "', resp)
        resp_new = resp_new.replace('"and', 'and').replace('vicinity"', 'vicinity').replace('"Essex County"',
                                                                                            'Essex County')
        resp_new = '"' + resp_new.replace(' : "', '" : "').replace('"Madras"', 'Madras').replace('"Saigon"',
                                                                                                 'Saigon').replace(
            '"BW"', 'BW').replace('"Cadiz"', 'Cadiz').replace('Luz "Huelva"', 'Luz Huelva')
        # resp_new=resp_new.replace(" ","")
        resp_new = eval('{' + resp_new[:-2] + '}')
        # resp_new={'Mumbai' : "119750|7014"}
        # resp_new={"New Orleans - LA" : "26491|26186|24542|24353|23380|19389|19259|18950|13542|13382|13361|13119|12337|11771|11770|7254"}
        return resp_new

    def set_checkIn(self, inDate):
        try:
            inYear=inDate.year
            inDay = inDate.day
            inMonth = inDate.month
            # inDay, inMonth, inYear = inDate.split('/')
        except:
            pass
        # try:
        #     inDay, inMonth, inYear = inDate.split('/')
        # except:
        #     pass
        # try:
        #     inDay, inMonth, inYear = inDate.split('-')
        # except:
        #     pass
        # try:
        #     inDay, inMonth, inYear = inDate.split(':')
        # except:
        #     pass
        # try:
        #     inDay, inMonth, inYear = inDate.split('.')
        # except:
        #     pass
        return inYear, inMonth, inDay


    def set_checkOut(self, outDate):
        try:
            outYear = outDate.year
            outDay = outDate.day
            outMonth = outDate.month
            # inDay, inMonth, inYear = inDate.split('/')
        except:
            pass
        # try:
        #     outDay, outMonth, outYear = outDate.split('/')
        # except:
        #     pass
        # try:
        #     outDay, outMonth, outYear = outDate.split('-')
        # except:
        #     pass
        # try:
        #     outDay, outMonth, outYear = outDate.split(':')
        # except:
        #     pass
        # try:
        #     outDay, outMonth, outYear = outDate.split('.')
        # except:
        #     pass
        return outYear, outMonth, outDay


    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = self._get_hotel_list()



    def _save_hotel(self, index, hotel_url):
        latitude_url = None
        cost_url = hotel_url[1]
        hotel_url=hotel_url[0]
        self.TRL.debug_log('Making Hotel for URL:%s' % hotel_url, self.request_id, self.sub_request_id, self.request_run_id)

        if self.hotels_id_dict is not None:
            self._set_hotel_web_id(self.hotels_id_dict[index])

        hotel_url=(hotel_url,cost_url)
        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(hotel_url, latitude_url, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        # hotel_data = hotel.save_html(index)
        return hotel.save_html(index)

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
            raise self.EXCEPTIONS['SCRIPT_TIMEOUT']

        self.TRL.debug_log('Hotels Found:%s' % len(self._hotels), self.request_id, self.sub_request_id, self.request_run_id)
        crawled_hotels = partial_hotels
        hotels_count = len(crawled_hotels)
        # crawled_hotels = [self._save_hotel(i, hotel_url) for i, hotel_url in enumerate(self._hotels[:1])]
        selling_url= self._hotels['selling']
        for i, hotel_url in enumerate(selling_url):
            i += hotels_count
            hotel_url=(hotel_url, list(self._hotels['cost'])[list(selling_url).index(hotel_url)])
            # hotel = self._save_hotel(i, hotel_url)
            # crawled_hotels.append(hotel)
            try:
                hotel = self._save_hotel(i, hotel_url)
                crawled_hotels.append(i)
                self.SERVICE_CALLS['increase_completed_hotel_count']()
            except self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']:
                pass
            except (
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ProxyError
            ) as e:
                self.request_data.update({'hotels': crawled_hotels})
                self.SERVICE_CALLS['save_partial_hotels'](self.request_data, str(e))
                raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
            # except self.HOTEL_HANDLER_CLASS.EXCEPTIONS['HOTEL_NOT_FOUND']:
            #     pass
        self.request_data.update({'hotels': crawled_hotels})
        return self.request_data


def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()

    crawled_data = TouricoLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    return crawled_data


# sample = {
#     "requestId": "12",
#     "subRequestId": "1",
#     "requestRunId": "",
#     "DomainName": "http://www.starwood.com",
#     "country": "Louisiana",
#     "RequestInputs": {
#         "fromAirport": "",
#         "toAirport":"",
#         "city": "New Orleans - LA",
#         "children": "0",
#         "children_age":"0",
#         "adults": 2,
#         "room": 1,
#         "board": "",
#         "checkIn":"2018-11-28",
#         "checkOut": "",
#         "nights": 2,
#         "days": 0,
#         "hotelName": "",
#         "starRating": "",
#         "webSiteHotelId": "",
#         "pos": "Spain",
#         "crawlMode": ""
#     }
# }
#
#
# hotels = crawl_hotels(sample, False)
# # print(hotels)
# #
#
# # crawled_hotels = crawl_hotels(sample,False)
# # with open("Tourico.json", "w", encoding="utf-8") as file:
# #     file.write(json.dumps(hotels,indent=4))
# # print(hotels)
# # #
# # with open("Tourico.json", 'r') as f:
# #     crawled_hotels = json.load(f)
# #
# from AetosParsingService.scripts import ParserTouricoPython
# parsed_data = ParserTouricoPython.crawl_hotels(hotels)
#
# # for h in hotels:
# #
# #     obj = ParserStarwoodPython.crawl_hotels(h)
# #     print(obj)
# with open("Tourico.json", "w", encoding="utf-8") as file:
#     file.write(json.dumps(parsed_data,indent=4))