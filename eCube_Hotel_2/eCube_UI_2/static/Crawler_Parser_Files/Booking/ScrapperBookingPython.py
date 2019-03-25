import datetime
import copy
import json
import requests
import pandas as pd
import time
from lxml import etree, html
from copy import deepcopy
from Crawling.scripts.Hotelbeds_Availability import ScrapperConfigBookingPython
from Crawling.scripts.core import exceptions
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler
import re
from codecs import escape_decode
from urllib.request import unquote

class BookingAvailabilityLogger(CrawlingLogger):
    NAME = 'booking_availability_crawling'

BookingAvailabilityLogger.set_logger()
CrawlerBase.TRL = BookingAvailabilityLogger
CrawlerBase.CONFIG_FILE = ScrapperConfigBookingPython

class BookingHotel(HotelHandler):


    @classmethod
    def get_hotel(cls, hotel_url, landing_page):

        html_elem = {'html_element': hotel_url}
        return cls(landing_page, html_elem)

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        pageHtml = html.fromstring(self._html['html_element'])
        return str(pageHtml.xpath(self.CONFIG_FILE.hotelNameXpath)[0]).strip()

    @property
    def _get_cache_page(self):
        return self._html

    @property
    def _get_html(self):

        return {'landingPage': list(map(lambda x: str(html.tostring(x)), self._landing_page._html))}

    def save_html(self,pagedata,index):
        hotel_data = dict()
        meta_data = dict()

        # Properties from Parent
        hotel_data['index'] = index
        hotel_data['hotel_count'] = self.hotel_count
        hotel_data['city'] = self.city
        hotel_data['country'] = self.country
        hotel_data['city_zone'] = BookingLandingPage.get_zones(self,self.city)
        hotel_data['checkIn'] = str(self.check_in)
        hotel_data['checkOut'] = str(self.check_out)
        # Crawler Output
        hotel_data['htmls'] = pagedata
        hotel_data['hotelName'] = self._get_name
        try:
            hotel_data['hotelName'] = self._get_name
        except Exception as e:
            raise self.EXCEPTIONS['HOTEL_NOT_FOUND'](str(e))
        hotel_data['roomTypes'] = ""
        hotel_data['cachePageHTML'] = pagedata #self._get_cache_page
        hotel_data['hotel_id'] = ""
        # Meta Data
        meta_data['requestId'] = self._landing_page.request_id   #self._landing_page.request_id
        meta_data['cachePageToken'] = self._get_cache_filename
        meta_data['subRequestId'] =   self._landing_page .sub_request_id
        meta_data['requestRunId'] =   self._landing_page .request_run_id
        meta_data['startDT'] = str(self.start_time)
        meta_data['endDT'] = str(datetime.datetime.now())
        hotel_data['meta'] = meta_data

        self.TRL.debug_log(
            'Saving Hotel:%s' % self._get_name, self._landing_page.request_id, self._landing_page.sub_request_id,
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers)
        hotel_data['meta']['cachePageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cache_page)
        hotel_data['meta']['cachePageURL'] = HotelHandler.SERVICE_CALLS['save_cache_page'](self._get_cache_filename,pagedata)
        response = copy.deepcopy(self._landing_page.request_data)

        response['hotel'] = hotel_data
        # return HotelHandler.SERVICE_CALLS['save_html'](hotel_data)
        return self.SERVICE_CALLS['save_html'](response)

    @classmethod
    def _get_latitude(cls, latitude_url, proxy, headers, cookie):
        return {'html_element': None}

class BookingLandingPage(HotelLandingPageHandler):
    HOST = 'https://www.booking.com'
    HOTEL_HANDLER_CLASS = BookingHotel
    HOTEL_LIST_DRIVER = True
    csrftoken = ""
    aid = ""
    label = ""
    sid = ""
    channel_id = ""
    # starcount_resplist=[]
    PROXY_LESS_HIT = False
    currency=''
    def get_zones(self, city):
        mapped_cities=[]
        dllurl= "https://ecube-hotel.eclerx.com/schedule/api/v1/GetMasterMappings?city="+str(self.city)+"&country="+(self.country)+"&supplier=Booking"

        resp_text,resp_obj,_=self.__class__.get_headerless_request(dllurl,self.proxy,timeout=30)
        if resp_obj.status_code==200:
            try:
                mulzone=re.findall(self.CONFIG_FILE.multizonecountpath,resp_text)[0]
                multizone = int(float(mulzone))
                zoneid1=re.findall(self.CONFIG_FILE.zoneidpath,resp_text)[0]
                zonename1= re.findall(self.CONFIG_FILE.zonenamepath,resp_text)[0]
                zonetype1=re.findall(self.CONFIG_FILE.zonetypepath,resp_text)[0]

            except Exception as e:
                    raise self.EXCEPTIONS['Multi zone not found'](str(e))
        zone1= zoneid1.split('|')
        znm = zonename1.split('|')
        ztyp= zonetype1.split('|')


        mapped_city={
                'city' :re.findall('<Destination>([\w\S].*?)<',resp_text)[0],
                 'zoneName':znm,'zoneCode':zone1,'zoneType' : ztyp
            }

        return mapped_city['city'], mapped_city['zoneName'], mapped_city['zoneCode'], mapped_city['zoneType']

    @classmethod
    def get_formatted_date(cls, datetime_obj):
        # print("datetime_obj====", datetime_obj)
        year = str(datetime_obj.year)
        month = datetime_obj.month
        month = "0" + str(month) if month < 10 else str(month)
        day = datetime_obj.day
        day = "0" + str(day) if day < 10 else str(day)
        date_str = year + "-" + month + "-" + day
        return date_str

    @property
    def _get_url_params(self):
        """
        :return: dict of key value to be added in URL
        """
        payload_list = []
        city, zones, zoneCodes, zoneTypes = self.get_zones(self.city)
        for zone in zones:
            print(zone)
            zoneType = zoneTypes[zones.index(zone)]
            zoneCode = zoneCodes[zones.index(zone)]

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
                'Connection': 'keep-alive',
                'Host': 'www.booking.com',
                'User-Agent': self.user_agent.strip()}

            homePageText, res_obj, driver_obj = self.get_request('https://www.booking.com', headers, self.proxy,
                                                                 driver=self.HOTEL_LIST_DRIVER)

            cookieDict = res_obj.cookies.get_dict()
            cookie = 'bkng=' + cookieDict['bkng']

            if res_obj.status_code == 200:
                csrf = re.findall("b_csrf_token:([\w\W].*?),", homePageText)
                b_aid = re.findall("b_aid:([\w\W].*?),", homePageText)
                b_label = re.findall("b_label:([\w\W].*?),", homePageText)
                b_sid = re.findall("b_label:([\w\W].*?),", homePageText)
                b_channelid = re.findall("b_partner_channel_id\W*([\w].*?),", homePageText)

                if len(csrf) > 0:
                    BookingLandingPage.csrftoken = csrf[0].strip().replace('\\', '').replace("'", "")
                    BookingLandingPage.aid = b_aid[0].strip().replace('\\', '').replace("'", "")
                    BookingLandingPage.label = b_label[0].strip().replace('\\', '').replace("'", "")
                    BookingLandingPage.sid = b_sid[0].strip().replace('\\', '').replace("'", "")
                    BookingLandingPage.channel_id = b_channelid[0].strip().replace('\\', '').replace("'", "")

            inDate= self.check_in
            outDate=self.check_out
            yy1, mm1, dd1 =  inDate.year, inDate.month, inDate.day
            yy2, mm2, dd2 = outDate.year, outDate.month, outDate.day
            # '''datecalc'''
            self.cookie = cookie
            self.headers=headers
            strAdultInput = "&group_adults=2&group_children=0"
            payload = {'label': BookingLandingPage.label, 'sid': BookingLandingPage.sid, 'sb': '1',
                       'src': 'searchresults', 'src_elem': 'sb',
                       'error_url': 'https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Flabel%3D' + BookingLandingPage.label + '%3Bsid%3D' + BookingLandingPage.sid + '%3Btmpl%3Dsearchresults%3Bac_position%3D0%3Bac_suggestion_theme_list_length%3D0%3Bcheckin_month%3D' + str(
                           mm1) + '%3Bcheckin_monthday%3D' + str(dd1) + '%3Bcheckin_year%3D' + str(
                           yy1) + '%3Bcheckout_month%3D' + str(mm2) + '%3Bcheckout_monthday%3D' + str(
                           dd2) + '%3Bcheckout_year%3D' + str(
                           yy2) + '%3Bclass_interval%3D1%3Bdtdisc%3D0%3Bgroup_adults%3D' + str(
                           self.adults) + '%3Bgroup_children%3D' + str(
                           self.children) + '%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Boffset%3D0%3Bpostcard%3D0%3Brows%3D15%3Bsb_price_type%3Dtotal%3Bsearch_pageview_id%3Db62834672bd50568%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc_elem%3Dsb%3Bss_all%3D0%3Bss_raw%3D' + self.city + '%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3D' + self.city + '%26%3B',
                       'ss': zone, 'checkin_monthday': str(dd1), 'checkin_month': str(mm1), 'checkin_year': str(yy1),
                       'checkout_monthday': str(dd2), 'checkout_month': str(mm2), 'checkout_year': str(yy2),
                       'group_adults': str(self.adults),
                       'group_children': str(self.children), 'no_rooms': '1', 'from_sf': '1', 'ss_raw': self.city,
                       'ac_position': '0', 'ac_langcode': 'en', 'ac_click_type': 'b', 'dest_id': str(zoneCode),
                       'dest_type': zoneType, 'place_id_lat': '37.110174', 'place_id_lon': '-8.272562',
                       'search_selected': 'true',
                       'search_pageview_id': '990f49a162fa02e7', 'ac_suggestion_list_length': '5',
                       'ac_suggestion_theme_list_length': '0'
                       }

            payload_list.append(payload)
        return payload_list

    @property
    def _get_cache_filename(self):
        now_time = str(time.time()).replace('.', '')
        sub_req = self.sub_request_id
        return 'tk_%s_sr_%s' % (now_time, sub_req)

    def set_checkIn(self, inDate):
        try:
            inDay, inMonth, inYear = inDate.split('/')
        except:
            pass
        try:
            inDay, inMonth, inYear = inDate.split('-')
        except:
            pass
        try:
            inDay, inMonth, inYear = inDate.split(':')
        except:
            pass
        try:
            inDay, inMonth, inYear = inDate.split('.')
        except:
            pass
        return inYear, inMonth, inDay

    def set_checkOut(self, outDate):
        try:
            outDay, outMonth, outYear = outDate.split('/')
        except:
            pass
        try:
            outDay, outMonth, outYear = outDate.split('-')
        except:
            pass
        try:
            outDay, outMonth, outYear = outDate.split(':')
        except:
            pass
        try:
            outDay, outMonth, outYear = outDate.split('.')
        except:
            pass
        return outYear, outMonth, outDay

    def _url_maker(self):
        self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id,
                           self.request_run_id)
        params = self._get_url_params
        url_list = []
        for param in params:
            self.TRL.debug_log('Params:%s' % param, self.request_id, self.sub_request_id, self.request_run_id)
            url_list.append("".join([self._clean_host_url + '/searchresults.en-gb.html?'] + ['&%s=%s' % (i, p) for i, p in param.items()]))
        return url_list

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)

        html_list = self._get_hotel_list
        # sample = list(map(html.fromstring, html_list))
        # self._html = sample
        # return sample
        return html_list

    @property
    def _get_hotel_list(self, url=None):
        # allresponse=""
        # starhreflist =[]
        # starcountlist=[]

        self.headers=self._get_headers()
        resp_list=[]
        if not url:
            link = self._url_maker()
        elif isinstance(url, str):
            link = url
        elif callable(url):
            link = url(self)
        else:
            self.TRL.error_log('Invalid URL to get Hotel List', self.request_id, self.sub_request_id, self.request_run_id)
            raise self.EXCEPTIONS['INVALID_URL']
        try:
            self.proxy.check_proxy(link[0], headers= self.headers)
        except (
            ProxyHandler.EXCEPTIONS['SERVER_DOWN_ERROR'],
            ProxyHandler.EXCEPTIONS['SERVER_ERROR'],
            ProxyHandler.EXCEPTIONS['PNF_ERROR'],
            ProxyHandler.EXCEPTIONS['PROXY_AUTH_ERROR'],
            ProxyHandler.EXCEPTIONS['REQUEST_ERROR']
        ) as e:
            self.TRL.error_log(
                'No Working Proxy Found:%s' % str(e), self.request_id, self.sub_request_id, self.request_run_id,
                headers=self.headers)
            raise ProxyHandler.EXCEPTIONS['NOT_WORKING']

        for kk in link:

            starhreflist=[]
            allresponse=[]
            starcountlist=[]
            kk = str(kk).replace(" ","%20")
            resp, resp_obj, _ = self.get_request(kk, self.headers, self.proxy, driver=self.HOTEL_LIST_DRIVER)
            self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
            request_type = RequestHandler._get_request_type()
            if request_type['driver']:
                self._set_cookie(_)
            else:
               self.cookie= resp_obj.cookies
            self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
            if resp_obj.status_code==200:
                responsedata1 = str(resp_obj.text.encode('UTF-8')).replace('\\n', ' ')
                ##fetch star count urls
                tree = html.fromstring(responsedata1)
                result=tree.xpath(self.CONFIG_FILE.starpath)
                curr = tree.xpath(self.CONFIG_FILE.currpath)
                lat=re.findall(self.CONFIG_FILE.latpath,str(responsedata1))
                long=re.findall(self.CONFIG_FILE.longpath,str(responsedata1))
                if len(lat) > 0:
                    self.latitude = lat[0]
                if len(long) > 0:
                    self.longitude = long[0]
                if len(curr) > 0:
                    self.currency = curr[0]
                if not result:
                    pass
                else:
                    subresult = result[0].xpath('./a')
                    if not subresult:
                        pass
                    else:
                        for kk1 in range(0, len(subresult)):
                            temp1 = subresult[kk1].xpath('./@href')
                            starhreflist.append("https://www.booking.com"+temp1[0].strip())
                            temp2 = subresult[kk1].xpath('./@data-count')
                            starcountlist.append(temp2[0].strip())
                    if len(starhreflist)>0 and len(starcountlist)==len(starhreflist):
                        resp_list.extend(self.crawl_starcounturl(starhreflist,starcountlist))
                        # allresponse= self.crawl_starcounturl(starhreflist,starcountlist)
                # resp_list.extend(allresponse)
                # resp_list.append("|Currency ::" +self.currency +"||Latitude :"+str(self.latitude) +"||Longitude :"+ str(self.longitude )+"||")
        return resp_list

    def crawl_starcounturl(self, starhreflist, starcountlist):
        offset = 0
        data1 = starhreflist
        data2 = starcountlist
        pages_captured=[]
        temp=[]

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Host': 'www.booking.com',
            'Accept-Language': 'en-US',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Booking-AID': BookingLandingPage.aid,
            'X-Booking-CSRF': BookingLandingPage.csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'X - Booking - Language - Code': 'en - gb',
            'X-Booking-Session-Id': BookingLandingPage.sid,
            'X-Booking-Label': BookingLandingPage.label
        }
        for j in range(0,len(data1)):

            offset = 0
            if "offset="not in data1[j]:
                data1[j] = data1[j] + "&offset=" + str(offset)
            if self.cookie:
                resp1, resp, _ = self.get_request(data1[j], headers, self.proxy,cookie=self.cookie ,driver=self.HOTEL_LIST_DRIVER)
            else:
                resp1, resp, _ = self.get_request(data1[j], headers, self.proxy,driver=self.HOTEL_LIST_DRIVER)

            # responsedata = str((resp.text).encode('UTF-8')).replace('\\n', ' ')
            responsedata = str((resp.text)).replace('\\n', ' ')
            if resp.status_code == 200:
              ####### Get Lastpage ######
                pagelimit = int(int(data2[j]) / 15) + 1
                for pg in range(0, pagelimit):
                    if pg == 0:
                        offset = 0
                        pages_captured.append(pg)
                        hoteltree = html.fromstring(responsedata)
                        divelement=hoteltree.xpath("//div[@id='hotellist_inner']")
                        try:
                            str_element=str(html.tostring(divelement[0])).split('<div class=" sr_item sr_separator')[0]+'</div>'
                            hoteltree=html.fromstring(str_element)

                        except:
                            pass

                        result=hoteltree.xpath('//div[boolean(@data-hotelid) and not(contains(@class,"soldout_property"))]')
                        temp.extend(result)

                        # for hotelblock in result:
                        #     strblock= html.tostring(hotelblock)
                        #     id= re.findall(self.CONFIG_FILE.hotelid,str(strblock))
                        #
                        #     if len(id)>0:
                        #         if id[0]in temp:
                        #             pass
                        #         else:
                        #             temp.append(id[0])

                    else:
                        offset = offset + 15
                        turl = data1[j].split("&offset=")
                        if len(turl) > 1:
                            data1[j] = turl[0] + "&offset=" + str(offset)
                        else:
                            data1[j] = data1[j] + "&offset=" + str(offset)
                        # print("Req url :::" + str(data1[j]))
                        resp1, resp, _ = self.get_request(data1[j], headers, self.proxy, cookie=self.cookie,driver=self.HOTEL_LIST_DRIVER)
                        responsedata4 = str((resp.text)).replace('\\n', ' ')
                        # responsedata4 = str((resp.text).encode('UTF-8')).replace('\\n', ' ')

                        if resp.status_code == 200:
                            hoteltree = html.fromstring(responsedata4)

                            divelement = hoteltree.xpath("//div[@id='hotellist_inner']")
                            try:
                                str_element = str(html.tostring(divelement[0])).split('<div class=" sr_item sr_separator')[
                                    0] + '</div>'
                                hoteltree = html.fromstring(str_element)

                            except:
                                pass

                            result = hoteltree.xpath('//div[boolean(@data-hotelid) and not(contains(@class,"soldout_property"))]')
                            temp.extend(result)

                            # for hotelblock in result:
                            #     strblock = html.tostring(hotelblock)
                            #     id = re.findall(self.CONFIG_FILE.hotelid, str(strblock))
                            #
                            #     if len(id) > 0:
                            #         if id[0] in temp:
                            #             pass
                            #         else:
                            #             temp.append(id[0])
                            #             BookingLandingPage.starcount_resplist.extend(hotelblock)

                            pages_captured.append(pg)
                        else:
                            pass
        # BookingLandingPage.starcount_resplist.extend(set(temp))
        return temp

    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
                   'Connection': 'keep-alive',
                   'Cookie': self.cookie,
                   'Host': 'www.booking.com',
                   'User-Agent': self.user_agent.strip()}
        return headers

    @property
    def _hotels(self):
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        return self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)

    def _save_hotel(self, index, hotel_html):
        latitude_url = None
        self.TRL.debug_log('Listpage data:%s' % hotel_html, self.request_id, self.sub_request_id, self.request_run_id)
        if self.hotels_id_dict is not None:
            self._set_hotel_web_id(self.hotels_id_dict[index])

        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        hotel = BookingHotel.get_hotel(hotel_html,self)

        return hotel.save_html(hotel_html,index)

    def crawl_hotels(self, redelivered):
        # redelivered = False
        partial_hotels = list()
        if redelivered:
            partial_hotels = self.SERVICE_CALLS['get_partial_hotels'](self.sub_request_id)
            print(len(partial_hotels))

        self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
        try:
            total_listpages = self._set_html()
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ProxyError
        ) as e:
            raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
        # self.TRL.debug_log('Listpages/hotelsFound::%s' % len(self._hotels) , self.request_id, self.sub_request_id, self.request_run_id)
        self.TRL.debug_log('Listpages/hotelsFound::%s' % len(total_listpages), self.request_id, self.sub_request_id,
                           self.request_run_id)
        crawled_hotels = []
        # hotels_count = len(total_listpages)
        self.hotel_count= len(total_listpages)
        # hotel_links = []
        # for list_page_index in range(len(total_listpages)):
        #     hoteltree = html.fromstring(total_listpages[list_page_index])
        #     hotel_links.extend(hoteltree.xpath('//div[@id="hotellist_inner"]/div[boolean(@data-hotelid) and not(contains(@class,"soldout_property"))]'))
        #
        # hotel_links=set(hotel_links)

        if self.PROXY_PAGE_WISE:
            self.proxy.initiate_new_proxy(page_type='Detail')

        for index, hotel_element in enumerate(total_listpages):
            try:
                # self._save_hotel(index, str(html.tostring(hotel_element).decode("UTF-8"))+"<div>|Currency ::" + self.currency +"||Latitude :"+str(self.latitude) +"||Longitude :"+ str(self.longitude )+"||</div>")
                self._save_hotel(index, str(html.tostring(hotel_element)) + "<div>|Currency ::" + self.currency + "||Latitude :" + str(
                    self.latitude) + "||Longitude :" + str(self.longitude) + "||</div>")
                # self._save_hotel(index, hotel_element)
                crawled_hotels.append(index)
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

        return self.request_data

