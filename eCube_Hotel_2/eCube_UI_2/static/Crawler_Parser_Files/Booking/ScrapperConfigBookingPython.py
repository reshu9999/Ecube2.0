visitHomePage = False
requestType = {
    'request': True,
    'driver': False
}


hotelLinksXpath ="//h3/a[@class='hotel_name_link url']/@href"
hotelNameXpath= '//span[contains(@class,"sr-hotel__name")]/text()'
multizonecountpath='<MultizoneCount>([\d.]*)<'
zoneidpath='<ZoneID>([\d\S].*?)<'
zonenamepath='<ZoneName>([\w\S].*?)<'
zonetypepath='<ZoneType>([\w\S].*?)<'
currpath='//input[@name="selected_currency"]/@value'
latpath='booking.env.b_map_center_latitude\W*([\d.]*);'
longpath='booking.env.b_map_center_longitude\W*([\d.]*);'
starpath='//p[@class="filtercategory-title"][contains(text(),"Star rating") or contains(text(),"Star Rating")]/../../div[@class="filteroptions"]'
hotelid='hotelid\W+([\d].*?)"'




#
# visitHomePage = False
# requestType = {
#     'request': True,
#     'driver': False
# }
#
# hotel_blocksXpath = '//div[@id="hotellist_inner"]/div[boolean(@data-hotelid) and not(contains(@class, "soldout_property"))]'
# hotel_idXpath = './@data-hotelid' #to be used with hotel_blocksXpath element
# hotelLinksXpath =   './div[not(contains(@class, "sold"))]//*[@class="hotel_name_link url"]/@href'#'//div[@id="hotellist_inner"]/div[not(contains(@class, "sold"))]//*[@class="hotel_name_link url"]/@href' #'//div[@id="hotellist_inner"]//*[@class="hotel_name_link url"]/@href' #'//strong[contains(@class,"price")]/../../../../../../../..//*[@class="hotel_name_link url"]/@href'
# ratingsXpath = '//div[@class="propertyInner"]//div[@class="propertyImageOuter"]/following-sibling::*[1]//span[@class = "ratingContainer"]/span[1]/text()'
# latLongXpath = '//div[@id = "contentArea"]//div[@class = "rateOptions"]/a[1]/../..//preceding-sibling::div[@class="propertyDetails"]/h2/a/@href'
# hotelNamesWithRatingsOnlyXpath = '//strong[contains(@class,"price")]/../../../../../../../..//*[@class="hotel_name_link url"]/@href'
# hotelpage_priceblocks =  '//span[contains(@class, "hprt-price")]/../../../..' #"//table[@id='maxotel_rooms']/tbody/tr[not(contains(@class, 'extendedRow sold'))]" #
# maxAdultsXpath = './/div[contains(@class, "hprt-occupancy-occupancy-info jq_tooltip")]/i'
#
# hotelpage_single_blockID = './@data-block-id'
# next_pageURL = '//*[contains(@class, "pagination__next")]/a/@href'
#
# tax_statusXpath = './/div[@class="hptr-taxinfo-block"]/div[@class="hptr-taxinfo-details"]/span[@class="hptr-taxinfo-label"]/text()'
# tax_descXpath = './/div[@class="hptr-taxinfo-block"]/div[@class="hptr-taxinfo-details"]/text()'
#
# unmatchHotelNameXpath = '//h3[contains(@class, "sr-hotel__title")]/a/span[contains(@class,"sr-hotel__name")]/text()'
# hotelNameXpath = '//*[@id="hp_hotel_name"]/text()'
# hotelID = '//*[@data-model="hotel_id"]/@value'
# allblockIDs = '//span[contains(@class, "hprt-price")]/../../../../@data-block-id'
# blockID = '//span[contains(@class, "hprt-price")]/../../../../@data-block-id'
# propertyIDXpath = '//span[@class="propertyName"]/a/@href'
# datesXpath = '//div[@class="headingContainer leftContainer"]/a/span[1]/text()'
# adultsXpath = '//div[@class="headingContainer leftContainer"]/a/span[2]/text()[1]'
# containersXpath = '//div[contains(@class, "roomContainer")]//div[@class = "roomBlock"]//div[@class = "rateDetailsBlock"]/../../../..'
# headingInContainersXpath = './/h1/text()[1]'
# roomDetailsInContainersXpath = './/div[@class = "roomDetails"]/ul/li/text()'
# pricesInContainersXpath = './/span[@class="reserveLink"]/span[@class="roomTotal"]/text() | .//span[@class="reserveLink"]/span[@class="roomRate"]/text()[2]'
# pricesInContainersXpath2 = './/span[@class="reserveLink"]/span[@class="roomTotal"]/text() | .//span[@class="reserveLink"]/span[@class="roomRate"]/text()'
#
#
# roomType = './/span[contains(@class,"hprt-roomtype")][2]/text()'
# not_included_tag = './td[contains(@class, "first")]/div[contains(@class, "hprt-roomtype-block")]//*[contains(text(), "Not included:")]'
# # latitude_longitude() function : xpaths
latitudeXpath = '//meta[@property="og:latitude"]/@content'
longitudeXpath = '//meta[@property="og:longitude"]/@content'
addressXpath = '//ul[@id="propertyAddress"]/li/*/text()'


Hotel__details1 = './/div[@class="bed-types bold-bed-types"]/text()'
Hotel__details2 = '//span[@class = "partyMix"]/text()'
Hotel__roomTypes = '//*[contains(@class, "rate-plan")]/..'
Hotel__roomType = './/span[contains(@class,"hprt-roomtype")][2]'
Hotel__promotion = '//div[@class="details"]//li[1]/text()'
Hotel__priceblocks = '//span[contains(@class, "hprt-price")]/../../../..'
Hotel__price = './/*[contains(@class, "price-standard") or contains(@class, "price-actual")]/text()'
Hotel__boardType = '//*[@class="details"]/h3/text()'
Hotel__address = '//*[@type="application/ld+json"]/text()'
Hotel__starRating = '//*[@class="hp__hotel_ratings__stars nowrap"]//span/text()'
Hotel__Lattitude = '//*[@type="application/ld+json"]/text()'
Hotel__Longitude = '//*[contains(@property, "longitude")]/@content'
Hotel__MaxAdults = './/*[contains(@class, "occupancy")]//*[@class="invisible_spoken"]/text()'
Hotel__Id = '//input[@name="hotel_id"]/@value'
Hotel__currency = '//*[@name="selected_currency"]/@value'
Hotel__adults = '//*[contains(@class, "summary-guests")]/text()'
Hotel__stay = '//*[contains(@class, "av-summary-checkout")]/following-sibling::span/text()'

RoomType__name = './/span[contains(@class,"hprt-roomtype")][2]/text()'
RoomType__price = '//span[@class="a1"]//text()'
RoomtType_best_value = './/*[contains(@class, "deal-message")]/text()'
RoomType_save_button = './/*[contains(@class, "discount-ribbon")]//text()'
RoomType_details = './/div[contains(@class, "hprt-facilities")]/text()'
RoomType__directpay = './/li[contains(@data-title, "No prepayment")]/span/text()'
RoomType__nonrefundable = '//*[contains(@data-et-mouseenter, "non_refundable")]//strong/text()'
