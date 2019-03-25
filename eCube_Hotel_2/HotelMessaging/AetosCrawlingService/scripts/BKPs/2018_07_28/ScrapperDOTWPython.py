import json

from lxml import etree, html
from copy import deepcopy
from scripts import dotw_config
from scripts.core import exceptions
from scripts.core.logs import CrawlingLogger
from scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler


class DOTWLogger(CrawlingLogger):
    NAME = 'dotw_crawling'


DOTWLogger.set_logger()
CrawlerBase.TRL = DOTWLogger
CrawlerBase.CONFIG_FILE = dotw_config


class DOTWHotel(HotelHandler):

    @property
    def _get_name(self):
        # from pdb import set_trace; set_trace()
        pageHtml = html.fromstring(self._html['html_element'])
        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()

    @property
    def _get_cache_page(self):
        return self._html['html_element']

    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        hotel_elem = etree.tostring(self._landing_page.hotel_elem).decode('utf-8')
        return {'hotelHTML': self._html, 'hotel_elem': hotel_elem}

    @property
    def _get_room_types(self):
        """
        :return: { 'roomtypehtml': 'page_source_of_roomtype',
                   'pricehtml': 'page_source_of_price_for_roomtype',
                   'boardTypeHTML': 'page_soource_of_promotion_for_boardtype',
                }
        """
        pageHtml = self._landing_page.hotel_elem
        # st()
        room_dict = {
            'roomTypeHTML': etree.tostring(pageHtml.getchildren()[2]).decode('utf-8'),
            'priceHTML': etree.tostring(pageHtml.getchildren()[2]).decode('utf-8'),
            'boardTypeHTML': etree.tostring(pageHtml.getchildren()[2]).decode('utf-8'),
        }

        return room_dict

    @property
    def _get_city_zone(self):
        return self._landing_page.city_zone

    @classmethod
    def complete_hotel_url(cls, hotel_url, domain):
        """
        :param: hotel_url as string
        :return: complete hotel url if partial
        """
        if not hotel_url.startswith(domain):
            hotel_url = '{0}{1}'.format(domain, hotel_url)
        return hotel_url


class DOTWLoginPage(object):
    LOGIN_PAGE = None  # object of LangingPage class

    @classmethod
    def _get_token(cls, html_page):
        """
        get token from login page
        :return: token
        """
        strt_token_idx = html_page.find('_token')
        end_token_idx = html_page.find('>', strt_token_idx + 1)
        out_str = html_page[strt_token_idx: end_token_idx]
        out_str = out_str[out_str.find('value'):]
        token = out_str.split('=')[1].strip('"')

        return token

    @classmethod
    def _get_login_page(cls):
        """
        get login page cookie and token
        :return: None
        """
        url = CrawlerBase.CONFIG_FILE.login_page_url
        headers = CrawlerBase.CONFIG_FILE.login_page_header

        res_html, res_obj, _ = cls.LOGIN_PAGE.get_request(url, headers=headers,
                                                          proxy=cls.LOGIN_PAGE.proxy)

        cls.LOGIN_PAGE.cookies_map['login_page_cookie'] = res_obj.headers['Set-Cookie']
        cls.LOGIN_PAGE._login_token = cls._get_token(res_html)

    @classmethod
    def process_login(cls):
        """
        login to dotw page
        :return: res_html, res_obj
        """
        url = CrawlerBase.CONFIG_FILE.user_login_url
        headers = CrawlerBase.CONFIG_FILE.user_login_header
        headers['Cookie'] = cls.LOGIN_PAGE.cookies_map['login_page_cookie']

        user_id = CrawlerBase.CONFIG_FILE.user_id
        password = CrawlerBase.CONFIG_FILE.password
        company_code = CrawlerBase.CONFIG_FILE.company_code

        post_str = "_token={0}&UserId=&UserId={1}&Password={2}&CompanyCode={3}".format(cls.LOGIN_PAGE._login_token,
                                                                                       user_id, password, company_code)

        # url, headers, proxy, body, body_type='url_string'
        return cls.LOGIN_PAGE.post_request(url, headers=headers,
                                           proxy=cls.LOGIN_PAGE.proxy, body=post_str,
                                           body_type='url_string')

    @classmethod
    def _process(cls):
        """
        process login page and get logged in successfully
        """
        cls._get_login_page()
        res_html, res_obj, _ = cls.process_login()
        cls.LOGIN_PAGE.cookies_map['user_login_cookie'] = res_obj.headers['Set-Cookie']
        res_elem = html.fromstring(res_html)
        cls.LOGIN_PAGE._country_list = json.loads(res_elem.xpath('//input[@id="countryList"]/@value')[0])


