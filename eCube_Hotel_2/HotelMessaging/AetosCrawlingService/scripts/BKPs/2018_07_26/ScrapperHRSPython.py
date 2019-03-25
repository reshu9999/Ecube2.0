import json
import requests
from lxml import html, etree
from scripts import hrs_config
from scripts.core import exceptions
from scripts.core.logs import CrawlingLogger
from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler
from scripts.hrs_city_mapping import city_mapper


class HRSLogger(CrawlingLogger):
    NAME = 'hrs_crawling'


HRSLogger.set_logger()
CrawlerBase.TRL = HRSLogger
CrawlerBase.CONFIG_FILE = hrs_config


class HRSHotel(HotelHandler):

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {'landingPage': self._landing_page._html, 'hotelHtml': self._html}

    @property
    def _get_name(self):
        pageHtml = html.fromstring(self._html['html_element'])
        return pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]

    @property #Bhavin
    def _get_cache_page(self):
        return self._html['html_element']

    @property
    def _get_room_types(self):
        # roomDetailsInContainersXpath
        # pricesInContainersXpath
        # pricesInContainersXpath2
        """
        :return: { 'roomtypehtml': 'page_source_of_roomtype',
                   'pricehtml': 'page_source_of_price_for_roomtype',
                   'promotionHTML': 'page_soource_of_promotion_for_roomtype',
                   'boardTypeHTML': 'page_soource_of_promotion_for_boardtype',
                }
        """
        pageHtml = html.fromstring(self._html['html_element'])
        room_dict = {
            # 'roomTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomDetailsInContainersXpath)[0]).decode('utf-8'),
            # 'priceHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.pricesInContainersXpath)[0]).decode('utf-8'),
            # 'promotionHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomPromotion)[0]).decode('utf-8'),
            # 'boardTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomBoardType)[0]).decode('utf-8'),
            # Bhavin
            'roomTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomDetailsInContainersXpath)[0]).decode(
                'utf-8'),
            'priceHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.pricesInContainersXpath)[0]).decode('utf-8'),
            'promotionHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomPromotion)[0]).decode('utf-8'),
            'boardTypeHTML': etree.tostring(pageHtml.xpath(self.CONFIG_FILE.roomBoardType)[0]).decode('utf-8'),
        }
        return room_dict

    @classmethod
    def complete_hotel_url(cls, hotel_url, domain):
        """
        :param: hotel_url as string
        :return: complete hotel url if partial
        """
        if not hotel_url.startswith(domain):
            if hotel_url.startswith('/web3/'):
                hotel_url = '{0}{1}'.format(domain,
                                    hotel_url[6:])
        return hotel_url

    # bhavin.dhimmar
    @classmethod
    def get_hotel(cls, hotel_url, latitude_url, landing_page):
        print('get_hotel called')
        headers = landing_page.headers
        proxy = landing_page.proxy
        cookie = landing_page.cookie
        cls.TRL.debug_log(
            'Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,
            landing_page.request_run_id, proxy=proxy, headers=headers)

        # from pdb import set_trace; set_trace()
        # resp_html, response, _ = cls.get_request(cls.complete_hotel_url(hotel_url, landing_page.domain), headers, proxy, cookie=cookie)
        #bhavin
        resp_html, response, _ = cls.get_request_HeaderLess(cls.complete_hotel_url(hotel_url, landing_page.domain), proxy,
                                                 cookie=cookie)
        html_elem = {'html_element': resp_html, 'latitude_html': cls._get_latitude(latitude_url, proxy, headers, cookie=cookie)}
        return cls(landing_page, html_elem)

    #Bhavin.Dhimmar
    @classmethod
    def get_request_HeaderLess(cls, url, proxy, cookie=None, timeout=10, driver=False):
        """
        :param url:
        :param headers:
        :param proxy:
        :param cookie:
        :param timeout:
        :return: response html and response object
        """
        request_type = cls._get_request_type()
        cls.TRL.debug_log('URL:%s' % url, proxy=proxy, headers=None)
        cls.TRL.debug_log('Request Type:%s' % request_type, proxy=proxy, headers=None)
        driver_obj = None

        # from pdb import set_trace; set_trace()
        if request_type['driver'] and driver:
            options = cls.OPTIONS
            # prxy = "69.39.224.131:80"
            # options.add_argument('--proxy-server=%s' % prxy)
            options.add_argument('--proxy-server=%s' % proxy.to_driver('http'))
            driver = cls.DRIVER_CLASS(executable_path=cls.EXECUTABLE_PATH, chrome_options=options)
            driver.get(url)
            driver_obj = driver

        if request_type['request']:
            if cookie:
                response = requests.get(url, headers=None, proxies=proxy.to_python('http'), timeout=timeout,
                                        cookies=cookie)
            else:
                # response = requests.get(url, headers=headers, proxies=proxy.to_python('http'), timeout=timeout)
                # bhavin
                response = requests.get(url, proxies=proxy.to_python('http'), timeout=timeout)

            res_html = response.text
            res_obj = response
        else:
            raise cls.EXCEPTIONS['INCORRECT_REQUEST_TYPE']

        return res_html, res_obj, driver_obj


