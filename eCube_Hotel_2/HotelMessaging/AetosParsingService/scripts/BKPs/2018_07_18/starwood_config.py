LP__hotelName = './/div[@id="searchEssentials"]//*[@class="noSifr"]/a/text()[1]'

Hotel__name = '//span[@class="propertyName"]/a/text()[1]'
# Hotel__name = '//span[@class="propertyName"]//a//text()'
Hotel__details1 = '//span[@class="date"]/text()'
Hotel__details2 = '//span[@class = "partyMix"]/text()'
Hotel__roomType = '//div[contains(@class, "roomContainer")]//h1/text()'
Hotel__promotion = '//div[@class="details"]//text()'
Hotel__price = './/span[@class="reserveLink"]/span[@class="roomTotal"]/text() | .//span[@class="reserveLink"]/span[@class="roomRate"]/text()'
Hotel__boardType = '//div[@class = "rateDetails "][1]//div[@class = "details"]//text()'
Hotel__address = '//ul[@id="propertyAddress"]/li//text()'
Hotel__starRating = '//span[@class="ratingContainer"]/span[1]//text()'
Hotel__LattitudeNLongitude = '//meta[@property="og:latitude"]//@content'


RoomType__name = '//span[@class="a1"]//text()'
RoomType__price = '//span[@class="a1"]//text()'