class DOTWHomePage(object):
    HOME_PAGE = None  # object of DOTWLandingPage

    @classmethod
    def _get_post_params(cls, query_name, *args, **kwargs):
        """
        :return: dict of key value to be sent in post body
        """
        post_data_dict = {}

        return post_data_dict

    @classmethod
    def _get_host_url_for(cls, *args):
        """
        :params: args the page for which the request is made
                city_code
        :return: url as string for the page requested
        """
        url = [
            lambda: "{0}/_ci_ajax/en/ajaxproxy?c=City&m=getTypeaheadDestination&s=true&limit=10&showMoreButton=true&query={1}&productId=1" if
            args[0] == 'city_code' else None]

        for each in url:
            if each is not None:
                return each()

        print('empty URL')
        return cls.HOME_PAGE.HOST

    @classmethod
    def get_city_code(cls):
        url = cls._get_host_url_for('city_code').format(cls.HOME_PAGE.HOST,
                                                        cls.HOME_PAGE.city)
        headers = CrawlerBase.CONFIG_FILE.city_code_header
        headers['Cookie'] = cls.HOME_PAGE.cookies_map['user_login_cookie']

        return cls.HOME_PAGE.get_request(url, headers=headers, proxy=cls.HOME_PAGE.proxy)

    @classmethod
    def _process(cls):
        # login_page processing
        res_html, res_obj, _ = cls.get_city_code()
        return res_html, res_obj


