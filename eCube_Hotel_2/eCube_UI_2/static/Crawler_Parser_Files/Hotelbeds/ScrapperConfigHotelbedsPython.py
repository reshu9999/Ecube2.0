visitHomePage = False
requestType = {
    'request': True,
    'driver': False
}


hotelLinksXpath = '//hotel'
ratingsXpath = '//div[@class="propertyInner"]//div[@class="propertyImageOuter"]/following-sibling::*[1]//span[@class = "ratingContainer"]/span[1]/text()'
latLongXpath = '//div[@id = "contentArea"]//div[@class = "rateOptions"]/a[1]/../..//preceding-sibling::div[@class="propertyDetails"]/h2/a/@href'
hotelNamesWithRatingsOnlyXpath = '//div[@class="propertyInner"]//div[@class="propertyImageOuter"]/following-sibling::*[1]//span[@class = "ratingContainer"]/../../../../../../../h2/a/text()[1]'

hotel_ZoneName="//hotel/@destinationcode"
hotelNameXpath = '//hotel/@name'
propertyIDXpath = '//span[@class="propertyName"]/a/@href'
datesXpath = '//div[@class="headingContainer leftContainer"]/a/span[1]/text()'
adultsXpath = '//div[@class="headingContainer leftContainer"]/a/span[2]/text()[1]'
containersXpath = '//div[contains(@class, "roomContainer")]//div[@class = "roomBlock"]//div[@class = "rateDetailsBlock"]/../../../..'
headingInContainersXpath = './/h1/text()[1]'
roomDetailsInContainersXpath = './/div[@class = "roomDetails"]/ul/li/text()'
pricesInContainersXpath = './/span[@class="reserveLink"]/span[@class="roomTotal"]/text() | .//span[@class="reserveLink"]/span[@class="roomRate"]/text()[2]'
pricesInContainersXpath2 = './/span[@class="reserveLink"]/span[@class="roomTotal"]/text() | .//span[@class="reserveLink"]/span[@class="roomRate"]/text()'


# latitude_longitude() function : xpaths
latitudeXpath = '//meta[@property="og:latitude"]/@content'
longitudeXpath = '//meta[@property="og:longitude"]/@content'
addressXpath = '//ul[@id="propertyAddress"]/li/*/text()'
