
LP__hotelName = './/div[@id="searchEssentials"]//*[@class="noSifr"]/a/text()[1]'

Hotel__name = '//span[@class="propertyName"]/a/text()[1]'
# Hotel__name = '//span[@class="propertyName"]//a//text()'
Hotel__details1 = '//span[@class="date"]/text()'
Hotel__details2 = '//span[@class = "partyMix"]/text()'
Hotel__roomType = './h1/text()'
Hotel__containers = '//*[contains(@class,"rateContainer") and not(contains(@class, "noImage"))]/../..'
Hotel__priceblocks = './/*[contains(@class,"rateDetails") and @data-starpoints="0"]'
Hotel__promotion = '//div[@class="details"]//li[1]/text()'
# Hotel__price = '//span[@class="reserveLink"]/span[@class="roomTotal"]/text()'
Hotel__price = './/*[@class="roomTotal"]/text() | .//*[@class="roomRate"]/text()'
# Hotel__price = './/span[@class="reserveLink"]/span[@class="roomTotal"]/text() | .//span[@class="reserveLink"]/span[@class="roomRate"]/text()'
Hotel__boardType = './/*[@class="details"]/h3/text()'
Hotel__address = '//ul[@id="propertyAddress"]/li//text()'
Hotel__starRating = '//*[@class="ratingContainer"]/span[1]/text()'
Hotel__Lattitude = '//meta[@property="og:latitude"]//@content'
Hotel__Longitude = '//meta[@property="og:longitude"]//@content'


RoomType__name = '//span[@class="a1"]//text()'
RoomType__price = '//span[@class="a1"]//text()'