def crawl_hotels(consumer_data, redelivered):
    crawled_data = BookingLandingPage(consumer_data).crawl_hotels(redelivered)
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(crawled_data['RequestInputs']['checkOut'])
    crawled_data['RequestInputs']['adults'] = str(crawled_data['RequestInputs']['adults'])
    print('\ncrawling hotels')
    return crawled_data
    # return BookingLandingPage(consumer_data).crawl_hotels(redelivered)

#
# sample = {
#     "requestId": "12",
#     "subRequestId": "1",
#     "requestRunId": "",
#     "DomainName": "https://www.booking.com",
#     "country":"Qatar", #""Spain"  ,  #"Switzerland",  #"Malaysia", ##
#     "POS" :"United Kingdom",
#     "RequestInputs": {
#         "fromAirport": "PCDGA",
#         "toAirport":"PAR",
#         "city": "Doha", ##""Seville",
#         "children": "",
#         "children_age":"",
#         "adults": 2,
#         "room": 1,
#         "board": "",
#         "checkIn": "2019-02-15" ,#"15-12-2018" ,#"15/12/2018",
#       #  "checkOut": "2018-12-16",
#         "nights": 2,
#         "days": 7,
#         "hotelName": "",
#         "starRating": "",
#         "webSiteHotelId": "",
#         "pos": "Spain",
#         "crawlMode": ""
#     }
# }
#
# #
# hotels = crawl_hotels(sample, False)
# #
# import json
# with open('Booking_avail_sample.json', 'w') as outfile:
#     outfile.write(json.dumps(hotels, indent=4))
#     # json.dump(hotels, outfile,indent=4)
#
# # # # # from AetosParsingService.scripts import Parser_BookingAvailability_Python
# # # # # obj = Parser_BookingAvailability_Python.crawl_hotels(hotels)
# # # # # print("objjj===",obj)
# # # #
# from AetosParsingService.scripts import Parser_BookingAvailability_Python
# file = open('Booking_avail_sample.json', 'r')
# sourceCode = file.read()
# obj= Parser_BookingAvailability_Python.crawl_hotels(sourceCode)
#
# import json
# with open('Booking_avail_sample22.json', 'w') as outfile:
#     outfile.write(json.dumps(obj, indent=4))
#     # json.dump(hotels, outfile,indent=4)
#
# # print("objjj===",obj)
