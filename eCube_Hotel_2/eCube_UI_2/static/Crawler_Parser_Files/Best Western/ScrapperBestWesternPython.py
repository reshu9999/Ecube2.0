# from geopy.geocoders import Nominatim
import datetime
import copy
import requests
import json
import time
import pandas as pd
import random
from lxml import etree, html
from _datetime import timedelta
from Crawling.scripts.Hotelbeds import ScrapperConfigBestWesternPython
import re
from Crawling.scripts.core.logs import CrawlingLogger
from Crawling.scripts.core.base import CrawlerBase, HotelLandingPageHandler, HotelHandler, RequestHandler, ProxyHandler
class BW_Logger(CrawlingLogger):
    NAME = 'BW_crawling'

BW_Logger.set_logger()
CrawlerBase.TRL = BW_Logger
CrawlerBase.CONFIG_FILE = ScrapperConfigBestWesternPython

class BW_ProxyHandler(ProxyHandler):
    pass

class BW_Hotel(HotelHandler):
    hotelname=""
    @property
    def _get_cache_page(self):
        return json.dumps(self._html['room_html']) #returning hotel page response json

    @classmethod
    def get_hotel(self, hotel_url, latitude_url, landing_page):
        fulllist=[]
        roomlinks=[]
        detail=""
        BW_LandingPage.roomcodes=[]
        BW_LandingPage.ratecodes=[]
        proxy = landing_page.proxy
        hotelcode=hotel_url.split('||')[0].strip()
        BW_Hotel.hotelname = hotel_url.split('||')[1].strip()

        format_str = '%d/%m/%Y'  # The format
        inDate = landing_page.check_in
        outDate = BW_LandingPage.checkOut_date

        yy1, mm1, dd1 = inDate.year, inDate .month, inDate.day
        yy2, mm2, dd2 = outDate.year, outDate.month, outDate.day
        if (len(str(mm1))) == 1:
            mm1 = '0' + str(mm1)
            mm2 = '0' + str(mm2)
        BW_LandingPage.formattedoutdate = str(yy2) + '-' + str(mm2) + '-' + str(dd2)
        BW_LandingPage.formattedindate = str(yy1) + '-' + str(mm1) + '-' + str(dd1)

        newheaders={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'www.bestwestern.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': hotel_url.split('| ')[-1].strip()
        }

        rateplanurl="https://www.bestwestern.com/bin/bestwestern/proxy?gwServiceURL=RIM_SELL_ORDER&hotelid="+str(hotelcode)+"&includeGatedRate=true"
        rp_html,rp_obj, _ = self.get_request(rateplanurl,newheaders,proxy, driver=BW_LandingPage.HOTEL_LIST_DRIVER,timeout=30)
        if rp_obj.status_code==200:
            detail=rp_html
            rp_dict=json.loads(rp_html)
            for rp in range(0,len(rp_dict)):
                r= rp_dict[rp]['rateCode']+ "|" +rp_dict[rp]['shortName']
                BW_LandingPage.ratecodes.append(r)
            newheaders={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'www.bestwestern.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': hotel_url.split('| ')[-1].strip()
            }

            if 'RACK|FLEXIBLE RATE' not in BW_LandingPage.ratecodes:
                BW_LandingPage.ratecodes.append('RACK|FLEXIBLE RATE')

            for rc in range(0,len(BW_LandingPage.ratecodes)):
                code=BW_LandingPage.ratecodes[rc].split('|')[0].strip()
                roomdetailurl=""
                roomdetailurl = "https://www.bestwestern.com/bin/bestwestern/proxy?gwServiceURL=ROOM_RATE_PLAN"
                roomdetailurl= roomdetailurl + "&hotelid="+str(hotelcode)+"&rateplan="+str(code)
                roomdetailurl= roomdetailurl+"&&checkinDate="+str(landing_page.formattedindate)+"&checkoutDate="+str(landing_page.formattedoutdate)
                roomdetailurl=roomdetailurl+"&numAdult="+str(landing_page.adults)+"&numChild=0&childrenAge=0&langCode=en_US"
                print(roomdetailurl)
                roomlinks.append(roomdetailurl)
                room_html, room_obj, _ = self.get_request(roomdetailurl, newheaders, proxy,driver=BW_LandingPage.HOTEL_LIST_DRIVER, timeout=30)
                if room_obj.status_code==200:
                    fulllist.append(room_html)
            with open("BW_Hoteldetail1.html", "w", encoding="utf-8") as file:
                file.write(str(fulllist))

            self.TRL.debug_log('Getting Hotel from URL:%s' % hotel_url, landing_page.request_id, landing_page.sub_request_id,landing_page.request_run_id, proxy=proxy, headers=newheaders)

        html_elem = {'hotel_html': rp_html +"|hotelprofile:: " + str(hotel_url),
                     'room_html':fulllist,
                     'price_html':None,
                     'latitude_html': None}

        return self(landing_page, html_elem)

    @property
    def _get_name(self):
        """
        return hotel name from hotelNameXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        return BW_Hotel.hotelname


    @property
    def _get_html(self):
        """
        :return: sample {'landingPage': self._landing_page._html}
        """
        return {
            'landingPage': self._landing_page._html,
            'hotel_html': self._html['hotel_html'],
            'room_html': self._html['room_html'],
            'price_html':self._html['price_html']
        }
    @property
    def _get_room_types(self):
        """
        :return: [{ 'roomtypehtml': 'page_source_of_roomtype1', 'pricehtml': 'page_source_of_price_for_roomtype1'},
                  { 'roomtypehtml': 'page_source_of_roomtype2', 'pricehtml': 'page_source_of_price_for_roomtype2'}]
        """
        roomType = self._html['room_html']
        price = None
        return {'roomTypeHTML': roomType, 'priceHTML': price}

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
        hotel_data['checkOut'] = str(BW_LandingPage.checkOut_date)
        hotel_data['POS'] = self._landing_page.pos
        hotel_data['nights'] = self._landing_page.nights
        hotel_data['adults'] = adultvalue
        # Crawler Output
        hotel_data['htmls'] = self._get_html
        try:
            hotel_data['hotelName'] = self._get_name
        except Exception as e:
            raise self.EXCEPTIONS['HOTEL_NOT_FOUND'](str(e))
        hotel_data['roomTypes'] = self._get_room_types
        hotel_data['cachePageHTML'] = self._get_cache_page
        hotel_data['hotel_id'] = self._landing_page.hotel_web_id
        hotel_data['adult'] = adultvalue
        hotel_data['pos'] = self._landing_page.pos
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
            self._landing_page.request_run_id, proxy=self._landing_page.proxy, headers=self._landing_page.headers)
        hotel_data['meta']['cachePageURL'] = self.SERVICE_CALLS['save_cache_page'](
            self._get_cache_filename, self._get_cache_page
        )
        response = copy.deepcopy(self._landing_page.request_data)
        response['hotel'] = hotel_data
        return self.SERVICE_CALLS['save_html'](response)

class BW_LandingPage(HotelLandingPageHandler):

    HOST = 'https://www.bestwestern.com'
    HOTEL_HANDLER_CLASS = BW_Hotel
    HOTEL_LIST_DRIVER = True
    PROXY_LESS_HIT = False
    apitoken = ""
    apikey = ""
    label = ""
    starcount_resplist = []
    roomcodes=[]
    # ratecodes=[]
    ratecodes={}
    adults = ""
    checkOut_date=""
    postdata=''
    ref=""
    formattedoutdate=""
    formattedindate=""

    def __init__(self, requeset_data):
        super(BW_LandingPage, self).__init__(requeset_data)
        proxy = BW_ProxyHandler()
        proxy.initiate_new_proxy(self.domain_name, self.country)
        self.proxy = proxy

    def get_zones(self, city):
        mapped_cities = [{'city': 'Agadir',
                              'zoneName': ['Agadir', 'Souss-Massa-Draa', 'Morocco', 'Aourir', 'Souss-Massa-Draa',
                                           'Morocco',
                                           'Mirleft',
                                           'Souss-Massa-Draa', 'Morocco', 'Sidi Ifni', 'Souss-Massa-Draa', 'Morocco',
                                           'Tafraout',
                                           'Souss-Massa-Draa',
                                           'Morocco', 'Taroudant', 'Souss-Massa-Draa', 'Morocco', 'Tiznit',
                                           'Souss-Massa-Draa',
                                           'Morocco', 'AÃ¯t Baha',
                                           'Souss-Massa-Draa', 'Morocco'],
                              'zoneCode': ['-20029', '-24231', '-39669', '-47350', '-49996', '-52246', '-54825',
                                           '-21291'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},
                         {'city': 'Abu Dhabi',
                              'zoneName': ['Abu Dhabi Emirate, United Arab Emirates', 'Hatta, United Arab Emirates',
                                           "Da‘sah, Abu Dhabi Emirate, United Arab Emirates",
                                           'Jurayrah, Abu Dhabi Emirate, United Arab Emirates',
                                           'Al Rahba, Abu Dhabi Emirate, United Arab Emirates',
                                           'Ghantoot, Abu Dhabi Emirate, United Arab Emirates',
                                           'Mezairaa, Abu Dhabi Emirate, United Arab Emirates',
                                           'Al Marfa, Abu Dhabi Emirate, United Arab Emirates',
                                           'Madinat Zayid, Abu Dhabi Emirate, United Arab Emirates',
                                           'Ghayathi%2C+Abu+Dhabi+Emirate%2C+United+Arab+Emirates',
                                           'Jebel Dhanna, Abu Dhabi Emirate, United Arab Emirates'],
                              'zoneCode': ['-782066', '900040195', '-782780', '-783288', '900053578', '900039854',
                                           '-783797', '-782245', '-783485', '900052887', '900039799'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city']},
                             {'city': 'Alanya',
                              'zoneName': ['Alanya%2BCoast%2C%2BTurkey', 'Konakli, Mediterranean Region Turkey, Turkey',
                                           'Mahmutlar, Mediterranean Region Turkey, Turkey'],
                              'zoneCode': ['1719', '-761842', '-764432'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Alentejo',
                              'zoneName': ['Alentejo%2C%20Portugal', 'Alc%C3%A1cer+do+Sal%2C+Alentejo%2C+Portugal',
                                           'Santa+Clara-a-Velha%2C+Alentejo%2C+Portugal',
                                           'Sines%2C+Alentejo%2C+Portugal'],
                              'zoneCode': ['2599', '-2157431', '-2175310', '-2176834'],
                              'zoneType': ['region', 'city', 'city', 'city']},

                             {'city': 'ALGARVE',
                              'zoneName': ['Algarve%2C%20Portugal', 'Loul%C3%A9%2C+Algarve%2C+Portugal'],
                              'zoneCode': ['1064', '-2168141'],
                              'zoneType': ['region', 'city']},

                             {'city': 'Amsterdam and vicinity',
                              'zoneName': ['Vinkeveen, Utrecht Province, Netherlands', 'Lisse, Netherlands',
                                           'Mijdrecht, Utrecht Province, Netherlands', 'Noord-Holland, Netherlands',
                                           'Flevoland, Netherlands'],
                              'zoneCode': ['-2154802', '-2148742', '-2149474', '1010', '1004'],
                              'zoneType': ['city', 'city', 'city', 'region', 'region']},

                             {'city': 'Ankara',
                              'zoneName': ['Ankara%2C+Central+Anatolia+Region%2C+Turkey',
                                           'K%C4%B1z%C4%B1lcahamam%2C+Central+Anatolia+Region%2C+Turkey'],
                              'zoneCode': ['-735338', '-760816'],
                              'zoneType': ['city', 'city']},

                             {'city': 'Koh Samui',
                              'zoneName': ['Ko Mat Sum', 'Ko Tao, Surat Thani Province, Thailand',
                                           'Koh Samui, Thailand'],
                              'zoneCode': ['900051058', '-3401990', '1501'],
                              'zoneType': ['city', 'city', 'region']},

                             {'city': 'ASTURIAS',
                              'zoneName': ['Asturias%2C%20Spain', 'Nueva+de+Llanes%2C+Asturias%2C+Spain',
                                           'poo+de+Llanes%2C+Asturias%2C+Spain'],
                              'zoneCode': ['727', '-394209', '-397142'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Auckland',
                              'zoneName': ['Henderson%2C+Auckland%2C+Auckland+Region%2C+New+Zealand',
                                           'Matakana%2C+Auckland+Region%2C+New+Zealand',
                                           'Silverdale%2C+Auckland+Region%2C+New+Zealand',
                                           'Thames%2C+Waikato%2C+New+Zealand', 'Waiheke+Island%2C+New+Zealand',
                                           'Whangaparaoa%2C+Auckland+Region%2C+New+Zealand',
                                           'Auckland Region, New Zealand'],
                              'zoneCode': ['6893', '-1513513', '1518096', '401901', '4110', '1521580', '-1506909'],
                              'zoneType': ['district', 'city', 'city', 'district', 'region', 'city', 'city']},

                             {'city': 'Avignon',
                              'zoneName': ['AviÃ±Ã³n, Provenza-Alpes-Costa Azul, Francia',
                                           'Beaucaire, Languedoc-RosellÃ³n, Francia',
                                           'Carpentras, Provenza-Alpes-Costa Azul, Francia',
                                           'Cavaillon, Provenza-Alpes-Costa Azul, Francia',
                                           'Goult, Provenza-Alpes-Costa Azul, Francia',
                                           'La Roque-sur-Pernes, Provenza-Alpes-Costa Azul, Francia',
                                           'L?Isle-sur-la-Sorgue, Provenza-Alpes-Costa Azul, Francia',
                                           'Montfavet, Provenza-Alpes-Costa Azul, Francia',
                                           'Noves, Provenza-Alpes-Costa Azul, Francia',
                                           'Orgon, Provenza-Alpes-Costa Azul, Francia',
                                           'Saint-RÃ©my-de-Provence, Provenza-Alpes-Costa Azul, Francia',
                                           'Tarascon, Provenza-Alpes-Costa Azul, Francia',
                                           'Ch%C3%A2teauneuf-du-Pape%2C+Provence-Alpes-C%C3%B4te+d%27Azur%2C+France',
                                           'Tavel%2C+Languedoc-Roussillon%2C+France'],
                              'zoneCode': ['-1409631', '-1410937', '-1416801', '-1417210', '-1429799', '-1438697',
                                           '-1447280',
                                           '-1452808', '-1455498', '-1456071', '-1468251', '-1472087', '-1419113',
                                           '-1472216'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city']},

                             {'city': 'Azores',
                              'zoneName': ['Azores%2C%20Portugal', 'Flores+Island%2C+Portugal',
                                           'S%C3%A3o+Miguel+Arcanjo%2C+Azores%2C+Portugal'],
                              'zoneCode': ['1530', '3713', '-2175998'],
                              'zoneType': ['region', 'region', 'city']},

                             {'city': 'Bandung',
                              'zoneName': ['Bandung%2C%20West%20Java%2C%20Indonesia',
                                           'Ciwidey%2C+West+Java%2C+Indonesia',
                                           'Pasirjambu%2C+West+Java%2C+Indonesia'],
                              'zoneCode': ['-2671576', '-2676240', '-2691470'],
                              'zoneType': ['city', 'city', 'city']},

                             {'city': 'Beijing Peking',
                              'zoneName': ['Changping%2C+Beijing+Area%2C+China',
                                           'Beijing%20Kaixi%20Apartment%20Beijing%20Binfen%20Plaza%2C%20Daxing%2C%20Beijing%20Area%2C%20China',
                                           'Huairou%2C%20Beijing%20Area%2C%20China',
                                           'Mentougou%2C%20Beijing%20Area%2C%20China',
                                           'Miyun%2C%20Beijing%20Area%2C%20China',
                                           'Pinggu%2C%20Beijing%20Area%2C%20China',
                                           'Shunyi%2C%20Beijing%20Area%2C%20China',
                                           'Tongzhou%2C%20Beijing%20Area%2C%20China',
                                           'Xiaotangshan%20%2C%20Changping%2C%20Beijing%20Area%2C%20China',
                                           'Yanqing%2C%20Beijing%20Area%2C%20China',
                                           'Daxing%2C%20Beijing%2C%20Beijing%20Area%2C%20China', 'Beijing'],
                              'zoneCode': ['-1899952', '-1910133', '-1909989', '-1918621', '-1918909', '-1921062',
                                           '-1926733',
                                           '-1929117', '15250', '-1935819', '2942', '-1898541'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'district',
                                           'city',
                                           'district', 'city']},

                             {'city': 'Biarritz',
                              'zoneName': ['Arbonne, Aquitania, Francia', 'Bayona, Aquitania, Francia',
                                           'Biarritz, Aquitania, Francia',
                                           'Bidarray, Aquitania, Francia', 'Moliets-et-Maa, Aquitania, Francia',
                                           'Ondres, Aquitania, Francia',
                                           'Saint-Ã‰tienne-de-BaÃ¯gorry, Aquitania, Francia',
                                           'Saint-Jean-Pied-de-Port, Aquitania, Francia',
                                           'Saint-PÃ©e-sur-Nivelle, Aquitania, Francia',
                                           'Bidart%2C%20Aquitaine%2C%20France', 'Urrugne%2C%20Aquitaine%2C%20France'],
                              'zoneCode': ['-1408023', '-1410844', '-1412526', '-1412556', '-1451901', '-1455908',
                                           '-1465185',
                                           '-1466256', '-1467833', '-1412557', '-1474153'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city']},

                             {'city': 'Bournemouth',
                              'zoneName': ['Bournemouth, Dorset, United Kingdom', 'Burley, Hampshire, United Kingdom',
                                           'Lymington, Hampshire, United Kingdom', 'Poole, Dorset, United Kingdom',
                                           'New%20Forest%2C%20United%20Kingdom'],
                              'zoneCode': ['-2590498', '-2591312', '-2602323', '-2605541', '2936'],
                              'zoneType': ['city', 'city', 'city', 'city', 'region']},

                             {'city': 'Dublin',
                              'zoneName': ['Dublin County, Ireland', 'Enniskerry, Wicklow County, Ireland',
                                           'Maynooth, Kildare County, Ireland', 'Gormanston, Meath, Ireland',
                                           'Drumcondra, Dublin, Dublin County, Ireland',
                                           'Howth, Dublin County, Ireland',
                                           'Dublin, Dublin County, Ireland', 'Lucan, Dublin County, Ireland',
                                           'Park West Business Park, Clondalkin , Dublin County, Ireland',
                                           'RÃ¡th CÃºil, Dublin County, Ireland', 'citywest, Dublin County, Ireland',
                                           'Stillorgan, Dublin County, Ireland'],
                              'zoneCode': ['849', '-1502727', '-1504466', '-1503171', '1242', '-1503408', '-1502554',
                                           '-1504347',
                                           '12303', '-1505206', '-1505500', '-1505775'],
                              'zoneType': ['region', 'city', 'city', 'city', 'district', 'city', 'city', 'city',
                                           'landmark',
                                           'city',
                                           'city', 'city']},

                             {'city': 'Cairns - QLD',
                              'zoneName': ['Atherton, Queensland, Australia', 'Cairns, Queensland, Australia',
                                           'Mission Beach, Queensland, Australia',
                                           'Port Douglas, Queensland, Australia',
                                           'Cairns Beaches, Australia', 'Magnetic Island, Australia',
                                           'Townsville%2C%20Queensland%2C%20Australia'],
                              'zoneCode': ['-1556468', '-1563537', '900039036', '-1595858', '3617', '4109', '-1605526'],
                              'zoneType': ['city', 'city', 'city', 'city', 'region', 'region', 'city']},

                             {'city': 'Vizcaya - Bilbao',
                              'zoneName': ['Bilbao%2C%20Basque%20Country%2C%20Spain',
                                           'Amorebieta-Etxano, Basque Country, Spain',
                                           'Areatza, Basque Country, Spain', 'Bermeo, Basque Country, Spain',
                                           'Erandio, Basque Country, Spain', 'Galdakao, Basque Country, Spain',
                                           'Ibarrangelu, Basque Country, Spain', 'Loiu, Basque Country, Spain',
                                           'Portugalete, Basque Country, Spain', 'Sestao, Basque Country, Spain',
                                           'Sondika, Basque Country, Spain', 'Zeanuri, Basque Country, Spain'],
                              'zoneCode': ['-373608', '-370652', '900040977', '-373419', '-381554', '900050059',
                                           '-385705',
                                           '900039982',
                                           '-397288', '-402818', '900039235', '900039362'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city']},

                             {'city': 'Casablanca',
                              'zoneName': ['Casablanca%2C%20Grand%20Casablanca%2C%20Morocco',
                                           'Dar%20Bouazza%2C%20Grand%20Casablanca%2C%20Morocco',
                                           'Khouribga%2C%20Morocco',
                                           'Mohammedia%2C%20Grand%20Casablanca%2C%20Morocco'],
                              'zoneCode': ['-28159', '900051106', '8859', '-39785'],
                              'zoneType': ['city', 'city', 'region', 'city']},

                             {'city': 'A CoruNa',
                              'zoneName': ['A%20Coru%C3%B1a%2C%20Spain', 'A Capela, Galicia, Spain',
                                           'Dodro, Galicia, Spain'],
                              'zoneCode': ['1364', '-375926', '-379908'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Central and North Greece',
                              'zoneName': ['Central%20Greece%2C%20Greece', 'Epirus%2C%20Greece',
                                           'Thessalia%2C%20Greece',
                                           'Dr%C3%A1ma%2C%20Macedonia%2C%20Greece',
                                           'Itea%2C%20Central%20Greece%2C%20Greece',
                                           'Kastoria%2C%20Macedonia%2C%20Greece',
                                           'Kater%C3%ADni%2C%20Macedonia%2C%20Greece',
                                           'Kilk%C3%ADs%2C%20Macedonia%2C%20Greece',
                                           'Kozani%2C%20Macedonia%2C%20Greece',
                                           'Kymi%2C%20Central%20Greece%2C%20Greece',
                                           'Litochoro%2C%20Macedonia%2C%20Greece',
                                           'Liv%C3%A1dia%2C%20Thessalia%2C%20Greece',
                                           'Loutra%20Pozar%2C%20Kato%20Loutraki%2C%20Macedonia%2C%20Greece',
                                           'N%C3%A9oi%20P%C3%B3roi%2C%20Makedonia%2C%20Greece', 'Pieria%2C%20Greece',
                                           'Platamonas%2C%20Macedonia%2C%20Greece',
                                           'Rodopi%20Mountains%2C%20Komotini%2C%20Thrace%2C%20Greece',
                                           'Serres%2C%20Macedonia%2C%20Greece', 'Thrace%2C%20Greece',
                                           'Î’Î­ÏÎ¿Î¹Î±, ÎœÎ±ÎºÎµÎ´Î¿Î½Î¯Î±, Î•Î»Î»Î¬Î´Î±'],
                              'zoneCode': ['810', '1801', '4024', '-816779', '-818214', '-819332', '-819482', '-820532',
                                           '-821650',
                                           '-820542', '-822507', '9106618', '232893', '9096595', '4144', '900048036',
                                           '35045', '-827913',
                                           '2630', '-830366'],
                              'zoneType': ['region', 'region', 'region', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city', 'city',
                                           'city', 'landmark', 'city', 'region', 'city', 'landmark', 'city', 'region',
                                           'city']},

                             {'city': 'Cologne / Bonn',
                              'zoneName': ['Cologne, North Rhine-Westphalia, Germany',
                                           'Bonn, North Rhine-Westphalia, Germany',
                                           'Leverkusen, North Rhine-Westphalia, Germany',
                                           'Bergisch%20Gladbach%2C%20North%20Rhine-Westphalia%2C%20Germany'],
                              'zoneCode': ['-1810561', '-1750167', '-1818588', '-1746251'],
                              'zoneType': ['city', 'city', 'city', 'city']},

                             {'city': 'CORDOBA',
                              'zoneName': ['Dos Torres, AndalucÃ­a, Spain', 'Puente-Genil, AndalucÃ­a, Spain',
                                           'Cordoba Province, Spain',
                                           'Baena%2C%20Andaluc%C3%ADa%2C%20Spain'],
                              'zoneCode': ['-380034', '-397782', '750', '-372139'],
                              'zoneType': ['city', 'city', 'region', 'city']},

                             {'city': 'CORFU',
                              'zoneName': ['Corfu%2C%20Greece', 'Argyr%C3%A1des%2C%20Ionian%20Islands%2C%20Greece',
                                           'Arillas%2C%20Ionian%20Islands%2C%20Greece',
                                           'Danilia%2C%20Ionian%20Islands%2C%20Greece',
                                           'Gastouri%2C%20Ionian%20Islands%2C%20Greece',
                                           'Karous%C3%A1des%2C%20Ionian%20Islands%2C%20Greece',
                                           'Kato Korakiana, Ionian Islands, Greece',
                                           'LefkÃ­mmi, Ionian Islands, Greece', 'MarathiÃ¡s, Ionian Islands, Greece',
                                           'Nissaki Bay, Nisaki, Ionian Islands, Greece',
                                           'Paramonas, Ionian Islands, Greece',
                                           'VelonÃ¡des, Ionian Islands, Greece', 'VitalÃ¡des, Ionian Islands, Greece',
                                           'Ionian Islands, Greece'],
                              'zoneCode': ['1570', '-814671', '900047900', '900049144', '-817711', '-819188', '-819609',
                                           '-822249',
                                           '-823088', '-824872', '900040495', '-830318', '-830469', '820'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'region']},

                             {'city': 'Corsica',
                              'zoneName': ['Corsica%2C+France', 'Cervione, Corsica, France', 'Oletta, Corsica, France',
                                           'Poggiolo, Corsica, France'],
                              'zoneCode': ['1383', '-1417542', '-1455808', '-1458880'],
                              'zoneType': ['region', 'city', 'city', 'city']},

                             {'city': 'Costa Brava and Costa Barcelona-Maresme',
                              'zoneName': ['Caldes d*Estrac, Catalonia, Spain',
                                           'Sant VicenÃ§ de Montalt, Catalonia, Spain',
                                           'Goppingen, Baden-Wurttemberg, Germany', 'Maresme, Spain',
                                           'CastellÃ³ d*EmpÃºries, Catalonia, Spain', 'Llagostera, Catalonia, Spain',
                                           'Vilassar de Mar, Catalonia, Spain'],
                              'zoneCode': ['-375006', '-402303', '1387', '14000', '-376963', '-389317', '-400931'],
                              'zoneType': ['city', 'city', 'region', 'region', 'city', 'city', 'city']},

                             {'city': 'Costa De La Luz (Cadiz)',
                              'zoneName': ['Costa%20de%20la%20Luz%2C%20Spain', 'Los CaÃ±os de Meca, AndalucÃ­a, Spain'],
                              'zoneCode': ['1401', '-389863'],
                              'zoneType': ['region', 'city']},

                             {'city': 'COSTA DEL SOL',
                              'zoneName': ['Algarrobo-Costa, AndalucÃ­a, Spain', 'Caleta De Velez, AndalucÃ­a, Spain',
                                           'San Luis de Sabinillas, AndalucÃ­a, Spain', 'Costa del Sol, Spain',
                                           'Manilva, AndalucÃ­a, Spain', 'Torrox Costa, AndalucÃ­a, Spain'],
                              'zoneCode': ['900048900', '900040697', '-401024', '1402', '-390948', '900040618'],
                              'zoneType': ['city', 'city', 'city', 'region', 'city', 'city']},

                             {'city': 'Crete',
                              'zoneName': ['Crete%2C%20Greece', 'Ãdhele, Rethymno, Greece', 'Almirida, Chania, Greece',
                                           'Kalo Chorio, Crete, Greece', 'Kamilari, Central Crete, Greece'],
                              'zoneCode': ['811', '-813176', '-813685', '-818643', '-818821'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city']},

                             {'city': 'Dubai',
                              'zoneName': [
                                  'Dubai Desert Conservation Reserve, Murquab, Dubai Emirate, United Arab Emirates',
                                  'Dubai%2C%20Dubai%20Emirate%2C%20United%20Arab%20Emirates',
                                  'Murquab, Dubai Emirate, United Arab Emirates'],
                              'zoneCode': ['900053984', '-782831', '900051432'],
                              'zoneType': ['landmark', 'city', 'city']},

                             {'city': 'BALI',
                              'zoneName': ['Bali%2C%20Indonesia', 'Ubud, Bali, Indonesia', 'Seminyak, Bali, Indonesia',
                                           'Legian, Bali, Indonesia', 'Kuta, Bali, Indonesia',
                                           'Canggu, Bali, Indonesia',
                                           'Lembongan, Bali, Indonesia', 'Sanur, Bali, Indonesia'],
                              'zoneCode': ['835', '-2701757', '900040134', '900048191', '-2683839', '900048236',
                                           '-2684938',
                                           '325646'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'BALI',
                              'zoneName': ['Bali%2C%20Indonesia', 'Ubud, Bali, Indonesia', 'Seminyak, Bali, Indonesia',
                                           'Legian, Bali, Indonesia', 'Kuta, Bali, Indonesia',
                                           'Canggu, Bali, Indonesia',
                                           'Lembongan, Bali, Indonesia', 'Sanur, Bali, Indonesia'],
                              'zoneCode': ['835', '-2701757', '900040134', '900048191', '-2683839', '900048236',
                                           '-2684938',
                                           '325646'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'ACAPULCO',
                              'zoneName': ['Acapulco%2C%20Guerrero%2C%20Mexico', 'Barra Vieja, Guerrero, Mexico'],
                              'zoneCode': ['-1649039', '900051418'],
                              'zoneType': ['city', 'city']},

                             {'city': 'BUCHAREST',
                              'zoneName': ['Bucharest, Romania', 'Otopeni, Ilfov, Romania',
                                           'Bucharest - Ilfov Region, Romania'],
                              'zoneCode': ['-1153951', '-1165889', '14490'],
                              'zoneType': ['city', 'city', 'region']},

                             {'city': 'Buenos Aires',
                              'zoneName': ['Buenos Aires, Argentina', 'Provincia de Buenos Aires, Argentina',
                                           'Buenos Aires, Argentina'],
                              'zoneCode': ['-979186', '3619', '-979186'],
                              'zoneType': ['city', 'region', 'city']},

                             {'city': 'Pyrenees - Aragon',
                              'zoneName': ['Pirineo%20Aragon%C3%A9s%2C%20Spain', 'AzanÃºy, Aragon, Spain',
                                           'BoltaÃ±a, Aragon, Spain'],
                              'zoneCode': ['2762', '-372047', '-373867'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'W. Cape-Cape Town-Garden Route',
                              'zoneName': ['Agulhas, Overberg, South Africa', 'Barrydale, Western Cape, South Africa',
                                           'Cape Town, Western Cape, South Africa',
                                           'Franschhoek, Western Cape, South Africa',
                                           'George, Western Cape, South Africa', 'Kalk Bay, Western Cape, South Africa',
                                           'Kleinberg, Western Cape, South Africa',
                                           'Knysna, Western Cape, South Africa',
                                           'Kommetjie, Cape Peninsula, South Africa',
                                           'Langebaan, Cape West Coast, South Africa',
                                           'Montagu, Western Cape, South Africa',
                                           'Mossel Bay, Garden Route, South Africa',
                                           'Oudtshoorn, Western Cape, South Africa',
                                           'Paarl, Western Cape, South Africa',
                                           'Paternoster, Western Cape, South Africa',
                                           'Plettenberg Bay, Garden Route, South Africa',
                                           'Prince Albert, Western Cape, South Africa',
                                           'Pringle Bay, Western Cape, South Africa',
                                           'Robertson, Western Cape, South Africa',
                                           'Roggeveld, Western Cape, South Africa',
                                           'Saldanha, Western Cape, South Africa',
                                           'Sedgefield, Western Cape, South Africa',
                                           'Simon?s Town, Western Cape, South Africa',
                                           'Somerset West, Western Cape, South Africa',
                                           'Stellenbosch, Western Cape, South Africa',
                                           'Stormsrivier, Eastern Cape, South Africa',
                                           'Swellendam, Western Cape, South Africa',
                                           'Tulbagh, Western Cape, South Africa',
                                           'Wellington, Western Cape, South Africa',
                                           'Wilderness, Western Cape, South Africa',
                                           'Hermanus, South Africa',
                                           'Oranjezicht, Cape Town, Western Cape, South Africa',
                                           'Caledon, Western Cape, South Africa',
                                           'Cape Town International Airport, Cape Town, Western Cape, South Africa',
                                           'Kagga Kamma Nature Reserve, Lochlynne, Western Cape, South Africa'],
                              'zoneCode': ['-1206410', '-1209278', '-1217214', '-1228880', '-1230653', '-1241268',
                                           '-1244023',
                                           '-1246436', '-1247063', '-1251042', '-1261967', '-1262929', '-1270304',
                                           '-1270835',
                                           '-1271442', '-1273101', '-1273830', '-1273851', '-1277201', '-1277397',
                                           '-1280475',
                                           '-1282144', '-1283450', '-1285082', '-1287082', '-1287770', '-1289176',
                                           '-1292611', '-13'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'region',
                                           'district', 'city',
                                           'airport', 'hotel']},

                             {'city': 'Genoa',
                              'zoneName': ['Genoa%2C%20Liguria%2C%20Italy', 'Imperia, Liguria, Italy',
                                           'La Spezia, Liguria, Italy',
                                           'Recco, Liguria, Italy', 'Sestri Levante, Liguria, Italy',
                                           'Spotorno, Liguria, Italy'],
                              'zoneCode': ['-118400', '-119237', '-119773', '126173', '129637', '130131'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'North Sardinia',
                              'zoneName': ['Porto Ottiolu, Sardinia, Italy', 'Aglientu%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Alghero%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Arzachena%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Badesi%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Budoni%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Cala%20Gonone%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Valledoria%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Dorgali%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Golfo%20Aranci%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'La%20Maddalena%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Nuoro%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Olbia%2C%20Cerde%C3%B1a%2C%20Italia', 'Palau%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Porto%20Cervo%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'San%20Giovanni%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'San%20Teodoro%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Santa%20Teresa%20di%20Gallura%2C%20Sardegna%2C%20Italia',
                                           'Sassari%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Sorso%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Tanaunella%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Tergu%2C%20Cerde%C3%B1a%2C%20Italia',
                                           'Sardinia, Italy', 'Sardinia North, Italy'],
                              'zoneCode': ['900040322', '-127509', '-110164', '-110765', '-110973', '900039373',
                                           '-112496',
                                           '900039181',
                                           '-116905', '-126199', '-119608', '-123178', '-123255', '-123746',
                                           '900039171',
                                           '-127602',
                                           '-128764', '-128723', '-129050', '-129976', '-130460', '14415', '908',
                                           '4187'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'region', 'region']},

                             {'city': 'Pyrenees - Catalan',
                              'zoneName': ['BoÃ­ TaÃ¼ll, Spain', 'Escunhau, Catalunya, Espanya',
                                           'Llimiana, Catalonia, Spain',
                                           'MollÃ³, Catalonia, Spain', 'SalardÃº, Catalonia, Spain',
                                           'Cellers, Cataluna, Espana',
                                           'Llivia, Pirineos, Espana', 'Montseny, Cataluna, Espana',
                                           'Pirineo catalan, Espana',
                                           'Valencia de Aneu, Catalonia, Spain'],
                              'zoneCode': ['3873', '-381760', '-389449', '-392440', '-400114', '-402616', '-389454',
                                           '-392880', '2932',
                                           '-406138'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'region',
                                           'city']},

                             {'city': 'Istria',
                              'zoneName': ['Funtana, Istria, Croatia', 'Tar, Istria, Croatia', 'Istria%2C%20Croatia'],
                              'zoneCode': ['-80405', '-98087', '1763'],
                              'zoneType': ['city', 'city', 'region']},

                             {'city': 'Shanghai',
                              'zoneName': ['Jinshan, Shanghai Area, China', 'Nanhui, Shanghai Area, China',
                                           'shanghai%20area'],
                              'zoneCode': ['-1912712', '-1910935', '3245'],
                              'zoneType': ['city', 'city', 'region']},

                             {'city': 'Rhodes',
                              'zoneName': ['Asgourou, Dodecanese, Greece', 'Koskinou, Dodecanese, Greece',
                                           'Pastida, Dodecanese, Greece',
                                           'Rhodes%2C%20Greece', 'Dodecanese, Greece'],
                              'zoneCode': ['900040602', '900048454', '900039631', '1591', '813'],
                              'zoneType': ['city', 'city', 'city', 'region', 'region']},

                             {'city': 'Navarra',
                              'zoneName': ['Ablitas, Navarre, Spain', 'Berrioplano, Navarre, Spain',
                                           'Navarra%2C%20Spain'],
                              'zoneCode': ['-369034', '-373473', '769'],
                              'zoneType': ['city', 'city', 'region']},

                             {'city': 'Washington D.C. - DC',
                              'zoneName': ['Clinton, Maryland, USA', 'Dumfries, Virginia, USA', 'Largo, Maryland, USA',
                                           'Takoma Park, Maryland, USA', 'Woodbridge, Virginia, USA',
                                           'Washington DC Metropolitan area, USA',
                                           'Washington Dulles International Airport, Washington, District of Columbia, USA',
                                           'Springfield, Virginia, USA', 'Alexandria, Virginia, USA',
                                           'Bethesda, Maryland, USA',
                                           'Greenbelt, Maryland, USA', 'Fairfax, Virginia, USA',
                                           'Herndon, Virginia, USA',
                                           'Triangle, Virginia, USA', 'Vienna, Virginia, USA',
                                           'Upper Marlboro, Maryland, USA',
                                           'McLean, Virginia, USA', 'Lanham, Maryland, USA',
                                           'National Harbor, Maryland, USA',
                                           'Front Royal, Virginia, USA', 'Gaithersburg, Maryland, USA'],
                              'zoneCode': ['20055003', '20137352', '20057536', '20021285', '20142779', '2470', '57',
                                           '20141715',
                                           '20135442', '20054014', '20056420', '20137588', '20138420', '20142126',
                                           '20142273',
                                           '20060819', '20139652', '20057529', '900040272', '20137883', '20056122'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'region', 'airport', 'city', 'city',
                                           'city', 'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city']},

                             {'city': 'Oslo',
                              'zoneName': ['Asker, Akershus, Norway', 'Drammen, Buskerud, Norway',
                                           'Gardermoen, Akershus, Norway',
                                           'Kolbotn, Akershus, Norway', 'Skjetten, Akershus, Norway',
                                           'Oslo%2C%20Oslo%20County%2C%20Norway'],
                              'zoneCode': ['-251754', '-255997', '-259312', '-266499', '900040219', '-273837'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Zaragoza',
                              'zoneName': ['Zaragoza%2C%20Aragon%2C%20Spain', 'Alhama de AragÃ³n, Aragon, Spain',
                                           'Calatayud, Aragon, Spain', 'CariÃ±ena, Aragon, Spain',
                                           'Ejea de los Caballeros, Aragon, Spain',
                                           'Tarazona de AragÃ³n, Aragon, Spain'],
                              'zoneCode': ['-409149', '-370189', '-374989', '-376198', '-380169', '-403875'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Peloponesse',
                              'zoneName': ['Arcadia, Greece', 'Filiatra, Peloponnese, Greece',
                                           'Methoni, Peloponnese, Greece',
                                           'StoÃºpa, Peloponnese, Greece', 'VounÃ¡ria, Peloponnese, Greece',
                                           'Peloponnese%2C%20Greece'],
                              'zoneCode': ['4204', '-817325', '-823879', '-828978', '-830672', '4023'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'region']},

                             {'city': 'Alicante - Costa Blanca',
                              'zoneName': ['Alcoy, Valencia Community, Spain', 'Pego, Valencia Community, Spain',
                                           'Alicante Province, Spain',
                                           'Alicante Airport, Alicante, Valencia Community, Spain',
                                           'Alfaz del Pi, Valencia Community, Spain', 'Orba, Valencia Community, Spain',
                                           'Guadalest, Valencia Community, Spain'],
                              'zoneCode': ['-369904', '900039298', '742', '138', '900039290', '-394605', '-384601'],
                              'zoneType': ['city', 'city', 'region', 'airport', 'city', 'city', 'city']},

                             {'city': 'Zurich',
                              'zoneName': [' Bad Zurzach, Aargau, Switzerland', ' Spreitenbach, Aargau, Switzerland',
                                           ' Villmergen, Aargau, Switzerland', ' Wildegg, Aargau, Switzerland',
                                           ' Canton of Zurich, Switzerland', 'Aarau, Aargau, Switzerland',
                                           'Einsiedeln, Canton of Schwyz, Switzerland'],
                              'zoneCode': ['-2554940', '-2554299', '-2554709', '-2554839', '672', '-2550904',
                                           '-2551870'],
                              'zoneType': [' city', ' city', ' city', ' city', ' region', ' region', 'city', 'city',
                                           'city']},

                             {'city': 'Vienna',
                              'zoneName': ['Vienna, Vienna (state), Austria', 'Vosendorf, Niederosterreich, Austria',
                                           'Baden, Niederosterreich, Austria', 'Schwechat, Lower Austria, Austria',
                                           'Fischamend Dorf, Lower Austria, Austria',
                                           'Irenental, Lower Austria, Austria'],
                              'zoneCode': ['-1995499', '-1994708', '-1974493', '-1991440', '-1977049', '-3856253'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Lisbon',
                              'zoneName': ['Alfragide, ?Lisbon Region, ?Portugal', 'Almada, ?Lisbon Region, ?Portugal',
                                           'Belverde, Amora, Portugal',
                                           'Costa da Caparica, ?RegiÃ£o de Lisboa, ?Portugal',
                                           'Linda-a-Velha, Lisbon Region, Portugal', 'Montijo, Lisbon Region, Portugal',
                                           'Palmela, Lisbon Region, Portugal',
                                           'Santa Iria da AzÃ³ia, RegiÃ£o de Lisboa, Portugal',
                                           'Sesimbra, Lisbon Region, Portugal', 'SetÃºbal, Lisbon Region, Portugal',
                                           'Vila Franca de Xira, Lisbon Region, Portugal',
                                           'Vila Fresca, RegiÃ£o de Lisboa, Portugal',
                                           'Queluz', 'Lisbon, Lisbon Region, Portugal', 'Oeste, Portugal',
                                           'Lisbon Region, Portugal'],
                              'zoneCode': ['-2157784', '-2157858', 'ChIJUwOTk1pKGQ0RftChd6UaBJI', '-2163719',
                                           '-2167950',
                                           '-2170180',
                                           '-2171402', '-2175383', '-2176735', '-2176724', '-2179519', '-2179523',
                                           '-2173585',
                                           '-2167973', '3404', '-2167973'],
                              'zoneType': ['city', 'city', 'landmark', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city', 'city',
                                           'city', 'city', 'city', 'region', 'city']},

                             {'city': 'Fethiye-Oludeniz',
                              'zoneName': ['Fethiye, Aegean Region, Turkey', 'Faralya, Aegean Region, Turkey',
                                           'GÃ¶cek, Aegean Region, Turkey', 'Oludeniz, Aegean Region, Turkey',
                                           'Ovacik, Aegean Region, Turkey'],
                              'zoneCode': ['-749044', '900039903', '-761520', '900039659', '-750073'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city']},

                             {'city': 'Dubrovnik-South Dalmatia',
                              'zoneName': ['Sipan%2C%20Vrboska%2C%20Split-Dalmatia%20County%2C%20Croatia',
                                           'Dubrovnik-Neretva%20County%2C%20Croatia', 'Mljet%20Island%2C%20Croatia',
                                           'Kolocep Island, Croatia', 'Pula, Croatia'],
                              'zoneCode': ['-101034', '4768', '2180', '2488', '-93462'],
                              'zoneType': ['city', 'region', 'region', 'region', 'city']},

                             {'city': 'FUERTEVENTURA',
                              'zoneName': ['Costa Calma, Canary Islands, Spain',
                                           'Morro del Jable, Canary Islands, Spain',
                                           'Fuerteventura, Spain', 'La Pared, Canary Islands, Spain'],
                              'zoneCode': ['900039316', '-393147', '752', '900050612'],
                              'zoneType': ['city', 'city', 'region', 'city']},

                             {'city': 'Tenerife',
                              'zoneName': ['Tenerife%2C%20Spain', 'San Isidro, Canary Islands, Spain',
                                           'Santa Ãšrsula, Canary Islands, Spain'],
                              'zoneCode': ['777', '-400820', '-402011'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Toulouse',
                              'zoneName': ['Blagnac, Midi-PyrÃ©nÃ©es, France', 'Merville, Midi-PyrÃ©nÃ©es, France',
                                           'Moissac, Midi-PyrÃ©nÃ©es, France', 'Montauban, Midi-PyrÃ©nÃ©es, France',
                                           'Seilh, Midi-PyrÃ©nÃ©es, France', 'Agen, Aquitaine, France',
                                           'Grenade, Basse-Terre, Guadeloupe', 'Toulouse, Midi-PyrÃ©nÃ©es, France'],
                              'zoneCode': ['-1412858', '-1451122', '-1451835', '-1452421', '-1470202', '-1406659',
                                           '-1202986',
                                           '-1473166'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Toronto',
                              'zoneName': ['Toronto, Ontario, Canada', 'Oakville, Ontario, Canada',
                                           'Burlington, Ontario, Canada',
                                           'Newmarket, Ontario, Canada', 'Milton, Ontario, Canada',
                                           'Markham, Ontario, Canada',
                                           'Mississauga, Ontario, Canada', 'Pickering, Ontario, Canada',
                                           'Vaughan, Ontario, Canada'],
                              'zoneCode': ['-574890', '-570498', '-561857', '-570118', '-569324', '-568752', '-569427',
                                           '-571264',
                                           '900040671'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Hanoi and North',
                              'zoneName': ['Ha Long Bay, Vietnam', 'Ha Noi Municipality, Vietnam', 'Ninh Binh, Vietnam',
                                           'Sapa, Lao Cai, Vietnam', 'Hai Phong, Hai Phong Municipality, Vietnam'],
                              'zoneCode': ['5288', '6228', '6267', '-3728113', '-3714825'],
                              'zoneType': ['region', 'region', 'region', 'city', 'city']},

                             {'city': 'Hong Kong',
                              'zoneName': ['Hong+Kong%2C+Hong+Kong', 'Sham Shui Po, Hong Kong, Hong Kong'],
                              'zoneCode': ['-1353149', '11036'],
                              'zoneType': ['city', 'district']},

                             {'city': 'Halkidiki',
                              'zoneName': ['Halkidiki%2C%20Greece', 'Ammoulliani, Stagira-Akanthos, Halkidiki, Greece',
                                           'Nea Moudania, Macedonia, Greece'],
                              'zoneCode': ['819', 'ChIJpzcjMJrHqBQRoObEu_wFcbA', '-824569'],
                              'zoneType': ['region', 'landmark', 'city']},

                             {'city': 'Hammamet',
                              'zoneName': ['Hammamet%2C+Nabeul%2C+Tunisia', 'Nabeul, Nabeul, Tunisia'],
                              'zoneCode': ['-722356', '-727574'],
                              'zoneType': ['city', 'city']},

                             {'city': 'Ibiza',
                              'zoneName': ['Ibiza%2C%20Spain', 'Cala Llonga, Balearic Islands, Spain',
                                           'Es Figueral Beach, Balearic Islands, Spain',
                                           'Santa InÃ©s, Islas Baleares, EspaÃ±a'],
                              'zoneCode': ['1408', '900048015', '900050266', '-401761'],
                              'zoneType': ['region', 'city', 'city', 'city']},

                             {'city': 'Seoul',
                              'zoneName': ['Seoul, South Korea', 'Seongnam, Gyeonggi-do, South Korea',
                                           'Guro-Gu, Seoul, South Korea'],
                              'zoneCode': ['-716583', '160125', '2415'],
                              'zoneType': ['city', 'city', 'district']},

                             {'city': 'New York Area - NY',
                              'zoneName': ['New York city, New York State, United States of America',
                                           'Brooklyn, New York State, United States of America',
                                           'Floral Park, New York State, USA',
                                           'Queens, New York State, USA', 'New Jersey, USA',
                                           'Bay Ridge, New York State, USA',
                                           'Bellerose, New York State, USA',
                                           'Staten Island, New York State, United States of America, North America',
                                           'Nanuet, New York State, USA, North America',
                                           'Amityville, New York State, USA',
                                           'Bay Shore, New York State, USA', 'Great Neck, New York State, USA',
                                           'Holtsville, New York State, USA', 'Rockville Centre, New York State, USA',
                                           'Roslyn, New York State, USA'],
                              'zoneCode': ['20088325', '20085207', '20086445', '20089077', '2616', '20084891',
                                           '20084955',
                                           '900040555',
                                           '20088244', '20084690', '20084892', '20086787', '20087151', '20089262',
                                           '20089305'],
                              'zoneType': ['city', 'city', 'city', 'city', 'region', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city']},

                             {'city': 'Osaka',
                              'zoneName': ['Osaka%2C%20Osaka%20Prefecture%2C%20Japan',
                                           'Izumi-Sano, Osaka Prefecture, Japan',
                                           'Sakai, Osaka Prefecture, Japan'],
                              'zoneCode': ['-240905', '-231191', '-242029'],
                              'zoneType': ['city', 'city', 'city']},

                             {'city': 'Kyoto',
                              'zoneName': ['Ine, Kyoto Prefecture, Japan', 'Kyoto%2C%20Kyoto%2C%20Japan',
                                           'Fukuchiyama, Kyoto, Japan',
                                           'Kameoka, Kyoto, Japan', 'Kusatsu, Shiga, Japan', 'Miyazu, Kyoto, Japan',
                                           'Uji, Kyoto, Japan',
                                           'Yosano, Kyoto, Japan'],
                              'zoneCode': ['ChIJ54StjXUK_18RKBn7P9WjHn0', '-235402', '-227323', '-231812', '-235206',
                                           '-236968',
                                           '-247265', '-247265'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Paris',
                              'zoneName': ['Disneyland Paris, France', 'Dourdan, Ile de France, France',
                                           'Melun, Ile de France, France',
                                           'Parc Asterix Amusement Park, Plailly, Picardy, France',
                                           'Ile de France, France'],
                              'zoneCode': ['1569', '-1424429', '-1450767', '1582', '1425'],
                              'zoneType': ['region', 'city', 'city', 'landmark', 'region']},

                             {'city': 'Kuantan and Pahang',
                              'zoneName': ['Kampung Janda Baik, Pahang, Malaysia'],
                              'zoneCode': ['-2403030'],
                              'zoneType': ['city']},

                             {'city': 'Boston - MA',
                              'zoneName': ['Boston%2C+Massachusetts%2C+USA', 'Marlborough, Massachusetts, USA',
                                           'Leominster, Massachusetts, USA', 'Milford, Massachusetts, USA',
                                           'Westborough, Massachusetts, USA', 'Devens, Massachusetts, USA',
                                           'Hudson, Massachusetts, USA',
                                           'Lawrence, Massachusetts, USA', 'Brockton, Massachusetts, USA',
                                           'Tewksbury, Massachusetts, USA', 'Andover, Massachusetts, USA',
                                           'Chelsea, Massachusetts, USA',
                                           'Concord, Massachusetts, USA', 'Framingham, Massachusetts, USA',
                                           'Westminster, Massachusetts, USA', 'Hull, Massachusetts, USA'],
                              'zoneCode': ['2442', '20062593', '20062509', '20062653', '20063624', '900054565',
                                           '20062422',
                                           '20062500',
                                           '20061756', '20063407', '20061593', '20061921', '20061976', '20062249',
                                           '20063635',
                                           '20062423'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Tokyo',
                              'zoneName': ['Tokyo, Tokyo Prefecture, Japan', 'Haneda, Tokyo, Tokyo To, Japan',
                                           'Narita, Tokyo, Tokyo To, Japan', 'Hachioji, Tokyo Prefecture, Japan',
                                           'Machida, Tokyo Prefecture, Japan',
                                           'Shinagawa Area, Tokyo, Tokyo Prefecture, Japan',
                                           'Tachikawa, Tokyo Prefecture, Japan'],
                              'zoneCode': ['-246227', '5', '30', '-228119', '-235462', '3049', '-244665'],
                              'zoneType': ['city', 'airport', 'airport', 'city', 'city', 'district', 'city']},

                             {'city': 'Antalya',
                              'zoneName': ['Antalya%20Province%2C%20Turkey', 'Mediterranean Region Turkey, Turkey',
                                           'Alanya%2BCoast%2C%2BTurkey', 'Konakli, Mediterranean Region Turkey, Turkey',
                                           'Mahmutlar, Mediterranean Region Turkey, Turkey',
                                           'Side%2C%20Mediterranean%20Region%20Turkey%2C%20Turkey',
                                           'Side Coast, Turkey',
                                           'Manavgat, Mediterranean Region Turkey, Turkey',
                                           'Kizilot, Mediterranean Region Turkey, Turkey',
                                           'Kalkan, Mediterranean Region Turkey, Turkey',
                                           'Kas, Mediterranean Region Turkey, Turkey',
                                           'Kizilagac, Mediterranean Region Turkey, Turkey',
                                           'Cirali, Mediterranean Region Turkey, Turkey', 'Kemer%2C%20Turkey',
                                           'city Center, Antalya, Mediterranean Region Turkey, Turkey',
                                           'Konyaalti Beach, Antalya, Mediterranean Region Turkey, Turkey',
                                           'Old Town Kaleici, Antalya, Mediterranean Region Turkey, Turkey',
                                           'Eski Lara, Antalya, Mediterranean Region Turkey, Turkey'],
                              'zoneCode': ['3902', '1088', '1719', '-761842', '-764432', '900039392', '5775', '-764597',
                                           '-761115',
                                           '-755728', '-758319', '900040050', '-743770', '3887', '1622', '1172', '1171',
                                           '5901'],
                              'zoneType': ['region', 'region', 'region', 'city', 'city', 'city', 'region', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'region', 'district', 'district', 'district',
                                           'district']},

                             {'city': 'Cannes',
                              'zoneName': ["Antibes, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Cannes, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Golfe-Juan, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Grasse, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Juan-les-Pins, Provence-Alpes-CÃ´te d'Azur, France",
                                           "La Gaude, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Mandelieu-la-Napoule, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Mougins, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Opio, Provence-Alpes-CÃ´te d'Azur, France",
                                           "ThÃ©oule-sur-Mer, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Tourrettes, Provence-Alpes-CÃ´te d'Azur, France"],
                              'zoneCode': ['-1407848', '-1416533', '-1429633', '-1430518', '-1433243', '-1436238',
                                           '900040131',
                                           '-1453878', '-1455947', '-1472539', '900040896'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city']},

                             {'city': 'Antalya',
                              'zoneName': ['Antalya%20Province%2C%20Turkey', 'Mediterranean Region Turkey, Turkey',
                                           'Alanya%2BCoast%2C%2BTurkey', 'Konakli, Mediterranean Region Turkey, Turkey',
                                           'Mahmutlar, Mediterranean Region Turkey, Turkey',
                                           'Side%2C%20Mediterranean%20Region%20Turkey%2C%20Turkey',
                                           'Side Coast, Turkey',
                                           'Manavgat, Mediterranean Region Turkey, Turkey',
                                           'Kizilot, Mediterranean Region Turkey, Turkey',
                                           'Kalkan, Mediterranean Region Turkey, Turkey',
                                           'Kas, Mediterranean Region Turkey, Turkey',
                                           'Kizilagac, Mediterranean Region Turkey, Turkey',
                                           'Cirali, Mediterranean Region Turkey, Turkey', 'Kemer%2C%20Turkey',
                                           'city Center, Antalya, Mediterranean Region Turkey, Turkey',
                                           'Konyaalti Beach, Antalya, Mediterranean Region Turkey, Turkey',
                                           'Old Town Kaleici, Antalya, Mediterranean Region Turkey, Turkey',
                                           'Eski Lara, Antalya, Mediterranean Region Turkey, Turkey'],
                              'zoneCode': ['3902', '1088', '1719', '-761842', '-764432', '900039392', '5775', '-764597',
                                           '-761115',
                                           '-755728', '-758319', '900040050', '-743770', '3887', '1622', '1172', '1171',
                                           '5901'],
                              'zoneType': ['region', 'region', 'region', 'city', 'city', 'city', 'region', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'region', 'district', 'district', 'district',
                                           'district']},

                             {'city': 'Copenhagen',
                              'zoneName': ['Ballerup, Hovedstaden, Denmark', 'Copenhagen, Hovedstaden, Denmark',
                                           'Roskilde, Region SjÃ¦lland, Denmark', 'VedbÃ¦k, Hovedstaden, Denmark',
                                           'Hvidovre, Hovedstaden, Denmark', 'Glostrup, Hovedstaden, Denmark',
                                           'Kongens Lyngby, Hovedstaden, Denmark', 'Gentofte, Hovedstaden, Denmark',
                                           'IshÃ¸j, Hovedstaden, Denmark'],
                              'zoneCode': ['-2739711', '-2745636', '-2749584', '-2753386', '-2744531', '-2742703',
                                           '-2745593',
                                           '-2742544', '-2744682'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Antwerp',
                              'zoneName': ['Grobbendonk, Antwerpen Province, Belgium'],
                              'zoneCode': ['-1959320'],
                              'zoneType': ['city']},

                             {'city': 'Bodrum',
                              'zoneName': ['G%C3%BCmbet%2C%20Aegean%20Region%2C%20Turkey', 'Golturkbuku%2C%20Turkey',
                                           'Yal%C4%B1kavak%2C%20Aegean%20Region%2C%20Turkey', 'Turgutreis%2C%20Turkey',
                                           'Bitez%2C%20Aegean%20Region%2C%20Turkey', 'Torba%2C%20Turkey',
                                           'Gumusluk%2C%20Aegean%20Region%2C%20Turkey',
                                           'Gundogan%2C%20Aegean%20Region%2C%20Turkey',
                                           'Ortakent%2C%20Aegean%20Region%2C%20Turkey',
                                           'Akyarlar%2C%20Aegean%20Region%2C%20Turkey',
                                           'Yaliciflik%2C%20Aegean%20Region%2C%20Turkey',
                                           'Guvercinlik, Aegean Region, Turkey',
                                           'Aegean Region, Turkey'],
                              'zoneCode': ['900039692', '900039693', '-775353', '-757891', '-739511', '900039974',
                                           '-751154',
                                           '900039691', '-766917', '-734436', '900039694', '-751683', '900051418'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city']},

                             {'city': 'Colombo',
                              'zoneName': ['Moratuwa, Colombo District, Sri Lanka'],
                              'zoneCode': ['-2229249'],
                              'zoneType': ['city']},

                             {'city': 'Guangzhou',
                              'zoneName': ['Guangzhou%2C%20Guangdong%2C%20China', 'Qingyuan, Guangdong, China',
                                           'Zengcheng, Guangdong, China'],
                              'zoneCode': ['-1907161', '-1922181', '-1914961'],
                              'zoneType': ['city', 'city', 'city']},

                             {'city': 'KwaZulu Natal - Durban',
                              'zoneName': ['Empangeni, KwaZulu-Natal, South Africa',
                                           'Jozini, KwaZulu-Natal, South Africa'],
                              'zoneCode': ['-1226918', '-1240524'],
                              'zoneType': ['city', 'city']},

                             {'city': 'Edinburgh',
                              'zoneName': ['Livingston, Lothian, United Kingdom', 'Ingliston, Lothian, United Kingdom',
                                           'Dunfermline, Fife, United Kingdom',
                                           'North Berwick, Lothian, United Kingdom',
                                           'Falkirk, Central Scotland, United Kingdom',
                                           "Bo'ness, Central Scotland, United Kingdom",
                                           'Bonnyrigg, Lothian, United Kingdom', 'Kirknewton, Lothian, United Kingdom',
                                           'North Queensferry, Fife, United Kingdom', 'Uphall, Lothian, United Kingdom',
                                           'Edinburgh, Lothian, United Kingdom'],
                              'zoneCode': ['-2601428', '900040254', '-2594879', '-2604220', '-2595891', '-2590378',
                                           '-2590383',
                                           '-2600387', '-2604359', '-2610506', '-2595386'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city']},

                             {'city': 'Fort Lauderdale - Hollywood Area - FL',
                              'zoneName': ['Fort Lauderdale, Florida, USA', 'Dania Beach, Florida, USA',
                                           'Deerfield Beach, Florida, USA',
                                           'Hollywood, Florida, USA', 'Pompano Beach, Florida, USA',
                                           'Miramar, Florida, USA',
                                           'Pembroke Pines, Florida, USA', 'Plantation, Florida, USA',
                                           'Sunrise, Florida, USA',
                                           'Tamarac, Florida, USA', 'Coral Springs, Florida, USA',
                                           'Weston, Florida, USA'],
                              'zoneCode': ['20022339', '20022025', '20022055', '20022659', '20023714', '20023220',
                                           '20023600',
                                           '20023676', '20024205', '20024244', '20021927', '20024505'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city']},

                             {'city': 'Guadalajara & Vicinity',
                              'zoneName': ['Mazamitla, Jalisco, Mexico', 'TepatitlÃ¡n de Morelos, Jalisco, Mexico',
                                           'Ajijic, Jalisco, Mexico', 'Jocotepec, Jalisco, Mexico',
                                           'TeuchitlÃ¡n, Jalisco, Mexico',
                                           'Lagos de Moreno, Jalisco, Mexico', 'La Piedad Cavadas, Michoacan, Mexico',
                                           'San Pedro TesistÃ¡n, Jalisco, Mexico',
                                           'Guadalajara%2C%20Jalisco%2C%20Mexico'],
                              'zoneCode': ['-1682914', '-1705041', '-1650147', '-1672177', '-1705482', '-1674649',
                                           '-1676593',
                                           '-1699888', '-1669612'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Kemer',
                              'zoneName': ['Kemer%2C%20Turkey', 'Mediterranean Region Turkey, Turkey',
                                           'Tekirova, Mediterranean Region Turkey, Turkey',
                                           'Beldibi, Mediterranean Region Turkey, Turkey',
                                           'Mediterranean Region Turkey, Turkey',
                                           'Beldibi, Mediterranean Region Turkey, Turkey',
                                           'Goynuk, Mediterranean Region Turkey, Turkey',
                                           'Tekirova, Mediterranean Region Turkey, Turkey',
                                           'Goynuk, Mediterranean Region Turkey, Turkey'],
                              'zoneCode': ['3887', '1088', '-772862', '-738715', '1088', '-738715', '-750704',
                                           '-772862',
                                           '-750704'],
                              'zoneType': ['region', 'region', 'city', 'city', 'region', 'city', 'city', 'city',
                                           'city']},

                             {'city': 'Marmaris',
                              'zoneName': ['Marmaris%20Area%2C%20Turkey', 'Dalyan, Aegean Region, Turkey',
                                           'Icmeler, Aegean Region, Turkey', 'AkbÃ¼k, Aegean Region, Turkey',
                                           'Akyaka, Aegean Region, Turkey', 'Dalaman, Aegean Region, Turkey',
                                           'Dalyan, Aegean Region, Turkey', 'Fethiye, Aegean Region, Turkey',
                                           'Icmeler, Aegean Region, Turkey', 'Izmir, Aegean Region, Turkey',
                                           'Kas, Mediterranean Region Turkey, Turkey',
                                           'Koycegiz, Aegean Region, Turkey',
                                           'Marmaris, Aegean Region, Turkey', 'Mugla, Aegean Region, Turkey',
                                           'Oludeniz, Aegean Region, Turkey', 'Turunc, Aegean Region, Turkey'],
                              'zoneCode': ['4899', '-744757', '-754030', '-733479', '-734419', '900039811', '-744757',
                                           '-749044',
                                           '-754030', '-755097', '-758319', '-762493', '-764696', '-765549',
                                           '900039659',
                                           '-773925'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Mauritius Islands',
                              'zoneName': ['Mauritius%20Islands', 'Tamarin, Mauritius West Coast, Mauritius',
                                           'Pereybere, Mauritius North Coast, Mauritius',
                                           'Blue Bay, Mauritius South Coast, Mauritius',
                                           'Trou dÊ¼ Eau Douce, Mauritius East Coast, Mauritius',
                                           'Bel Ombre, Mauritius South Coast, Mauritius',
                                           'Tamarin, Mauritius West Coast, Mauritius'],
                              'zoneCode': ['135', '-1355600', '900048665', '900049859', '-1355635', '-1354779',
                                           '-1355600'],
                              'zoneType': ['country', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'New Orleans - LA',
                              'zoneName': ['Westwego, Louisiana, USA',
                                           'New Orleans, Louisiana, United States of America',
                                           'Avondale, Louisiana, USA', 'Gretna, Louisiana, USA',
                                           'Kenner, Louisiana, USA',
                                           'Laplace, Louisiana, USA', 'Marrero, Louisiana, USA',
                                           'Metairie, Louisiana, USA',
                                           'Saint Rose, Louisiana, USA'],
                              'zoneCode': ['20051299', '20050264', '20048277', '20049417', '20049715', '20049810',
                                           '20050034',
                                           '20050105', '20050794'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Tel Aviv',
                              'zoneName': ['Tel%20Aviv%2C%20Center%20District%20Israel%2C%20Israel',
                                           'Ben Gurion Airport, Tel Aviv, Center District Israel, Israel',
                                           'Ramat Gan, Center District Israel, Israel',
                                           'Rechovot, Center District Israel, Israel'],
                              'zoneCode': ['3641', '113', '-781147', '-781147'],
                              'zoneType': ['region', 'airport', 'city', 'city']},

                             {'city': 'Turin',
                              'zoneName': ['Turin%2C%20Piedmont%2C%20Italy', 'Alessandria, Piedmont, Italy',
                                           'Bra, Cuneo, Italy',
                                           'Cesana Torinese, Piedmont, Italy', 'Cuneo, Piedmont, Italy',
                                           'Fossano, Piedmont, Italy',
                                           'Moncalieri, Piedmont, Italy', 'Novara, Piedmont, Italy'],
                              'zoneCode': ['-130938', '-110146', 'ChIJa2jz0Qyr0hIRgrE06nFX4tI', '-115231', '-116669',
                                           '-117899',
                                           '-122041', '-123138'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Golfe de Saint Tropez',
                              'zoneName': ["Aups, Provence-Alpes-Cote d'Azur, France",
                                           "Brignoles, Provence-Alpes-Cote d'Azur, France",
                                           "Draguignan, Provence-Alpes-Cote d'Azur, France",
                                           "Gassin, Provence-Alpes-Cote d'Azur, France",
                                           "Trigance, Provence-Alpes-Cote d'Azur, France",
                                           "La Grande-Motte, Languedoc-Roussillon','Le Lavandou, Provence-Alpes-Cote d'Azur, France",
                                           "Rayol-Canadel-sur-Mer, Provence-Alpes-Cote d'Azur, France",
                                           'Gulf of Saint Tropez, France',
                                           "Plan-de-la-Tour, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Tourtour, Provence-Alpes-CÃ´te d'Azur, France"],
                              'zoneCode': ['-1409244', '-1415280', '-1424504', '-1428807', '-1473801', '-1436408',
                                           '-1441682',
                                           '-1443011', '1581', '-1458557', '-1473306'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'region',
                                           'city',
                                           'city']},

                             {'city': 'Tours',
                              'zoneName': ['Amboise, Centre, France', 'Azay-le-Rideau, Centre',
                                           'Joue-les-Tours, Centre, France',
                                           'Loches, Centre, France', 'Luynes, Centre, France',
                                           'Montbazon, Centre, France',
                                           'Montrichard, Centre, France', 'Richelieu, Centre, France',
                                           'Tours, Centre, France',
                                           'Vouvray, Centre, France', 'Blois, Centre, France'],
                              'zoneCode': ['-1407398', '-1409765', '-1433166', '-1447411', '-1448426', '-1452480',
                                           '-1453379',
                                           '-1461803', '-1473290', '-1477881', '-1413119'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city']},

                             {'city': 'Munich',
                              'zoneName': ['Landshut, Bavaria, Germany', 'Munich, Bavaria, Germany',
                                           'Bad Aibling, Bavaria, Germany',
                                           'Dachau, Bavaria, Germany', 'Eching, Bavaria, Germany',
                                           'Erding, Bavaria, Germany',
                                           'Freising, Bavaria, Germany', 'Haar, Bavaria, Germany',
                                           'Hohenlinden, Bavaria, Germany',
                                           'Neufahrn bei Freising, Bavaria, Germany', 'Puchheim, Bavaria, Germany',
                                           'Schwaig bei MÃ¼nchen, Bavaria, Germany', 'Unterhaching, Bavaria, Germany',
                                           'UnterschleiÃŸheim, Bavaria, Germany', 'Aschheim, Bavaria, Germany'],
                              'zoneCode': ['-181533', '-1829149', '-1743029', '-1757011', '-1762845', '-1766950',
                                           '-1771648', '-1783533',
                                           '-1795131', '-1831496', '-1845143', '-1861562', '-1877587', '-1878286',
                                           '-1741418'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city']},

                             {'city': 'Budapest',
                              'zoneName': ['Budapest%2C%20Pest%2C%20Hungary',
                                           '06. TerÃ©zvÃ¡ros, Budapest, Pest, Hungary',
                                           '08. JÃ³zsefvÃ¡ros, Budapest, Pest, Hungary',
                                           '07. ErzsÃ©betvÃ¡ros, Budapest, Pest, Hungary',
                                           '13. AngyalfÃ¶ld - ÃšjlipÃ³tvÃ¡ros, Budapest, Pest, Hungary',
                                           '05. BelvÃ¡ros - LipÃ³tvÃ¡ros, Budapest, Pest, Hungary',
                                           '09. FerencvÃ¡ros, Budapest, Pest, Hungary', 'BudaÃ¶rs, Pest, Hungary',
                                           'HÃ©vÃ­z, Zala, Hungary', 'SiÃ³fok, Somogy, Hungary'],
                              'zoneCode': ['-850553', '1249', '1251', '1250', '1256', '1248', '1252', '-850550',
                                           '-855735',
                                           '-866124'],
                              'zoneType': ['city', 'district', 'district', 'district', 'district', 'district',
                                           'district',
                                           'city',
                                           'city', 'city']},

                             {'city': 'Barcelona',
                              'zoneName': ['Barcelona%2C%20Catalonia%2C%20Spain',
                                           'Downtown Barcelona, Barcelona, Catalonia, Spain',
                                           'Gothic Quarter, Barcelona, Catalonia, Spain'],
                              'zoneCode': ['745', '2287', '1288'],
                              'zoneType': ['region', 'district', 'district']},

                             {'city': 'Verona',
                              'zoneName': [' Caldiero%2C%20V%C3%A9neto%2C%20Italia',
                                           ' Castel%20d%27Azzano%2C%20V%C3%A9neto%2C%20Italia',
                                           ' Grezzana%2C%20Grezzana%2C%20V%C3%A9neto%2C%20Italia',
                                           ' San%20Bonifacio%2C%20V%C3%A9neto%2C%20Italia',
                                           ' Verona%2C%20V%C3%A9neto%2C%20Italia',
                                           'Grezzana, Veneto, Italy', 'San Martino Buon Albergo, Veneto, Italy'],
                              'zoneCode': ['', '900039823', '900052264', '-118882', '-127327', '-132092', '-11888',
                                           '-127907'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Valencia',
                              'zoneName': [' Requena, Valencia Community, Spain',
                                           ' Valencia, Valencia Community, Spain',
                                           ' BÃ©tera, Valencia Community, Spain', ' Alaquas, Valencia Community, Spain',
                                           ' Alfafar, Valencia Community, Spain', ' Paterna, Valencia Community, Spain',
                                           ' Torrent, Valencia Community, Spain',
                                           ' Almussafes, Valencia Community, Spain',
                                           ' BenetÃºser, Valencia Community, Spain',
                                           ' El Puig, Valencia Community, Spain',
                                           ' Utiel, Valencia Community, Spain', ' Alboraya, Valencia Community, Spain',
                                           ' Aldaia, Valencia Community, Spain', ' Cheste, Valencia Community, Spain',
                                           ' Bocairent, Valencia Community, Spain',
                                           ' Puerto de Sagunto, Valencia Community, Spain',
                                           ' Burjassot, Comunitat Valenciana, Espanya',
                                           ' BenisanÃ³, Valencia Community, Spain',
                                           ' Picanya, Valencia Community, Spain',
                                           ' Massalfassar, Comunitat Valenciana, Espanya',
                                           ' Manises, Valencia Community, Spain', ' Costa%20de%20Valencia%2C%20Spain',
                                           ' Valencia%20Community%2C%20Spain', 'Quart de Poblet, Valencia, Spain'],
                              'zoneCode': ['-398847', '-406131', '-373552', '-369516', '-370091', '-395665', '-404769',
                                           '-370439',
                                           '-373203', '-397907', '-405593', '-369721', '900048423', '-377923',
                                           '-373759',
                                           '-381099',
                                           '-374428', '-373267', '-396471', '-391324', '-390953', '1391', '1523',
                                           'ChIJQRm8zP5PYA0RYQoAHo0WYqQ'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'region',
                                           'region', 'region']},

                             {'city': 'Brisbane - QLD',
                              'zoneName': ['Brisbane, Queensland, Australia', 'Ipswich, Queensland, Australia',
                                           'Redcliffe, Queensland, Australia', 'Moreton Island,Australia',
                                           'Caboolture%2C%20Queensland%2C%20Australia',
                                           'Loganlea%2C%20Queensland%2C%20Australia',
                                           'Toowoomba%2C%20Queensland%2C%20Australia',
                                           'Scarborough, Queensland, Australia'],
                              'zoneCode': ['-1561728', '-1579571', '-1597026', '3693', '-1563472', '-1584290',
                                           '-1605321',
                                           '333697'],
                              'zoneType': ['city', 'city', 'city', 'region', 'city', 'city', 'city', 'city']},

                             {'city': 'Cantabria',
                              'zoneName': ['Cantabria%2C%20Spain', 'Arenas%20de%20Igu%C3%B1a%2C%20Cantabria%2C%20Spain',
                                           'Igollo%2C%20Cantabria%2C%20Spain', 'Novales%2C%20Cantabria%2C%20Spain',
                                           'Reinosa%2C%20Cantabria%2C%20Spain', 'Udias%2C%20Cantabria%2C%20Spain',
                                           'Valle%2C%20Cantabria%2C%20Spain'],
                              'zoneCode': ['731', '-371247', '-385770', '-394173', '-398734', '900049568', '-406246'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Thessaloniki',
                              'zoneName': ['Thessalon%C3%ADki%2C%20Macedonia%2C%20Greece',
                                           'Agia Triada, Macedonia, Greece',
                                           'Anchialos, Macedonia, Greece', 'Perea, Macedonia, Greece'],
                              'zoneCode': ['-829252', '-815181', '-814101', '-825880'],
                              'zoneType': ['city', 'city', 'city', 'city']},

                             {'city': 'Istanbul',
                              'zoneName': ['Fatih, Istanbul, Marmara Region, Turkey',
                                           'Buyukcekmece, Marmara Region, Turkey',
                                           'Kumburgaz, Marmara Region, Turkey', 'Beylikduzu, Marmara Region, Turkey',
                                           'Tuzla, Marmara Region, Turkey', 'Basaksehir, Marmara Region, Turkey',
                                           'Esenyurt, Marmara Region, Turkey',
                                           'Aksaray, Istanbul, Marmara Region, Turkey',
                                           'Old city Sultanahmet, Istanbul, Marmara Region, Turkey',
                                           'Taksim, Istanbul, Marmara Region, Turkey',
                                           'Beyoglu, Istanbul, Marmara Region, Turkey',
                                           'Sisli, Istanbul, Marmara Region, Turkey',
                                           'Asian Side, Istanbul, Marmara Region, Turkey',
                                           'Laleli, Istanbul, Marmara Region, Turkey',
                                           'Beyazit, Istanbul, Marmara Region, Turkey',
                                           'Sirkeci, Istanbul, Marmara Region, Turkey',
                                           'Besiktas, Istanbul, Marmara Region, Turkey',
                                           'Kadikoy, Istanbul, Marmara Region, Turkey',
                                           'Istanbul, Marmara Region, Turkey',
                                           'Downtown Istanbul, Istanbul, Marmara Region, Turkey'],
                              'zoneCode': ['4511', '-740638', '-763225', '900050863', '-774022', '900052777', '-748518',
                                           '6227', '1045',
                                           '1053', '4310', '1416', '2107', '2525', '1419', '2493', '1158', '1134',
                                           '-755070', '4308'],
                              'zoneType': ['district', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'district',
                                           'district',
                                           'district', 'district', 'district', 'district', 'district', 'district',
                                           'district',
                                           'district', 'city', 'district']},

                             {'city': 'Krakow',
                              'zoneName': ['Bochnia%2C%20Lesser%20Poland%2C%20Poland',
                                           'KrakÃ³w%2C+Lesser+Poland%2C+Poland',
                                           'Modlnica%2C+Lesser+Poland%2C+Poland',
                                           'Modlniczka%2C+Lesser+Poland%2C+Poland',
                                           'Wieliczka%2C+Lesser+Poland%2C+Poland', 'Krak%C3%B3w+-+Balice',
                                           'Modlniczka, Lesser Poland, Poland', 'Modlnica, Poland'],
                              'zoneCode': ['-494208', '-510625', '-517054', '-517055', '-534981', '843', '-517055',
                                           '-517054'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'airport']},

                             {'city': 'Zante',
                              'zoneName': ['Zakynthos%2C%20Greece', 'KipsÃ©li, Ionian Islands, Greece',
                                           'Laganas, Ionian Islands, Greece'],
                              'zoneCode': ['1663', '-820615', '900039486'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Miami Area - FL',
                              'zoneName': ['Miami Beach, Florida, USA', 'Miami, Florida, USA',
                                           'Florida city, Florida, USA',
                                           'Aventura mall, Aventura, Florida, USA', 'Miami Lakes, Florida, USA',
                                           'North Miami, Florida, USA'],
                              'zoneCode': ['20023182', '20023181', '20022300', '13121', '20023184', '20023366'],
                              'zoneType': ['city', 'city', 'city', 'landmark', 'city', 'city']},

                             {'city': 'Helsinki',
                              'zoneName': ['Vantaa Airport, Helsinki, EtelÃ¤-Suomen, Finland',
                                           'JÃ¤rvenpÃ¤Ã¤, Southern Finland, Finland'],
                              'zoneCode': ['94', '-1367278'],
                              'zoneType': ['airport', 'city']},

                             {'city': 'Marseille',
                              'zoneName': ["Saint-Cyr-sur-Mer, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Aubagne, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Cassis, Provence-Alpes-CÃ´te d'Azur, France",
                                           "La Ciotat, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Les-Pennes-Mirabeau, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Marseille, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Vitrolles, Provence-Alpes-CÃ´te d'Azur, France"],
                              'zoneCode': ['-1464530', '-1408878', '-1416912', '-1435362', '-1445354', '-1449947',
                                           '-1477622'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Naples',
                              'zoneName': ['Portici, Campania, Italy', 'Torre del Greco, Campania, Italy',
                                           'Naples%2C%20Campania%2C%20Italy', 'Chiaia, Naples, Campania, Italy',
                                           'Naples Historic Center, Naples, Campania, Italy',
                                           'Central Station, Naples, Campania, Italy',
                                           'Port of Naples, Naples, Campania, Italy',
                                           'Plebiscito, Naples, Campania, Italy'],
                              'zoneCode': ['-125511', '-131012', '898', '1292', '1291', '1295', '2243', '1296'],
                              'zoneType': ['city', 'city', 'region', 'district', 'district', 'district', 'district',
                                           'district']},

                             {'city': 'Nice',
                              'zoneName': ["Cagnes-sur-Mer, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Nice, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Beaulieu-sur-Mer, Provence-Alpes-CÃ´te d'Azur, France",
                                           "La Colle-sur-Loup, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Saint-Paul-de-Vence, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Saint-Laurent-du-Var, Provence-Alpes-CÃ´te d'Azur, France",
                                           "Vence, Provence-Alpes-CÃ´te d'Azur, France','Saint-Jean-Cap-Ferrat, France"],
                              'zoneCode': ['-1416112', '-1454990', '-1411081', '-1435409', '-1467763', '-1466573',
                                           '-1475342',
                                           '-1466094'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'London',
                              'zoneName': ['Basildon, Essex, United Kingdom', 'Bexley, Greater London, United Kingdom',
                                           'Brentford, Greater London, United Kingdom',
                                           'Bromley, Greater London, United Kingdom',
                                           'Chigwell, Essex, United Kingdom',
                                           'Chislehurst, Greater London, United Kingdom',
                                           'Croydon, Greater London, United Kingdom',
                                           'Enfield, Greater London, United Kingdom',
                                           'Ilford, Greater London, United Kingdom',
                                           'Kingston upon Thames, Greater London, United Kingdom',
                                           'London, Greater London, United Kingdom',
                                           'Richmond upon Thames, Greater London, United Kingdom',
                                           'Sutton, Greater London, United Kingdom',
                                           'Twickenham, Greater London, United Kingdom',
                                           'Heathrow, Greater London, United Kingdom',
                                           'Bethnal Green, Greater London, United Kingdom',
                                           'London Luton Airport, London, Greater London, United Kingdom',
                                           'Potters Bar, Hertfordshire, United Kingdom',
                                           'Soho, London, Greater London, United Kingdom',
                                           'Southwark, London, Greater London, United Kingdom',
                                           'London Stansted Airport, London, Greater London, United Kingdom',
                                           'Watford, Hertfordshire, United Kingdom',
                                           'Woolwich, London, Greater London, United Kingdom'],
                              'zoneCode': ['-2589397', '-2589817', '-2590807', '-2591010', '-2592428', '-2592483',
                                           '-2593790',
                                           '-2595615', '-2599348', '-2600204', '-2601889', '-2606258', '-2609149',
                                           '-2610350',
                                           '-2598406', '-2589789', '137', '-2605672', '39', '122', '75', '-2610992',
                                           '144'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'airport', 'city', 'district',
                                           'district', 'airport',
                                           'city', 'district']},

                             {'city': 'Lucerne',
                              'zoneName': ['Nottwil, Canton of Lucerne, Switzerland',
                                           'Rothenburg, Canton of Lucerne, Switzerland'],
                              'zoneCode': ['-2553379', '-2553868'],
                              'zoneType': ['city', 'city']},

                             {'city': 'Centre Portugal',
                              'zoneName': ['Lisbon%20city%20Centre%2C%20Lisbon%2C%20Lisbon%20Region%2C%20Portugal',
                                           'Arouca%2C%20Norte%20Region%2C%20Portugal',
                                           'Caldas%20de%20Aregos%2C%20Norte%20Region%2C%20Portugal',
                                           'Cartaxo%2C%20Ribatejo%2C%20Portugal',
                                           'Esmoriz%2C%20Norte%20Region%2C%20Portugal',
                                           'Vagos%2C%20Centro%20Region%2C%20Portugal',
                                           'Vale%20de%20Cambra%2C%20Norte%20Region%2C%20Portugal',
                                           'Vieira%20de%20Leiria%2C%20Centro%20Region%2C%20Portugal',
                                           'Vila%20Pouca%20da%20Beira%2C%20Centro%20Region%2C%20Portugal'],
                              'zoneCode': ['3992', '-2158704', '-2160807', '-2161631', '-2164686', '-2178050',
                                           '-2178386',
                                           '-2179360',
                                           '-2179659'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Montpellier',
                              'zoneName': ['Aigues-Mortes, Languedoc-Roussillon, France',
                                           'La Grande-Motte, Languedoc-Roussillon, France',
                                           'Saint-ClÃ©ment-de-RiviÃ¨re, Languedoc-Roussillon, France',
                                           'Vias, Languedoc-Roussillon, France',
                                           "Cap d'Agde, Languedoc-Roussillon, France','Castries, Languedoc-Roussillon, France",
                                           'Fabregues, Languedoc-Roussillon, France',
                                           'Frontignan, Languedoc-Roussillon, France',
                                           'Mauguio, Languedoc-Roussillon, France',
                                           'Montpellier, Languedoc-Roussillon, France',
                                           'Port-Camargue, Languedoc-Roussillon, France',
                                           'Saint-Jean-de-VÃ©das, Languedoc-Roussillon, France',
                                           'Sete, Languedoc-Roussillon, France'],
                              'zoneCode': ['-1406800', '-1436408', '-1464390', '-1476069', '-1440527', '-1417085',
                                           '-1426201',
                                           '-1428412', '-1450295', '-1453260', '900049677', '-1466202', '-1470743'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city']},

                             {'city': 'Chicago - IL',
                              'zoneName': ['Chicago%2C%20Illinois%2C%20USA', 'Burr%20Ridge%2C%20Illinois%2C%20USA',
                                           'Lake%20Bluff%2C%20Illinois%2C%20USA'],
                              'zoneCode': ['2443', '20033016', '20034458'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'FLORENCE',
                              'zoneName': ['Florence%2C%20Tuscany%2C%20Italy', 'Tuscany%2C+Italy',
                                           'Bagno a Ripoli, Tuscany, Italy',
                                           'Signa, Tuscany, Italy',
                                           'Florence Historic Center, Florence, Tuscany, Italy',
                                           'San Lorenzo, Florence, Tuscany, Italy',
                                           'Fortezza da Basso, Florence, Tuscany, Italy',
                                           'Uffizi, Florence, Tuscany, Italy'],
                              'zoneCode': ['-117543', '910', '-111064', '-129717', '691', '2055', '2052', '2050'],
                              'zoneType': ['city', 'region', 'city', 'city', 'district', 'district', 'district',
                                           'district']},

                             {'city': 'Gdansk',
                              'zoneName': ['Gdansk, Pomerania, Poland', 'Gdynia, Pomerania, Poland',
                                           'Sopot, Pomerania, Poland',
                                           'Jurata, Pomerania, Poland', 'Gdansk Sobieszewo, Poland'],
                              'zoneCode': ['-501400', '-501414', '-529430', '-506164', '-529173'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city']},

                             {'city': 'Lyon',
                              'zoneName': ['AmbÃ©rieu-en-Bugey, RhÃ´ne-Alpes, France',
                                           'Bourg-en-Bresse, RhÃ´ne-Alpes, France',
                                           'Bourgoin-Jallieu, RhÃ´ne-Alpes, France', 'Bron, RhÃ´ne-Alpes, France',
                                           'Chanas, RhÃ´ne-Alpes, France', 'Chaponnay, RhÃ´ne-Alpes, France',
                                           'CharbonniÃ¨res-les-Bains, RhÃ´ne-Alpes, France',
                                           'Chasse-sur-RhÃ´ne, RhÃ´ne-Alpes, France',
                                           "Chonas-l'Amballan, RhÃ´ne-Alpes, Fr",
                                           "Collonges-au-Mont-d'Or, RhÃ´ne-Alpes, France",
                                           'Condrieu, RhÃ´ne-Alpes, France', 'Dardilly, RhÃ´ne-Alpes, France',
                                           'Ã‰cully, RhÃ´ne-Alpes, France', 'Givors, RhÃ´ne-Alpes, France',
                                           'La Tour-de-Salvagny, RhÃ´ne-Alpes, France',
                                           "L'Isle-d'Abeau, RhÃ´ne-Alpes, France",
                                           'Lyon, RhÃ´ne-Alpes, France', 'Massieux, RhÃ´ne-Alpes, France',
                                           'Moissieu-sur-Dolon, RhÃ´ne-Alpes, France',
                                           "Saint-Cyr-au-Mont-d'Or, RhÃ´ne-Alpes, France",
                                           'Sainte-Foy-lÃ¨s-Lyon, RhÃ´ne-Alpes, France',
                                           'Saint-Laurent-de-Mure, RhÃ´ne-Alpes, France',
                                           'Saint-Priest, RhÃ´ne-Alpes, France', 'Saint-Vulbas, RhÃ´ne-Alpes, France',
                                           'Sathonay-Camp, RhÃ´ne-Alpes, France',
                                           'Tassin-la-Demi-Lune, RhÃ´ne-Alpes, France',
                                           'Villefontaine, RhÃ´ne-Alpes, France',
                                           'Villefranche-sur-SaÃ´ne, RhÃ´ne-Alpes, France',
                                           'Villeurbanne, RhÃ´ne-Alpes, France', 'Vonnas, RhÃ´ne-Alpes, France',
                                           'Lyon - Saint Exupery Airport, Lyon, RhÃ´ne-Alps, France',
                                           'Oullins, RhÃ´ne-Alps, France',
                                           'Chaponnay, RhÃ´ne-Alps, France', 'Chasse-sur-RhÃ´ne, RhÃ´ne-Alps, France',
                                           'Saint-Cyr-au-Mont-dÊ¼Or, RhÃ´ne-Alps, France',
                                           'Saint-Laurent-de-Mure, RhÃ´ne-Alps, France',
                                           'Vonnas, RhÃ´ne-Alps, France'],
                              'zoneCode': ['-1407356', '-1414325', '-1414375', '-1415406', '-1418363', '-1418588',
                                           '-1418646',
                                           '-1418962', '-1420304', '-1421041', '-1421409', '-1423622', '-1424962',
                                           '-1429468',
                                           '-1439185', '-1447271', '-1448468', '-1450190', '-1451846', '-1464499',
                                           '-1464877',
                                           '-1466543', '-1468109', '-1468904', '-1469573', '-1472163', '-1476721',
                                           '-1476744', '900'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city']},

                             {'city': 'Malaga',
                              'zoneName': ['M%C3%A1laga%2C%20Andaluc%C3%ADa%2C%20Spain', 'CÃ³mpeta, AndalucÃ­a, Spain',
                                           'GaucÃ­n, AndalucÃ­a, Spain', 'Tolox, AndalucÃ­a, Spain',
                                           'VÃ©lez-MÃ¡laga, AndalucÃ­a, Spain'],
                              'zoneCode': ['766', '-378570', '-383849', '-404380', '-406825'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city']},

                             {'city': 'Manchester',
                              'zoneName': ['Manchester%2C%20Greater%20Manchester%2C%20United%20Kingdom',
                                           'Burnley, Lancashire, United Kingdom',
                                           'Densham Deborah, Forest Drive, Sale, United Kingdom'],
                              'zoneCode': ['-2602512', '-2591335', 'ChIJLe7RUmCse0gRv5HfCQVEglc'],
                              'zoneType': ['city', 'city', 'landmark']},

                             {'city': 'Orlando Area - Florida - FL',
                              'zoneName': ['Orlando, Florida, USA', 'Altamonte Springs, Florida, USA',
                                           'Apopka, Florida, USA',
                                           'Kissimmee, Florida, USA', 'Davenport, Florida, USA',
                                           'Lake Mary, Florida, USA',
                                           'Lake Mary, Florida, USA', 'River Ranch, Florida, USA',
                                           'Buena Ventura Lakes, FL, United States', 'Citrus Ridge, Florida, USA',
                                           'Four Corners, Florida, USA', 'Howey in the Hills, Florida, USA',
                                           'Ocoee, Florida, USA'],
                              'zoneCode': ['20023488', '20021339', '20021367', '20022851', '20022031', '20022910',
                                           '20023956',
                                           '900051829', 'ChIJXVFvsTyG3YgRtEi4uciYzpY', '900040365', '20022365',
                                           '20022687',
                                           '20023438'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city']},

                             {'city': 'Los Angeles - CA',
                              'zoneName': ['Disneyland California', 'Huntington Beach', 'Long Beach', 'Newport Beach',
                                           'Santa Clarita',
                                           'Woodland Hills', 'LOS ANGELES', 'Burbank, California, USA',
                                           'Dana Point, California, USA',
                                           'Diamond Bar, California, USA', 'El Monte, California, USA',
                                           'Fillmore, California, USA',
                                           'Glendale, California, USA', 'Harbor city, California, USA',
                                           'Hawthorne, California, USA',
                                           'Hermosa Beach, California, USA', 'Inglewood, California, USA',
                                           'La Puente, California, USA',
                                           'Laguna Hills, California, USA', 'Manhattan Beach, California, USA',
                                           'Murrieta, California, USA', 'Oxnard, California, USA',
                                           'Pico Rivera, California, USA',
                                           'Redondo Beach, California, USA', 'San Clemente, California, USA',
                                           'San Dimas, California, USA', 'Signal Hill, California, USA',
                                           'Simi Valley, California, USA',
                                           'Thousand Oaks, California, USA', 'Torrance, California, USA',
                                           'Van Nuys, California, USA',
                                           'West Covina, California, USA'],
                              'zoneCode': ['3731', '20013595', '20014160', '20014760', '20015796', '20016922',
                                           '20014181',
                                           '20011868',
                                           '20012464', '20012588', '20012775', '20012950', '20013171', '20013363',
                                           '900040177',
                                           '20013450', '20013651', '20013904', '20013924', '20014271', '20014685',
                                           '20015025',
                                           '20015190', '20015479', '20015724', '20015727', '20015984', '20015993',
                                           '20016410',
                                           '20016461', '20016606', '20016765'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city']},

                             {'city': 'Milan',
                              'zoneName': ['Abbiategrasso, ?Lombardy, ?Italy', 'Assago, ?Lombardy, ?Italy',
                                           'Basiglio, ?Lombardy, ?Italy', 'Bollate, ?Lombardy, ?Italy',
                                           'Busto Arsizio, ?Lombardy, ?Italy', 'Cambiago, ?Lombardy, ?Italy',
                                           'Cavenago di Brianza, ?Lombardy, ?Italy',
                                           'Cesano Maderno, ?Lombardy, ?Italy',
                                           'Cinisello Balsamo, ?Lombardy, ?Italy', 'Cologno Monzese, ?Lombardy, ?Italy',
                                           'Cusago, Lombardy, Italy', 'Gerenzano, Lombardy, Italy',
                                           'Legnano, Lombardy, Italy',
                                           'Limbiate, Lombardy, Italy', 'Lomazzo, Lombardy, Italy',
                                           'Mediglia, Lombardy, Italy',
                                           'Monza, Lombardy, Italy', 'Mozzate, Lombardy, Italy',
                                           'Ornago, Lombardy, Italy',
                                           'Ospedaletto Lodigiano, Lombardy, Italy', 'Pero, Lombardy, Italy',
                                           'Pieve Emanuele, Lombardy, Italy', 'Pregnana Milanese, Lombardy, Italy',
                                           'Saronno, Lombardy, Italy', 'Sesto San Giovanni, Lombardy, Italy',
                                           'Trezzano sul Naviglio, Lombardy, Italy',
                                           "Trezzo sull'Adda, Lombardy, Italy",
                                           'Milan%2C+Lombardy%2C+Italy', 'Milan city Center, Milan, Lombardia, Italy',
                                           'Milan Central Station, Milan, Lombardy, Italy',
                                           'CittÃ  Studi, Milan, Lombardy, Italy',
                                           'Navigli, Milan, Lombardy, Italy'],
                              'zoneCode': ['-109825', '900039151', '900048648', '-111739', '-112376', '-112662',
                                           '-114896',
                                           '-115235',
                                           '-115568', '-115989', '900039347', '900039688', '-119953', '-120184',
                                           '-120302',
                                           '900049762',
                                           '-122630', '-122785', '-123424', '900039390', '900040489', '900048692',
                                           '900040152',
                                           '-129028', '-129634', '-131331', '-131332', '-121726', '2303', '1183',
                                           '779'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'district', 'landmark',
                                           'district',
                                           'district']},

                             {'city': 'Mykonos',
                              'zoneName': ['Ftelia, Cyclades, Greece', 'Mykonos%2C%20Greece'],
                              'zoneCode': ['900040874', '2813'],
                              'zoneType': ['city', 'region']},

                             {'city': 'Malta',
                              'zoneName': ['Comino, Malta', 'Gozo, Malta', 'Lija, Malta, Malta',
                                           'Malta International Airport, Luqa, Malta', 'Msida, Malta, Malta',
                                           'Qawra, Malta, Malta',
                                           'Malta%2C%20Malta'],
                              'zoneCode': ['900050204', '981', '-18800', 'ChIJbUqwUoVaDhMRSnid2CRmag0', '-18907',
                                           '900039073', '3939'],
                              'zoneType': ['city', 'region', 'city', 'airport', 'city', 'city', 'region']},

                             {'city': 'Melbourne - VIC',
                              'zoneName': ['Dandenong Ranges, Australia', 'Fawkner, Victoria, Australia',
                                           'Melton, Victoria, Australia',
                                           'Victoria, Australia'],
                              'zoneCode': ['4986', '-1573057', '-1586889', '617'],
                              'zoneType': ['region', 'city', 'city', 'region']},

                             {'city': 'Metro Manila',
                              'zoneName': ['Ermita, Manila, Luzon, Philippines', 'Manila%2C+Luzon%2C+Philippines',
                                           'Metro Manila, Philippines', 'Cagraray, Luzon, Philippines',
                                           'Santa Rosa, Luzon, Philippines',
                                           'Boracay, Visayas, Philippines', 'San Mateo, Luzon, Philippines'],
                              'zoneCode': ['8110', '-2437894', '5258', '-2418412', '-2451779', '-2436593', '-2450613'],
                              'zoneType': ['district', 'city', 'region', 'city', 'city', 'city', 'city']},

                             {'city': 'Newcastle-upon-Tyne',
                              'zoneName': ['Consett, Durham, United Kingdom', 'Hexham, Northumberland, United Kingdom',
                                           'Longhorsley, Northumberland, United Kingdom',
                                           'South Shields, Tyne and Wear, United Kingdom',
                                           'Sunderland, Tyne and Wear, United Kingdom', 'Tyne and Wear, United Kingdom',
                                           'Northumberland, United Kingdom'],
                              'zoneCode': ['-2593170', '-2598615', '-2601956', '-2608323', '-2609121', '3155', '1115'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'region', 'region']},

                             {'city': 'Rimini',
                              'zoneName': ['Emilia-Romagna%2C%20Italy', 'Marche%2C%20Italy',
                                           'Gatteo a Mare, Emilia-Romagna, Italy',
                                           'Lido di Savio, Emilia-Romagna, Italy',
                                           'Montegridolfo, Emilia-Romagna, Italy',
                                           'Rivazzurra, Rimini, Emilia-Romagna, Italia'],
                              'zoneCode': ['899', '905', '93565', '-120155', '900039878', '1657'],
                              'zoneType': ['region', 'region', 'city', 'city', 'city', 'district']},

                             {'city': 'Rome',
                              'zoneName': ['Rome%2C+Lazio%2C+Italy&ssne=Ile+de+R%C3%A9%2C+France',
                                           'Fiumicino%2BAirport%252C%2BRome%252C%2BLazio%252C%2BItaly',
                                           'Anzio, Lazio, Italy',
                                           'Ariccia, Lazio, Italy', 'Bracciano, Lazio, Italy',
                                           'Fiano Romano, Lazio, Italy',
                                           'Fiuggi, Lazio, Italy', 'Frascati, Lazio, Italy', 'Fregene, Lazio, Italy',
                                           'Grottaferrata, Lazio, Italy', 'Pomezia, Lazio, Italy',
                                           'Rieti, Lazio, Italy',
                                           'Sacrofano, Lazio, Italy', 'Valmontone, Lazio, Italy',
                                           'Viterbo, Lazio, Italy'],
                              'zoneCode': ['-126693', '29', '-110494', '-110670', '-112072', '-117438', '-117559',
                                           '-117961', '-118012',
                                           '-118945', '-125268', '-126320', '-127067', '-131820', '-132645'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city']},

                             {'city': 'Siena',
                              'zoneName': ['Siena+Area%2C+Italy', 'Siena%2C%20Tuscany%2C%20Italy',
                                           "Casole d'Elsa, Tuscany, Italy",
                                           'Gaiole in Chianti, Tuscany, Italy', 'Gambassi Terme, Tuscany, Italy',
                                           'Montaione, Tuscany, Italy', 'Montefiridolfi, Tuscany, Italy',
                                           'Roccastrada, Tuscany, Italy',
                                           'Tavarnelle in Val di Pesa, Tuscany, Italy'],
                              'zoneCode': ['4094', '-129709', '-114278', '-118164', '-118260', '-122134', '900039433',
                                           '-126625',
                                           '-130532'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Ho Chi Minh city (Saigon) and South',
                              'zoneName': ['Chau Doc, An Giang, Vietnam', 'Con Dao, Vietnam',
                                           'Ho Chi Minh Municipality, Vietnam',
                                           'Phu Quoc Island, Vietnam', 'Ba Ria - Vung Tau, Vietnam',
                                           'Binh Thuan, Vietnam',
                                           'Can Tho Municipality, Vietnam', 'Can Tho, Can Tho Municipality, Vietnam',
                                           'Phu Quoc, Kien Giang , Vietnam'],
                              'zoneCode': ['-3710453', '-3711308', '6229', '5891', '6233', '5391', '6230', '-3709910',
                                           '-3726177'],
                              'zoneType': ['city', 'city', 'region', 'region', 'region', 'region', 'region', 'city',
                                           'city']},

                             {'city': 'Sicily',
                              'zoneName': ['Sicily%2C%20Italy', 'Enna, Sicily, Italy'],
                              'zoneCode': ['909', '-117041'],
                              'zoneType': ['region', 'city']},

                             {'city': 'Skiathos',
                              'zoneName': ['Vassilias, Skiathos, Greece', 'Skiathos%2C%20Greece'],
                              'zoneCode': ['900039637', '2891'],
                              'zoneType': ['city', 'region']},

                             {'city': 'Sofia',
                              'zoneName': ['Bankya, Sofia, Bulgaria', 'Pravets, Sofia, Bulgaria',
                                           'Sofia%2C%20Sofia%2C%20Bulgaria'],
                              'zoneCode': ['-831971', '-837480', '-838489'],
                              'zoneType': ['city', 'city', 'city']},

                             {'city': 'Split-Middle Dalmatia',
                              'zoneName': ['Okrug Gornji, Split-Dalmatia County, Croatia', 'Vis Island, Croatia',
                                           'Podstrana',
                                           'Obonjan Island, Sibenik-Knin County, Croatia',
                                           'PrimoÅ¡ten, Sibenik-Knin County, Croatia',
                                           'Tisno, Sibenik-Knin County, Croatia',
                                           'Vranjic, Split-Dalmatia County, Croatia',
                                           'Split-Dalmatia%20County%2C%20Croatia', 'Brodarica, Croatia',
                                           'Lozovac, Croatia',
                                           'Makarska, Croatia', 'Novalja, Croatia', 'Postira, Croatia',
                                           'Rogoznica, Croatia',
                                           'Å ibenik, Croatia', 'Skradin, Croatia', 'Split, Croatia',
                                           'Stari Grad, Croatia',
                                           'Tisno, Croatia', 'Trogir, Croatia', 'Vodice, Croatia',
                                           'Split city Center, Split, Splitsko-Dalmatinska Å¾upanija, Croatia',
                                           'Znjan, Split, Split-Dalmatia County, Croatia',
                                           'Bacvice, Split, Split-Dalmatia County, Croatia',
                                           'Split Old Town, Split, Split-Dalmatia County, Croatia'],
                              'zoneCode': ['-81736', '2904', '-92454', '900056079', '-93222', '-98226', '-102742',
                                           '4850',
                                           '77533',
                                           '-87588', '-87968', '-90224', '-92805', '-94539', '-95501', '-95863',
                                           '-96492',
                                           '-96909',
                                           '98226', '-98777', '-100686', '8048', '8053', '8052', '6898'],
                              'zoneType': ['city', 'region', 'city', 'city', 'city', 'city', 'city', 'region', 'city',
                                           'city', 'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'district',
                                           'district', 'district', 'district']},

                             {'city': 'Stockholm',
                              'zoneName': ['Stockholm%2C%20Stockholm%20county%2C%20Sweden',
                                           'Bromma, Stockholm county, Sweden',
                                           'HÃ¤gersten, Stockholm county, Sweden', 'Kista, Stockholm county, Sweden',
                                           'Arlanda Airport, Stockholm, Stockholm county, Sweden'],
                              'zoneCode': ['-2524279', '-2475051', '900040987', '-2494669', '55'],
                              'zoneType': ['city', 'city', 'city', 'city', 'airport']},

                             {'city': 'Seville',
                              'zoneName': ['Seville%20Andaluc%20Spain', 'AlcalÃ¡ de Guadaira, AndalucÃ­a, Spain',
                                           'AznalcÃ¡zar, AndalucÃ­a, Spain', 'Camas, AndalucÃ­a, Spain',
                                           'Castilleja de la Cuesta, AndalucÃ­a, Spain',
                                           'Dos Hermanas, AndalucÃ­a, Spain',
                                           'Ã‰cija, AndalucÃ­a, Spain', 'Osuna, AndalucÃ­a, Spain',
                                           'Torre de la Reina, AndalucÃ­a, Spain', 'Villamanrique de la Condesa'],
                              'zoneCode': ['-402849', '-369775', '-372066', '-375208', '-377038', '-380027', '-380128',
                                           '-394848',
                                           '900039990', '-407797'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city']},

                             {'city': 'Strasbourg',
                              'zoneName': ['Strasbourg%2C%20Alsace%2C%20France', 'Barr, Alsace, France',
                                           'Marlenheim, Alsace, France'],
                              'zoneCode': ['788', '-1410448', '-1449743'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Sydney - NSW',
                              'zoneName': ['New South Wales, Australia', 'Chullora, New South Wales, Australia',
                                           'Collaroy, New South Wales, Australia',
                                           'Blacktown, New South Wales, Australia'],
                              'zoneCode': ['612', '-1565625', '-1566380', '-1559713'],
                              'zoneType': ['region', 'city', 'city', 'city']},

                             {'city': 'Austrian Alps',
                              'zoneName': ['Austrian%20Alps%2C%20Austria', 'Mieming%2C+Tyrol%2C+Austria',
                                           'Nauders%2C+Tyrol%2C+Austria',
                                           'Niederau%2C+Tyrol%2C+Austria', 'Obergurgl%2C+Tyrol%2C+Austria',
                                           'Oberndorf%2C+Tyrol%2C+Austria', 'Pertisau%2C+Tyrol%2C+Austria',
                                           'Rennweg%2C+Carinthia%2C+Austria', 'Sankt+Lambrecht%2C+Styria%2C+Austria',
                                           'S%C3%B6lden%2C+Tyrol%2C+Austria', 'S%C3%B6ll%2C+Tyrol%2C+Austria',
                                           'Spiss%2C+Tyrol%2C+Austria', 'Sankt+Ulrich+am+Pillersee%2C+Tyrol%2C+Austria',
                                           'Sankt+Urban%2C+Carinthia%2C+Austria',
                                           'Sankt+Michael+im+Lungau%2C+Salzburg%2C+Austria',
                                           'Vent%2C+Tyrol%2C+Austria', 'Bruck%2C+Salzburg%2C+Austria',
                                           'Eben+im+Pongau%2C+Salzburg%2C+Austria', 'Fieberbrunn%2C+Tyrol%2C+Austria',
                                           'Fladnitz+an+der+Teichalm%2C+Styria%2C+Austria',
                                           'Fuschl+am+See%2C+Salzburg%2C+Austria',
                                           'Galt%C3%BCr%2C+Tyrol%2C+Austria',
                                           'Saalbach+Hinterglemm%2C+Salzburg%2C+Austria',
                                           'Hintertux%2C+Tyrol%2C+Austria', 'Itter%2C+Tyrol%2C+Austria',
                                           'Jerzens%2C+Tyrol%2C+Austria',
                                           'Kappl%2C+Tyrol%2C+Austria', 'Katschberg%2C+Austria',
                                           'Laa+an+der+Thaya%2C+Lower+Austria%2C+Austria',
                                           'Lech+am+Arlberg%2C+Vorarlberg%2C+Austria',
                                           'Lermoos%2C+Tyrol%2C+Austria'],
                              'zoneCode': ['3761', '-1985130', '-1985833', '-1986128', '-1986667', '-1986857',
                                           '-1987708',
                                           '-1989230',
                                           '-1990195', '-1991873', '-1991877', '900047955', '-1990436', '-1990443',
                                           '-1990314',
                                           '-1994413', '6009954', '-1976035', '-1976999', '-1977084', '-1977519',
                                           '-1977651', '-1989883',
                                           '-1980413', '6011229', '-1981581', '-1981913', '15286', '-1983476',
                                           '-1983913',
                                           '-1984126'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'region', 'city', 'city', 'city']},

                             {'city': 'Lanzarote',
                              'zoneName': ['Charco del Palo, Canary Islands, Spain', 'Conil, Canary Islands, Spain',
                                           'Lanzarote, Spain',
                                           'La santa, Tinajo, Canary Islands, Spain'],
                              'zoneCode': ['900049819', '-378656', '760', '-404240'],
                              'zoneType': ['city', 'city', 'region', 'city']},

                             {'city': 'Venice (and vicinity)',
                              'zoneName': ['Venice-Lido, Veneto, Italy', ' Mestre, Veneto, Italy',
                                           ' Marghera, Veneto, Italy',
                                           ' Venice, Veneto, Italy', ' Campalto, Veneto, Italy',
                                           'Bibione, Veneto, Italy',
                                           'Caorle, Veneto, Italy', 'Chioggia, Veneto, Italy', 'Dolo, Veneto, Italy',
                                           'Favaro Veneto, Veneto, Italy', 'Lido di Jesolo, Veneto, Italy',
                                           'Marcon, Veneto, Italy',
                                           'Mira, Veneto, Italy', 'Mirano, Veneto, Italy',
                                           'Mogliano Veneto, Veneto, Italy',
                                           'Murano, Veneto, Italy', 'Noventa di Piave, Veneto, Italy',
                                           "Quarto d'Altino",
                                           'Veneto',
                                           'Italy', 'Tessera', 'Veneto', 'Italy', 'Venetien', 'Italien',
                                           'Cannaregio, Venice, Veneto, Italy',
                                           'Venice city Center, Venice, Veneto, Italy',
                                           'Venice Biennale, Venice, Veneto, Italy', 'Castello, Venice, Veneto, Italy',
                                           'San Marco, Venice, Veneto, Italy'],
                              'zoneCode': ['-120151', '-121620', '-121068', '-132007', '-112732', '-111592', '-113074',
                                           '-115437',
                                           '-116857', '-117323', '-120157', '-121043', '-121796', '-121814', '-121885',
                                           '-122830',
                                           '-123154', '-125976', '-130716', '914', '621', '2291', '1138566', '625',
                                           '620'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'region',
                                           'district',
                                           'district', 'district', 'district', 'district']},

                             {'city': 'Nottingham',
                              'zoneName': ['Grantham, Lincolnshire, United Kingdom',
                                           'Newark upon Trent, Nottinghamshire, United Kingdom'],
                              'zoneCode': ['-2597411', '-2603908'],
                              'zoneType': ['city', 'city']},

                             {'city': 'Panama city',
                              'zoneName': ['Panama%20city%2C%20Panama%2C%20Panama', 'Tocumen, Panama, Panama',
                                           'Playa Bonita Village, Panama, Panama', 'Gamboa, Panama',
                                           'ParaÃ­so, Panama, Panama'],
                              'zoneCode': ['-168008', '170900', '900051359', '-162066', '-168079'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city']},

                             {'city': 'Pontevedra',
                              'zoneName': ['Pontevedra%20Province%2C%20Spain', 'Paxarinas, Galicia, Spain',
                                           'Villalonga, Galicia, Spain'],
                              'zoneCode': ['772', '900052403', '-407764'],
                              'zoneType': ['region', 'city', 'city']},

                             {'city': 'Gran Canaria',
                              'zoneName': ['Artenara, Canary Islands, Spain', 'Arucas, Canary Islands, Spain',
                                           'El Cortijo, Canary Islands, Spain',
                                           'San NicolÃ¡s, Playa del Ingles, Canary Islands, Spain',
                                           'Sardina, Canary Islands, Spain', 'Taurito, Canary Islands, Spain',
                                           'Gran Canaria, Spain',
                                           'AgÃ¼imes, Canary Islands, Spain', 'Arucas, Canary Islands, Spain',
                                           'Vega de San Mateo, Canary Islands, Spain'],
                              'zoneCode': ['-371721', '-371751', '900040233', '900039399', '-402353', '900048242',
                                           '754',
                                           '-369422',
                                           '371751', '-406723'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'region', 'city', 'city',
                                           'city']},

                             {'city': 'Las Vegas - NV',
                              'zoneName': ['Las%20Vegas%2C%20Nevada%2C%20USA',
                                           'Mt. Charleston, Mount Charleston, Nevada, USA'],
                              'zoneCode': ['20079110', '18468'],
                              'zoneType': ['city', 'landmark']},

                             {'city': 'PAPHOS',
                              'zoneName': ['Paphos+Region%2C+Cyprus', 'Paphos city, Paphos Region, Cyprus',
                                           'Miliou, Paphos Region, Cyprus', 'Kouklia, Paphos Region, Cyprus',
                                           'Peyia, Paphos Region, Cyprus', 'Mandria, Paphos Region, Cyprus'],
                              'zoneCode': ['2874', '-2738671', '-2738586', '-2738444', '-2738712', '-2738540'],
                              'zoneType': ['region', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Puerto Vallarta',
                              'zoneName': ['Puerto%20Vallarta%2C%20Jalisco%2C%20Mexico', 'Ipala, Jalisco, Mexico',
                                           'Sayulita, Nayarit, Mexico', 'BucerÃ­as, Nayarit, Mexico',
                                           'Rincon de Guayabitos, Nayarit, Mexico', 'Nuevo Vallarta , Nayarit, Mexico',
                                           'BucerÃ­as, Nayarit, Mexico', 'Cruz de Huanacaxtle, Nayarit, Mexico',
                                           'Punta Mita, Nayarit, Mexico', 'La Laguna, Jalisco, Mexico',
                                           'Quemaro, Jalisco, Mexico'],
                              'zoneCode': ['-1690444', '-1671436', '-1702968', '-1653523', '-1693798', '900047970',
                                           '-1653523',
                                           '-1659840', '-1690519', '-1675331', '-1690655'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city']},

                             {'city': 'Moscow',
                              'zoneName': ['Podolsk, Moscow region, Russia', 'Domodedovo',
                                           'Khimki, Moscow region, Russia',
                                           'Stupino, Moscow region, Russia', "Kotel'niki", 'Moscow region, Russia',
                                           'ShebantsÃ«vo, Moscow region, Russia', 'Denezhnikovo, Moscow region, Russia',
                                           'Odintsovo, Moscow region, Russia', 'Skolkovo, Moscow region, Russia',
                                           'Dolgoprudnyy, Moscow region, Russia', 'Kostrovo, Moscow region, Russia',
                                           'Moscow, Russia',
                                           'Serpukhov, Moscow region, Russia'],
                              'zoneCode': ['-2984157', '-2902898', '-2925518', '-3012362', '-2934601', '-3001462',
                                           '-2901252',
                                           '-2972924', '-3005248', '-2902591', '-2934437', '-2960561', '-2999411'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city']},

                             {'city': 'St Petersburg',
                              'zoneName': ['Saint%20Petersburg%2C%20Russia', 'Repino, Leningrad Region, Russia',
                                           'Pulkovo Airport, Saint Petersburg, Russia'],
                              'zoneCode': ['-2996338', '-2991998', '227'],
                              'zoneType': ['city', 'city', 'airport']},

                             {'city': 'San Francisco Area - CA',
                              'zoneName': ['Chinatown, San Francisco, CA, United States',
                                           'San Francisco, California, USA',
                                           'Brentwood, California, USA', 'Half Moon Bay, California, USA',
                                           'Mill Valley, California, USA', 'Millbrae, CA, United States',
                                           'Sausalito, California, USA',
                                           'Pacifica, California, USA', 'Redwood city, California, USA',
                                           'Burlingame, CA, United States',
                                           'Belmont, California, USA', 'San Bruno, California, USA',
                                           'Brisbane, California, USA',
                                           'South San Francisco, California, USA', 'San Mateo, California, USA',
                                           'Daly city, California, USA', 'Tiburon, California, USA'],
                              'zoneCode': ['1431', '20015732', '20011784', '20013330', '20014467', '20014468',
                                           '20015832',
                                           '20015042',
                                           '20015482', '20011872', '20011584', '20015722', '20011800', '20016097',
                                           '20015758',
                                           '20012461', '20016422'],
                              'zoneType': ['district', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city', 'city',
                                           'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'WARSAW',
                              'zoneName': ['Grebiszew%2C+Masovia%2C+Poland', 'Piaseczno%2C%20Masovia%2C%20Pol',
                                           'Jachranka%2C%20Masovia%2C%20Pol', 'Raszyn%2C%20Masovia%2C%20Poland',
                                           'JÃ³zefÃ³w, Masovia, Poland', 'O?tarzew, Masovia, Poland',
                                           'PruszkÃ³w, Masovia, Poland',
                                           'T?uszcz, Masovia, Poland', 'Warsaw, Masovia, Poland',
                                           'Warsaw, Masovia, Poland'],
                              'zoneCode': ['900048522', '-521463', '-504634', '-525210', '-506064', '-519890',
                                           '-523884',
                                           '-532887',
                                           '-534433', '-534433'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city']},

                             {'city': 'Madrid',
                              'zoneName': ['Madrid%2C%20Community%20of%20Madrid%2C%20Spain',
                                           'El Molar, Community of Madrid, Spain',
                                           'Velilla de San Antonio, Community of Madrid, Spain',
                                           'Madrid city Center, Madrid, Comunidad de Madrid, Spain',
                                           'Barrio de las Letras, Madrid, Community of Madrid, Spain',
                                           'Lavapies, Madrid, Community of Madrid, Spain',
                                           'Malasana, Madrid, Community of Madrid, Spain',
                                           'Chueca, Madrid, Community of Madrid, Spain'],
                              'zoneCode': ['765', '-380874', '-406840', '176', '3253', '3252', '6629', '2765'],
                              'zoneType': ['region', 'city', 'city', 'district', 'district', 'district', 'district',
                                           'district']},

                             {'city': 'Stuttgart',
                              'zoneName': ['Ditzingen, Baden-WÃ¼rttemberg, Germany',
                                           'Boblingen, Baden-Wurttemberg, Germany',
                                           'Filderstadt, Baden-Wurttemberg, Germany',
                                           'Goppingen, Baden-Wurttemberg, Germany',
                                           'Leinfelden-Echterdingen, Baden-Wurttemberg, Germany',
                                           'Ludwigsburg, Baden-Wurttemberg, Germany',
                                           'Niefern-Oschelbronn, Baden-Wurttemberg, Germany',
                                           'Sindelfingen, Baden-Wurttemberg, Germany',
                                           'Stuttgart, Baden-Wurttemberg, Germany'],
                              'zoneCode': ['-1759934', '-1749166', '6181536', '-1777648', '-1817634', '-1821445',
                                           '15123',
                                           '-1865057',
                                           '-1871728'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city']},

                             {'city': 'Marrakech',
                              'zoneName': ['Gueliz, Marrakech, Marrakech-Safi, Morocco',
                                           'Imlil, ?Marrakech-Safi, ?Morocco',
                                           'Lalla Takerkoust, ?Marrakech-Safi, ?Morocco',
                                           'Ouirgane, ?Marrakech-Safi, ?Morocco',
                                           'Marrakech%2C%20Marrakech-Tensift-Haouz%2C%20Morocco',
                                           'Marrakech-Safi, Morocco'],
                              'zoneCode': ['2314', '-35522', '-38225', '-41331', '-38833', '4992'],
                              'zoneType': ['district', 'city', 'city', 'city', 'city', 'region']},

                             {'city': 'Porto and North of Portugal',
                              'zoneName': ['Amarante, Norte Region, Portugal', 'Amares, Norte Region, Portugal',
                                           'BaiÃ£o, Norte Region, Portugal', 'Barcelos, Norte Region, Portugal',
                                           'Boticas, Norte Region, Portugal', 'Braga, Norte Region, Portugal',
                                           'BraganÃ§a, Norte Region, Portugal',
                                           'Cabeceiras de Basto, Norte Region, Portugal',
                                           'Caminha, Minho, Portugal', 'Cerva, Norte Region, Portugal',
                                           'Chaves, Norte Region, Portugal',
                                           'Covas do Douro, Norte Region, Portugal', 'Espinho, Norte Region, Portugal',
                                           'Esposende, Minho, Portugal', 'Fafe, Norte Region, Portugal',
                                           'Geres, Norte Region, Portugal',
                                           'GuimarÃ£es, Norte Region, Portugal', 'Lamego, Norte Region, Portugal',
                                           'LeÃ§a da Palmeira, Norte Region, Portugal', 'Maia, Norte Region, Portugal',
                                           'Marialva, Centro Region, Portugal', 'Matosinhos, Norte Region, Portugal',
                                           'MesÃ£o Frio, Norte Region, Portugal', 'MonÃ§Ã£o, Norte Region, Portugal',
                                           'Mondim de Basto, Norte Region, Portugal', 'Paredes, Norte Region, Portugal',
                                           'Pedras Salgadas, Norte Region, Portugal',
                                           'Penafiel, Norte Region, Portugal',
                                           'Ponte da Barca, Norte Region, Portugal',
                                           'Ponte de Lima, Norte Region, Portugal',
                                           'PÃ³voa de Lanhoso, Norte Region, Portugal',
                                           'PÃ³voa de Varzim, RegiÃ£o do Norte, Portugal',
                                           'Raiva, Norte Region, Portugal', 'Sandim, Norte Region, Portugal',
                                           'Santa Maria da Feira, Norte Region, Portugal',
                                           'Viana do Castelo, Norte Region, Portugal',
                                           'Vidago, Norte Region, Portugal', 'Vila do Conde, Norte Region, Portugal',
                                           'Vila Nova de Cerveira, Norte Region, Portugal',
                                           'Vila Nova de Gaia, Norte Region, Portugal',
                                           'Vila Praia de Ã‚ncora, Norte Region, Portugal',
                                           'Vila Real, Norte Region, Portugal',
                                           'Vizela, Norte Region, Portugal', 'QuintiÃ£es, Norte Region, Portugal',
                                           'Lousada, Norte Region, Portugal',
                                           'Santa Marinha do ZÃªzere, Norte Region, Portugal',
                                           'BastuÃ§o, Norte Region, Portugal', 'Vale de Mendiz, Norte Region, Portugal',
                                           'PaÃ§o de Sousa, Norte Region, Portugal', 'Pinheiro, Norte Region, Portugal',
                                           'CervÃ£es, Norte Region, Portugal',
                                           'Porto%2C%20Norte%20Region%2C%20Portugal',
                                           'Norte Region'],
                              'zoneCode': ['-2158154', '-2158170', '-2159167', '-2159373', '-2160125', '-2160205',
                                           '-2160210',
                                           '-2160536', '-2160957', '-2162849', '-2163041', '-2163880', '-2164773',
                                           '-2164801',
                                           '-2164952', '900040488', '-2167026', '-2167651', '-2167860', '-2167860',
                                           '-2168721',
                                           '-2168998', '-2169217', '-2169585', '-2169602', '-2171601', '-2171847',
                                           '-2172017', '-2'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'region']},

                             {'city': 'Frankfurt',
                              'zoneName': ['Frankfurt, Hessen, Germany', 'Bad Soden am Taunus, Hessen, Germany',
                                           'Bad Vilbel, Hessen, Germany', 'Eschborn, Hessen, Germany',
                                           'Friedrichsdorf, Hessen, Germany',
                                           'Hanau am Main, Hessen, Germany', 'KÃ¶nigstein im Taunus, Hessen, Germany',
                                           'Kronberg im Taunus, Hessen, Germany', 'Maintal, Hessen, Germany',
                                           'Neu Isenburg, Hessen, Germany', 'Offenbach, Hessen, Germany',
                                           'RÃ¶dermark, Hessen, Germany',
                                           'RÃ¼sselsheim, Hessen, Germany', 'Wetzlar, Hessen, Germany',
                                           'Hessen%2C%20Germany'],
                              'zoneCode': ['1771148', '-1743251', '-1743269', '-1767533', '-1772058', '-1785726',
                                           '-1811043', '-1813055',
                                           '-1822609', '-1832053', '-1838156', '900039293', '-1854081', '-1887191',
                                           '705'],
                              'zoneType': ['city', 'city', 'city', 'city', 'city', 'city', 'city', 'city', 'city',
                                           'city',
                                           'city',
                                           'city', 'city', 'city', 'region']},

                             {'city': 'Hamburg',
                              'zoneName': ['Hamburg, Hansestadt Hamburg, Germany',
                                           'Itzehoe, Schleswig-Holstein, Germany',
                                           'Buchholz, ?Lower-Saxony, ?Germany', 'Schleswig-Holstein, Germany'],
                              'zoneCode': ['-1785434', '-1801207', '824569', '714'],
                              'zoneType': ['city', 'city', 'city', 'city']},

                             {'city': 'Geneva',
                              'zoneName': ['Canton of Geneva, Switzerland', 'Vaud, Switzerland'],
                              'zoneCode': ['3958', '3931'],
                              'zoneType': ['region', 'region']},

                             {'city': 'Granada',
                              'zoneName': ['Granada+Province%2C+Spain', 'HuÃ©scar, ?AndalucÃ­a, ?Spain',
                                           'Moraleda de Zafayona, ?AndalucÃ­a, ?Spain', ],
                              'zoneCode': ['755', '385647', '-392931', ],
                              'zoneType': ['region', 'city', 'city', ]}]

        for mapped_city in mapped_cities:
            if city.lower() in mapped_city['city'].lower():
                return mapped_city['city'], mapped_city['zoneName'], mapped_city['zoneCode'], mapped_city['zoneType']

    def get_latlong(self, zone):
        a= zone
        latlong={'Parc Asterix Amusement Park, Plailly, Picardy, France': 'Latitude:49.601756 | Longitude: 2.87162207855588',
        'Loul%C3%A9%2C+Algarve%2C+Portugal': 'Latitude:37.21427465 | Longitude: -8.08652381525089',
        'Algarve%2C%20Portugal': 'Latitude:37.2454248 | Longitude: -8.15092527307923',
        'Disneyland Paris, France': 'Latitude:48.8711359 | Longitude: 2.77612651196751',
        'Dourdan, Ile de France, France': 'Latitude:48.5288442 | Longitude: 2.0153689',
        'Melun, Ile de France, France': 'Latitude:48.539927 | Longitude: 2.6608169',
        'Canton of Geneva, Switzerland': 'Latitude:46.2017559 | Longitude: 6.1466014',
        'Doha, Qatar': 'Latitude:25.2856329 | Longitude: 51.5264162',
        'Vaud, Switzerland': 'Latitude:46.6356963 | Longitude: 6.5320717',
        'Ile de France, France': 'Latitude:48.6443057 | Longitude: 2.7537863'
        }

        if zone in latlong.keys():
            return latlong[zone]

    @property
    def _get_url_params(self):
        i = 0

        payload_list = []
        city, zones, zoneCodes, zoneTypes = self.get_zones(self.city)
        homePageText, res_obj, driver_obj = self.get_request('https://www.bestwestern.com/en_US.html',self.headers, self.proxy, driver=self.HOTEL_LIST_DRIVER)
        if res_obj.status_code == 200:
            print("Homepage hit success")
            # geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
            # location = geolocator.geocode(self.city+', '+self.country)
            # print((location.latitude, location.longitude))
        else:
            print(res_obj.status_code)
        # self.cookie=res_obj.cookies
        cookieDict = res_obj.cookies.get_dict()
        # self.headers2 = res_obj.headers.get_dict()
        for zone in zones:
            print(zone)
            for zone in zones:
                print(zone)
                latlongstring = self.get_latlong(zone)

                if len(latlongstring) > 0:
                    latlong1 = latlongstring.split('|')
                    latitude = latlong1[0].replace('Latitude', '').replace(':', '').strip()
                    longitude = latlong1[1].replace('Longitude', '').replace(':', '').strip()
            # location = geolocator.geocode(zone)
            # if len(location)>0:
            #     print((location.latitude, location.longitude))
            #     latitude=location.latitude
            #     longitude=location.longitude

            inDate = self.check_in
            format_str = '%d/%m/%Y'  # The format
            inDate = datetime.datetime.strptime(self.check_in, format_str)
            outDate = BW_LandingPage.checkOut_date
            # outDate= datetime.datetime.strptime(BW_LandingPage.checkOut_date, format_str)

            yy1, mm1, dd1 = inDate.year, inDate.month, inDate.day
            yy2, mm2, dd2 = outDate.year, outDate.month, outDate.day
            BW_LandingPage.formattedoutdate=str(yy2) + '-' +str(mm2) + '-' + str(dd2)
            BW_LandingPage.formattedindate=str(yy1)+'-'+str(mm1)+'-'+str(dd1)

            BW_LandingPage.adults = self.adults
            payload = {
                'gwServiceURL':'HOTEL_SEARCH',
                'distance': '50',
                'depth':'2',
                'checkinDate':str(yy1)+'-'+str(mm1)+'-'+str(dd1),
                'checkoutDate': str(yy2) + '-' +str(mm2) + '-' + str(dd2),
                'latitude':latitude,
                'longitude':longitude,
                'numberOfRooms':'1',
                'occupant':'numAdults:'+str(self.adults)+',numChild:0'
            }
            print (payload)
            i = i+1
            payload_list.append(payload)
            if i > 0:
                break
        return payload_list

    @property
    def _hotels(self):
        codeurllist=[]
        codelist=[]
        """
        return hotel link from hotelLinksXpath
        :return: self._html.xpath(self.CONFIG_FILE.hotelLinksXpath)
        """
        try:
            itemdict= json.loads(self._html)
            for i in range(0,len(itemdict)):
                code=itemdict[i]['resort']
                name=itemdict[i]['resortSummary']['name']
                addr=itemdict[i]['resortSummary']['address1']+','+itemdict[i]['resortSummary']['city']+', '+itemdict[i]['resortSummary']['postalCode']+', '+itemdict[i]['resortSummary']['country']
                finalval=code+' || '+name+' || '+addr

                finalurl="https://www.bestwestern.com/en_US/book/"+str(itemdict[i]['resortSummary']['city']).lower()+"/hotel-rooms/"+str(name).lower().replace(' ','-').replace("\'",'-')+"/propertyCode."+str(code)+".html"

                codelist.append(code)
                codeurllist.append(finalval+"| "+ finalurl)
        except(ProxyHandler.EXCEPTIONS['HOTEL_NOT_FOUND']) as e:
            raise ProxyHandler.EXCEPTIONS['HOTEL_NOT_FOUND']
        self.hotel_count = len(codelist)
        return codeurllist

    def _set_cookie(self, cookie_object):
        """
        :param cookie_object: either request or driver object to get cookie and set in self.cookie
        :return:
        """
        self.cookie = cookie_object.get_dict()

    def _set_html(self):
        if self._get_visit_homepage():
            self._process_homepage()
            self.TRL.debug_log('Visited Homepage', self.request_id, self.sub_request_id, self.request_run_id)

        self.TRL.debug_log('Setting HTML', self.request_id, self.sub_request_id, self.request_run_id)
        # params = self._get_url_params

        html_list = self._get_hotel_list()
        return html_list

    def _url_maker(self):

        i=0
        url_list = []
        city, zones, zoneCodes, zoneTypes = self.get_zones(self.city)

        self.TRL.debug_log('Host:%s' % self._get_host_url_for_url_maker, self.request_id, self.sub_request_id,self.request_run_id)

        homePageText, res_obj, driver_obj = self.get_request('https://www.bestwestern.com/en_US.html', self.headers,                                                             self.proxy, driver=self.HOTEL_LIST_DRIVER)
        if res_obj.status_code == 200:
            print("Homepage hit success")

        else:
            print(res_obj.status_code)
        cookieDict = res_obj.cookies.get_dict()

        for zone in zones:
            print(zone)
            latlongstring= self.get_latlong(zone)

            if len(latlongstring) > 0:
                latlong1=latlongstring.split('|')
                latitude = latlong1[0].replace('Latitude','').replace(':','').strip()
                longitude = latlong1[1].replace('Longitude','').replace(':','').strip()

            inDate = self.check_in
            format_str = '%d/%m/%Y'  # The format
            # inDate = datetime.datetime.strptime(self.check_in, format_str)
            outDate = BW_LandingPage.checkOut_date
            inDate = self.check_in

            # outDate= datetime.datetime.strptime(BW_LandingPage.checkOut_date, format_str)

            yy1, mm1, dd1 = inDate.year, inDate.month, inDate.day
            yy2, mm2, dd2 = outDate.year, outDate.month, outDate.day
            if (len(str(mm1)))==1:
                mm1='0'+str(mm1)
                mm2='0'+str(mm2)

            BW_LandingPage.adults = self.adults

            url= "https://www.bestwestern.com/bin/bestwestern/proxy?gwServiceURL=HOTEL_SEARCH&distance=50&depth=2&checkinDate="+str(yy1)+'-'+str(mm1)+'-'+str(dd1)+"&checkoutDate="+str(yy2)+'-'+str(mm2)+'-'+str(dd2)+"&latitude="+str(latitude)+"&longitude="+str(longitude)+"&numberOfRooms=1&occupant=numAdults:"+str(self.adults)+",numChild:0"

            i = i + 1
            url_list.append(url)
            if i > 0:
                break
        return url_list

    def _get_hotel_list(self, url=None):
        """Overrided to added timeout value"""
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
        print(link)
        try:
            pass
            # self.proxy.check_proxy('https://www.bestwestern.com/en_US/book/hotel-search.html', self.headers)
        except (
            ProxyHandler.EXCEPTIONS['SERVER_DOWN_ERROR'],
            ProxyHandler.EXCEPTIONS['SERVER_ERROR'],
            ProxyHandler.EXCEPTIONS['PNF_ERROR'],
            ProxyHandler.EXCEPTIONS['PROXY_AUTH_ERROR'],
            ProxyHandler.EXCEPTIONS['REQUEST_ERROR']
        ) as e:
            self.TRL.error_log(
                'No Working Proxy Found:%s' % str(e), self.request_id, self.sub_request_id, self.request_run_id,headers=self.headers)
            raise ProxyHandler.EXCEPTIONS['NOT_WORKING']
        time.sleep(random.choice([6,5,4]))

        newheaders={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'www.bestwestern.com',
            'Referer': 'https://www.bestwestern.com/en_US/book/hotel-search.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        resp_html, resp_obj, _ = self.get_request(link[0],newheaders,self.proxy, driver=self.HOTEL_LIST_DRIVER,timeout=30)
        if resp_obj.status_code==200:
            print("Hotel search list page hit successs")
            with open("BW_hoteldetail.html", "w", encoding="utf-8") as file:
                file.write(resp_html)
            # item_dict = json.loads(resp_html)
        else:
            self.TRL.debug_log('Setting Cookie', self.request_id, self.sub_request_id, self.request_run_id)
            request_type = RequestHandler._get_request_type()
            if request_type['driver']:
                self._set_cookie(_)
            else:
                self._set_cookie(resp_obj.cookies)
            self.TRL.debug_log('Cookie: %s' % self.cookie, self.request_id, self.sub_request_id, self.request_run_id)
        return resp_html

    @property
    def _get_headers(self):
        """
        :param headers_object: either request or driver object to get headers and set in self.headers
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }
        return headers

    def _save_hotel(self, index, hotel_data_dict):
        hotel = BW_Hotel.get_hotel(hotel_data_dict,None,self)
        self.TRL.debug_log('Saving with Index:%s' % index, self.request_id, self.sub_request_id, self.request_run_id)
        return hotel.save_html(index)

    def crawl_hotels(self, redelivered):
        # redelivered = False
        partial_hotels = list()
        if redelivered:
            partial_hotels = self.SERVICE_CALLS['get_partial_hotels'](self.sub_request_id)
            print('crawled_hotels found')
            print(len(partial_hotels))

        self.TRL.debug_log('Starting Crawl', self.request_id, self.sub_request_id, self.request_run_id)
        try:
            self._html=self._set_html()
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ProxyError
        ) as e:
            raise self.EXCEPTIONS['SCRIPT_TIMEOUT']
        hotel_url_list = self._hotels
        self.TRL.debug_log('Hotels Found:%s' % len(hotel_url_list), self.request_id, self.sub_request_id, self.request_run_id)
        crawled_hotels = partial_hotels
        hotels_count = len(crawled_hotels)
        for i, hotel in enumerate(hotel_url_list[hotels_count:]):
            if i >0:
                break

            i += hotels_count
            try:
                hotel = self._save_hotel(i, hotel)
                crawled_hotels.append(hotel)
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
        return self.request_data

