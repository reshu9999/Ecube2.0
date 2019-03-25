# getData() function : xpaths

# REQUIRED
visitHomePage = True
requestType = {
    'request': True,
    'driver': True,
}


crawlURL = 'searchWeb1000.do'
crawlURLBaseQuery = 'activity=showHotellistWithPromotion&showOverlay=true'

hotelCountXpath = ''
hotelLinksXpath = ''
ratingsXpath = '//div[@class="contentTitle"]//span[not(text())]/@class'
latLongXpath = ''
hotelNamesWithRatingsOnlyXpath = ''

hotelNameXpath = '//div[@class="contentTitle"]//span[@class="title"]/text()'
propertyIDXpath = ''
datesXpath = ''
adultsXpath = ''
containersXpath = ''
headingInContainersXpath = ''

roomDetailsInContainersXpath = '//table[@class="basketOffers"]//td[@class="roomOffer"]'
roomPromotion = '//table[@class="basketOffers"]//td[@class="roomOffer"]'
pricesInContainersXpath = '//table[@class="basketOffers"]//td[@class="roomPrice"]'
roomBoardType = '//table[@class="basketOffers"]//td[@class="roomPrice"]'

# latitude_longitude() function : xpaths
latitudeXpath = '//meta[contains(@property, "latitude")]/@content'
longitudeXpath = '//meta[contains(@property, "longitude")]/@content'
addressXpath = '//div[@class="contentTitle"]//div//address/text()'
