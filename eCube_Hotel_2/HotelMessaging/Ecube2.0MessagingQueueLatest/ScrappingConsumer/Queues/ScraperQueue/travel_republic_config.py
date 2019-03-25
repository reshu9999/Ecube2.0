# getData() function : xpaths

# REQUIRED
visitHomePage = True
requestType = {
    'request': True,
    'driver': True,
}


hotelCountXpath = ''
hotelLinksXpath = ''
ratingsXpath = ''
latLongXpath = ''
hotelNamesWithRatingsOnlyXpath = ''

hotelNameXpath = '//h1[@class="new-hotel-name"]/text()'
propertyIDXpath = ''
datesXpath = ''
adultsXpath = ''
containersXpath = ''
headingInContainersXpath = ''

roomDetailsInContainersXpath = '//table//tr[contains(@class, "room-row roomRow roomSelector")]'
pricesInContainersXpath = '//table//tr[contains(@class, "room-row roomRow roomSelector")]'
roomBoardType = '//table//tr[contains(@class, "room-row roomRow roomSelector")]'
paymentType = '//table//tr[contains(@class, "room-row roomRow roomSelector")]'
promotionType = '//table//tr[contains(@class, "room-row roomRow roomSelector")]'

matchHotelRoomDetailsInContainersXpath = '//table//tr[contains(@class, "room-row roomRow roomSelector")][1]'
matchHotelPricesInContainersXpath = '//table//tr[contains(@class, "room-row roomRow roomSelector")][1]'
matchHotelRoomBoardType = '//table//tr[contains(@class, "room-row roomRow roomSelector")][1]'
matchHotelRoomPaymentType = '//table//tr[contains(@class, "room-row roomRow roomSelector")][1]'
matchHotelRoomPromotionType = '//table//tr[contains(@class, "room-row roomRow roomSelector")][1]'


latitudeXpath = ''
longitudeXpath = ''
addressXpath = ''