class DOTWLandingPage(HotelLandingPageHandler):
    HOST = CrawlerBase.CONFIG_FILE.HOST

    HOTEL_HANDLER_CLASS = DOTWHotel

    def __init__(self, request_data):
        self.cookies_map = dict()
        self._country_list = list()
        self._login_token = None
        self.city_code = None
        self.country_code = None
        self.residence_id = None
        self.landing_pages = None
        self.city_zone = None
        super().__init__(request_data)

    @property
    def _hotels(self):
        """
        return hotel elements from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        hotels = list()
        # if self.city == 'Kuala Lumpur' or self.city == 'Istanbul':
        if self.city == 'KUALA LUMPUR' or self.city == 'ISTANBUL':
            for each in self.landing_pages['hotels']:

                first_page = each['page1']
                second_page = each['page2']
                if second_page:
                    pageHtml = html.fromstring(first_page)
                    atom = [(i, each['city_code'], each['city'])
                            for i in pageHtml.xpath(self.CONFIG_FILE.hotelLinksXpath)]
                    hotels.extend(atom)

                    pageHtml = html.fromstring(second_page)
                    atom = [(i, each['city_code'], each['city'])
                            for i in pageHtml.xpath(self.CONFIG_FILE.hotelLinksXpath)]
                    hotels.extend(atom)
        else:
            for each in self.landing_pages['hotels']:
                for page in each.values:
                    pageHtml = html.fromstring(page)
                    hotels.extend(pageHtml.xpath(self.CONFIG_FILE.hotelLinksXpath))

        self.hotel_counts = len(hotels)
        return hotels

    @property
    def _get_currency(self):
        return "AED"

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
                city_code, sid_query, hotel_list
        :return: url as string for the page requested
        """
        url_list = []

        for each in url_list:
            if each() is not None:
                return each()

        return DOTWLandingPage.HOST

    @property
    def _get_headers(self, ):
        """
        headers for making requests
        :return: var_headers
        """
        var_headers = dict()

        var_headers["Accept"] = "text/html, */*; q=0.01"
        var_headers["Accept-Language"] = "en-US"
        var_headers["Host"] = "us.dotwconnect.com"
        var_headers["Proxy-Connection"] = "Keep-Alive"
        var_headers["User-Agent"] = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"
        var_headers["X-Requested-With"] = "XMLHttpRequest"

        if 'user_login_cookie' in self.cookies_map:
            var_headers["Cookie"] = self.cookies_map['user_login_cookie']
            if 'Cookie' not in self.headers.keys():
                self.headers.update({'Cookie': self.cookies_map['user_login_cookie']})
        return var_headers

    def _set_hotel_web_id(self, hotel_id):
        """
        set hotel web id
        :param: hotel_id
        :return: None
        """
        self.hotel_web_id = hotel_id

    def _set_city_zone(self, city_zone):
        self.city_zone = city_zone.upper()

    def _set_hotel_element(self, hotel_elem):
        self.hotel_elem = deepcopy(hotel_elem)

    def hotel_list_params(self, city_code, city, hotel_listing=False):
        strpos = self.pos.replace(' ', '+')
        adults = CrawlerBase.CONFIG_FILE.travellers_data_dict[int(self.adults)]['adults']
        children = CrawlerBase.CONFIG_FILE.travellers_data_dict[int(self.adults)]['children']
        childage1 = CrawlerBase.CONFIG_FILE.travellers_data_dict[int(self.adults)]['childage1']
        childage2 = CrawlerBase.CONFIG_FILE.travellers_data_dict[int(self.adults)]['childage2']

        hotel_url_params = dict()

        if hotel_listing is not True:
            hotel_url_params["destination"] = city.replace(' ', '+').upper()
        else:
            hotel_url_params["_token"] = self._login_token
        hotel_url_params["PSearchId"] = str(city_code)
        hotel_url_params["PSearchType"] = 'city'
        hotel_url_params["PLocationType"] = ''
        hotel_url_params["destinationCountry"] = str(self.country_code)

        hotel_url_params["DateFrom"] = '{0}%2F{1}%2F{2}'.format(self.check_in.day, self.check_in.month,
                                                                 self.check_in.year)

        hotel_url_params["dateFrom"] = '{0}-{1}-{2}'.format(self.check_in.year, self.check_in.month, self.check_in.day)

        hotel_url_params["DateTo"] = '{0}%2F{1}%2F{2}'.format(self.check_out.day, self.check_out.month,
                                                               self.check_out.year)

        hotel_url_params["dateTo"] = '{0}-{1}-{2}'.format(self.check_out.year, self.check_out.month,
                                                           self.check_out.day)

        hotel_url_params["roomsNo"] = "1"
        hotel_url_params["markerRange"] = "5"
        hotel_url_params["propertyType"] = ""
        hotel_url_params["starRating"] = ""
        hotel_url_params["availability"] = "-1"
        hotel_url_params["address"] = ""
        hotel_url_params["radius"] = "3"
        hotel_url_params["latitude"] = ""
        hotel_url_params["longitude"] = ""
        hotel_url_params["orderRates"] = "0"
        hotel_url_params["residency%5B1%5D"] = "{0}".format(self.residence_id)
        hotel_url_params["textResidency%5B1%5D"] = "{0}".format(strpos)
        hotel_url_params["nationality%5B1%5D"] = "{0}".format(self.residence_id)
        hotel_url_params["textNationality%5B1%5D"] = "{0}".format(strpos)
        hotel_url_params["adultsCount%5B1%5D"] = "{0}".format(adults)
        hotel_url_params["childrenCount%5B1%5D"] = "{0}".format(children)
        hotel_url_params["childrenAges%5B1%5D%5B0%5D"] = "{0}".format(childage1)
        hotel_url_params["childrenAges%5B1%5D%5B1%5D"] = "{0}".format(childage2)
        hotel_url_params["childrenAges%5B1%5D%5B2%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B3%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B4%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B5%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B6%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B7%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B8%5D"] = "3"
        hotel_url_params["childrenAges%5B1%5D%5B9%5D"] = "3"
        hotel_url_params["doSearch"] = "1"

        return hotel_url_params

    def _get_hotels(self, url, headers):
        """
        get the hotel lists page
        :param: url for hotel list
        :param: headers for hotel list request
        :return: html hotel list page dict
        """
        # res_html, res_obj, _ = self.get_request(url, headers=headers, proxy=self.proxy)
        res_html, res_obj, _ = self.get_headerless_request(url, proxy=self.proxy)
        list_elem = html.fromstring(res_html)
        transaction_id = list_elem.xpath('//input[@id="currentTransactionID"]/@value')
        if not len(transaction_id):
            raise self.EXCEPTIONS['SCRIPT_PNF']
        transaction_id = transaction_id[0]
        next_page_url = CrawlerBase.CONFIG_FILE.next_hotel_list_page_url.format(transaction_id)
        res_html2, res_obj2, _ = self.get_request(next_page_url, headers=headers, proxy=self.proxy)

        return {"page1": res_html, "page2": res_html2}

    def _get_hotel_list(self):
        if self.city == 'Kuala Lumpur' or self.city == 'Istanbul':
            hotel_list = []
            city_name = self.city.replace(' ', '_')
            city_zones = getattr(CrawlerBase.CONFIG_FILE, city_name)

            for city_code, city in city_zones.items():
                url = 'https://us.dotwconnect.com/interface/en/accommodation/search?{0}'.format(''.join(
                    # ['{0}={1}'.format(i, j) for i, j in self.hotel_list_params(city_code, city).items()]
                    ['&%s=%s' % (i, p) for i, p in self.hotel_list_params(city_code, city).items()]
                ))
                listing_page = self._get_hotels(url, self._get_headers)
                listing_page.update({'city_code': city_code})
                listing_page.update({'city': city})
                hotel_list.append(listing_page)
            return hotel_list
        else:
            url = '{0}{1}'.format(DOTWLandingPage.HOST, ''.join(
                # ['{0}={1}'.format(i, j) for i, j in self.hotel_list_params(self.city_code, self.city).items()]
                ['&%s=%s' % (i, p) for i, p in self.hotel_list_params(self.city_code, self.city).items()]
            ))
            return list(self._get_hotels(url, self._get_headers))

    def _process_homepage(self):
        """
        method to process homepage, get cookies and make post
        form data call
        :return: None
        """
        DOTWLoginPage.LOGIN_PAGE = self
        DOTWLoginPage._process()
        for each in self._country_list:
            if each['text'] == self.pos:
                self.residence_id = each['val']
                break

        DOTWHomePage.HOME_PAGE = self
        res_html, res_obj = DOTWHomePage._process()
        res_dict = json.loads(res_html)
        self.city_code = res_dict[0]['id']
        self.country_code = res_dict[0]['countryId']

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        if self.landing_pages is None:
            self.landing_pages = dict()
        self.landing_pages['hotels'] = self._get_hotel_list()

    def _save_hotel(self, index, hotel_url):
        latitude_url = None
        self.TRL.debug_log('Making Hotel for URL: %s' % hotel_url[0], self.request_id, self.sub_request_id,
                           self.request_run_id)

        if self.city == 'Kuala Lumpur' or self.city == 'Istanbul':
            elem = hotel_url[0]
            attribs = hotel_url[0].attrib

            self._set_hotel_web_id(attribs['data-hotelid'])
            self._set_city_zone(hotel_url[2])
            self._set_hotel_element(elem)

            crawl_url = CrawlerBase.CONFIG_FILE.hotel_data_url.format(attribs['data-hotelid'])
            city_code, city = hotel_url[1:]
            crawl_url = '{0}{1}'.format(crawl_url, ''.join(
                # ['{0}={1}'.format(i, j) for i, j in self.hotel_list_params(city_code, city, True).items()]
                ['&%s=%s' % (i, p) for i, p in self.hotel_list_params(city_code, city).items()]
            ))
        else:
            attribs = hotel_url.attrib
            self._set_hotel_web_id(attribs['data-hotelid'])
            self._set_city_zone(self.city)
            self._set_hotel_element(hotel_url)
            crawl_url = '{0}{1}'.format(hotel_url, ''.join(
                # ['{0}={1}'.format(i, j) for i, j in self.hotel_list_params(self.city_code, self.city).items()]
                ['&%s=%s' % (i, p) for i, p in self.hotel_list_params(self.city_code, self.city).items()]
            ))

        # from pdb import set_trace; set_trace()
        hotel = self.HOTEL_HANDLER_CLASS.get_hotel(crawl_url, latitude_url, self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        hotel_data = hotel.save_html(index)
        return hotel_data


def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    # consumer_data['RequestInputs']['city'] = 'Istanbul'
    crawled_data = DOTWLandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    print('\ncrawling hotels')
    print(type(crawled_data))
    # file_distincter = time.time()
    # with open('do/tw_crawled_data_%s.json' % file_distincter, 'w+') as file_obj:
    #     print("file_distincter")
    #     print(file_distincter)
    #     file_obj.write(json.dumps(crawled_data))
    return crawled_data