def crawl_hotels(consumer_data, redelivered):
    import time
    print('starting crawl')
    start_time = time.time()
    checkIn_date = (consumer_data['RequestInputs']['checkIn'])
    # checkOut_date=(consumer_data['RequestInputs']['checkOut'])
    consumer_data['RequestInputs']['checkIn'] = checkIn_date
    BW_LandingPage.checkOut_date = checkIn_date + datetime.timedelta(int(consumer_data['RequestInputs']['nights']))
    crawled_data = BW_LandingPage(consumer_data).crawl_hotels(redelivered)
    end_time = time.time()
    print('total time "%s"' % (end_time - start_time))
    crawled_data.update({'RequestInputs': consumer_data['RequestInputs']})
    crawled_data['RequestInputs']['checkIn'] = str(crawled_data['RequestInputs']['checkIn'])
    crawled_data['RequestInputs']['checkOut'] = str(BW_LandingPage.checkOut_date)
    print('\ncrawling hotels')
    print(type(crawled_data))
    return crawled_data
#
# sample = {
#     "requestId": "12",
#     "subRequestId": "1",
#     "requestRunId": "",
#     "DomainName": "https://www.bestwestern.com/en_US.html",
#     "country":"Portugal",
#     "RequestInputs": {
#         "city":"Algarve",
#         "children": 0,
#         "adults": 2,
#         "room": "1",
#         "board": "",
#         "checkIn": "15/02/2019",
#         "checkOut": "17/02/2019",
#         "nights": 2,
#         "days": 5,
#         "hotelName": "",
#         "starRating": "",
#         "fromAirport": "",
#         "toAirport": "",
#         "webSiteHotelId": "",
#         "pos": "Spain",
#         "crawlMode": ""
#     }
# }
#
# crawled_data = crawl_hotels(sample,False)
# with open("BW_CrawledData.json", "w", encoding="utf-8") as file:
#     file.write(json.dumps(crawled_data,indent=4))
# # # # #
# with open("BW_CrawledData.json", 'r') as f:
#     crawled_data = json.load(f)
# #
# from AetosParsingService.scripts import ParserBestwesternPython
# parsed_data = ParserBestwesternPython.crawl_hotels(crawled_data)
# with open("BW_ParsedData.json", "w", encoding="utf-8") as file:
#     file.write(json.dumps(parsed_data,indent=4))
# # print(parsed_data)