class HRSLandingPage(HotelLandingPageHandler):

    HOST = 'https://www.hrs.com/web3/'

    HEADERS = {
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Proxy-Connection": "Keep-Alive",
        "Host": "www.hrs.com",
        "Referer": "https://www.hrs.com/",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    HOTEL_HANDLER_CLASS = HRSHotel

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        HRSLandingPage.HEADERS["Host"] = "osc.hrs.com"
        HRSLandingPage.HEADERS['Referer'] = "https://www.hrs.com/web3/searchWeb1000.do?activity=showHotellistWithPromotion&showOverlay=true&clientId={0}--&cid={1}".format(
                                                self.client_id,
                                                self.cid
                                            )

        if hasattr(HRSLandingPage.HEADERS, 'Cookie'):
            delattr(HRSLandingPage.HEADERS, 'Cookie')

        url_string = self._get_host_url_for_url_maker('hotel_data')
        hotels = self._html['hotels'][3:]
        hotel_urls = []
        hotel_id_lst = []
        for each in hotels:
            hotel_id = each[0]
            hotel_urls.append(url_string.format(HRSLandingPage.HOST,
                            self.jsessionid, self.client_id, self.cid, self._get_currency,
                            hotel_id))
            hotel_id_lst.append(hotel_id)
        else:
            self.hotels_id_dict = dict(enumerate(hotel_id_lst))
           
        return hotel_urls

    @property
    def _get_hotel_count(self):
        return self._html['hotels'][0]

    @property
    def _get_currency(self):
        if self.city == "Sharm el Sheikh -Dahab":
            return "USD"
        return "EUR"

    @property
    def _lat_long_links(self):
        """
        return lat and long links from latLongXpath
        :return: [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]
        """
        if len(self.CONFIG_FILE.latLongXpath) == 0:
            raise exceptions.LatLongNotFountError
        return [self._clean_host_url + lt for lt in self._html.xpath(self.CONFIG_FILE.latLongXpath)]

    def _get_host_url_for_url_maker(self, *args):
        """
        :params: args the page for which the request is made
                form_page, hotel_list, hotel_data
        :return: url as string for the page requested
        """
        url_list = [
                    lambda: '{0}searchWeb1000.do?clientId={1}&cid={2}'.format(HRSLandingPage.HOST,
                                self.client_id, self.cid) if args[0] == 'form_page' else None,
                    lambda: '{0}hotelListJson.do?clientId={1}&cid={2}&activity=getHotelListJson&il97gsip'.format(HRSLandingPage.HOST,
                                self.client_id, self.cid) if args[0] == 'hotel_list' else None,
                    lambda: '{0}showDetailsOfHotel.do;jsessionid={1}?clientId={2}-&cid={3}&bookingFrom=list&currency={4}&hotelnumber={5}&activity=showListHotel&method=showHotel&waitingReloadCounter=0' if args[0] == 'hotel_data' else None,
                    # lambda: '{0}showDetailsOfHotel.do;jsessionid={1}?clientId={2}-&cid={3}&bookingFrom=list&currency={4}&hotelnumber={5}&activity=showListHotel&method=showHotel' if args[0] == 'hotel_data' else None,
                ]
        crawl_url = None

        for each in url_list:
            if each() is not None:
                crawl_url = each()
                break
        else:
            crawl_url = HRSLandingPage.HOST

        return crawl_url

    def _get_post_params(self):
        """
        returns a dictionary of post parameters for hotel requests
        :return: dict of key value to be sent in post body
        """
        inSplit = self.check_in.strftime("%m/%d/%y").split('/')
        inMonth, inDay, inYear = inSplit[0], inSplit[1], inSplit[2]
        outSplit = self.check_out.strftime("%m/%d/%y").split('/')
        outMonth, outDay, outYear = outSplit[0], outSplit[1], outSplit[2]
        url_dict = {
            "clientId": self.client_id,
            "cid": self.cid,
            "activity": "initSearch",
            "hotelThemesType=": "",
            "searchSource": "1",
            "stopWatchTime": "",
            "location": self.city.upper(),
            "stayPeriod.start.date": "{0}%2F{1}%2F{2}".format(inMonth, inDay, inYear),
            "stayPeriod.end.date": "{0}%2F{1}%2F{2}".format(outMonth, outDay, outYear),
            "roomSelector": "0",
            "singleRooms": "",
            "doubleRooms": "1",
            "adults": "2",
            "children": "0",
            "childAccomodations%5B0%5D.age": "-1",
            "childAccomodations%5B0%5D.accomodation": "1",
            "childAccomodations%5B1%5D.age": "-1",
            "childAccomodations%5B1%5D.accomodation": "1",
            "childAccomodations%5B2%5D.age": "-1",
            "childAccomodations%5B2%5D.accomodation": "1",
            "childAccomodations%5B3%5D.age": "-1",
            "childAccomodations%5B3%5D.accomodation": "1",
            "childAccomodations%5B4%5D.age": "-1",
            "childAccomodations%5B4%5D.accomodation": "1",
            "childAccomodations%5B5%5D.age": "-1",
            "childAccomodations%5B5%5D.accomodation": "1",
            "minRating": "0",
            "perimeter": "-1",
            "hotelname": "",
            "submitBasicSearch": "Search+for+hotel",
            "travelPurpose": "",
            "topDestinationsSearch": "0",
            "topDestinationsSearchSelection": "0",
            "suggestedID": city_mapper[self.city]["DestID"],
        }

        return url_dict

    @property
    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        return HRSLandingPage.HEADERS

    def _set_headers(self, res_obj):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        self.HEADERS = res_obj.headers

    def _set_cookie(self, resp_object):
        """
        :param cookie_object: either response or driver object to get cookie and set in self.cookie
        :return:
        """
        if resp_object is not None:
            HRSLandingPage.HEADERS['Cookie'] = resp_object.headers['Set-Cookie']
        else:
            pass

    def _set_hotel_web_id(self, hotel_id):
        """
        set hotel web id
        :param: hotel url
        :return: None
        """
        self.hotel_web_id = hotel_id

    def _get_hotel_list(self):
        url = self._get_host_url_for_url_maker('hotel_list')
        return super()._get_hotel_list(url)

    def _get_post_data(self):
        """
        return post params as a url string
        :return: post body as string
        """
        post_body = self._get_post_params()
        post_body = ''.join([ '&{0}={1}'.format(i, j) for i, j in post_body.items() ])
        return post_body

    def _process_form_data(self):
        """
        method to process form data for travellers details
        :return: None
        """
        url = self._get_host_url_for_url_maker('form_page')
        body = self._get_post_data()
        res_html, res_obj, driver_obj = self.post_request(url, body=body, 
                                                    body_type='url_string', headers=self._get_headers, proxy=self.proxy)
        return None

    def _process_homepage(self):
        """
        method to process homepage, get cookies and make post
        form data call
        :return: None
        """
        res_html, res_obj, driver_obj = self.get_request(HRSLandingPage.HOST, self._get_headers, proxy=self.proxy)
        self._set_cookie(res_obj)
        cid_idx = res_html.find('&cid')
        cookie = res_obj.headers['Set-Cookie']
        self.cid = res_html[res_html.find('&cid'):res_html.find('&',cid_idx+1)].split('=')[1]
        client_idx = res_html.find('&clientId')
        self.client_id = res_html[res_html.find('&clientId'):res_html.find('-', client_idx)].split('=')[1]

        self.jsessionid = cookie[cookie.find('jsession')+11:cookie.find(';',cookie.find('jsession'))]
        self._process_form_data()

        return None

    def _set_html(self):
        """
        method to process home page and get the hotel list
        for the specific city
        :return: None
        """
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        self._html = json.loads(self._get_hotel_list())


def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    print("consumer_data")
    print(consumer_data)
    start_time = time.time()
    crawled_data = HRSLandingPage(consumer_data).crawl_hotels(redelivered)
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
