# getData(, function : xpaths

# REQUIRED
visitHomePage = True


requestType = {
    'request': True,
    'driver': False
}


hotelLinksXpath = '//div[@data-hotelid and @data-hotelname]'
ratingsXpath = ''
latLongXpath = ''
hotelNamesWithRatingsOnlyXpath = ''


hotelNameXpath = '//h3[@class="hotel_desc_name"]/text()'
propertyIDXpath = ''
datesXpath = ''
adultsXpath = ''
containersXpath = ''
headingInContainersXpath = ''
roomDetailsInContainersXpath = ''
pricesInContainersXpath = ''
pricesInContainersXpath2 = ''


# latitude_longitude(, function : xpaths
latitudeXpath = ''
longitudeXpath = ''
addressXpath = ''

# HOST
HOST = 'https://us.dotwconnect.com/'

travellers_data_dict = {
    1: {
        "children": 0,
        "adults": 1,
        "childage1": 3,
        "childage2": 3,
    },
    2: {
        "adults": 2,
        "children": 0,
        "childage1": 3,
        "childage2": 3,
    },
    3: {
        "adults": 2,
        "children": 1,
        "childage1": 6,
        "childage2": 3,
    },
    4: {
        "adults": 2,
        "children": 2,
        "childage1": 6,
        "childage2": 8,
    }
}

# CREDENTIALS
user_id = "fortest"
password = "Test1234"
company_code = "1348075"


login_page_url = "https://us.dotwconnect.com/interface/en/login"
user_login_url = "https://us.dotwconnect.com/interface/en/login/customer"
next_hotel_list_page_url = "https://us.dotwconnect.com/interface/en/accommodation/getRemainingResults/{0}"

hotel_data_url = "https://us.dotwconnect.com/interface/en/accommodation/getInfo/{0}?"

# headers
login_page_header = {
    "Accept": "text/html, application/xhtml+xml, */*",
    "Accept-Language": "en-US",
    "Host": "us.dotwconnect.com",
    "Proxy-Connection": "Keep-Alive",
    "Referer": "https://us.dotwconnect.com/interface/en/accommodation",
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0,",
}

user_login_header = {
    "Accept": "text/html, application/xhtml+xml, */*",
    "Accept-Language": "en-US",
    "Host": "us.dotwconnect.com",
    "Proxy-Connection": "Keep-Alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://us.dotwconnect.com/interface/en/login",
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0,",
}

city_code_header = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US",
    "Host": "us.dotwconnect.com",
    "Proxy-Connection": "Keep-Alive",
    "Referer": "https://us.dotwconnect.com/interface/en/accommodation",
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "X-Requested-With": "XMLHttpRequest",
}

Kuala_Lumpur = {
    "21894": "KUALA+LUMPUR",
    "22054": "PETALING+JAYA",
    "21804": "CYBERJAYA",
    "22144": "SHAH+ALAM",
    "22074": "PUTRAJAYA",
    "22124": "SEPANG",
}

KUALA_LUMPUR = {
    "21894": "KUALA+LUMPUR",
    "22054": "PETALING+JAYA",
    "21804": "CYBERJAYA",
    "22144": "SHAH+ALAM",
    "22074": "PUTRAJAYA",
    "22124": "SEPANG",
}

Istanbul = {
    "14214": "ISTANBUL",
    "146165": "ISTANBUL+(SILE)",
}

ISTANBUL = {
    "14214": "ISTANBUL",
    "146165": "ISTANBUL+(SILE)",
}
