
LP__hotelName = './/div[@id="searchEssentials"]//*[@class="noSifr"]/a/text()[1]'

Hotel__id = "//div[@data-prwidget-name='meta_h_text_links_simplified']/div[@data-provider and @data-pernight]/@data-locationid"
Hotel__name = "//h1[@id='HEADING']/text()"
Hotel__details1 = '//span[@class="date"]/text()'
Hotel__details2 = '//span[@class = "partyMix"]/text()'
Hotel__roomType = './h1/text()'
Hotel__containers = '//*[contains(@class,"rateContainer") and not(contains(@class, "noImage"))]/../..'
Hotel__priceblocks = './/*[contains(@class,"rateDetails") and @data-starpoints="0"]'
Hotel__promotion = '//div[@class="details"]//li[1]/text()'
Hotel__supplier = "//div[@data-prwidget-name='meta_h_text_links_simplified']/div[@data-provider and @data-pernight]/@data-provider"
Hotel__price = "//div[@data-prwidget-name='meta_h_text_links_simplified']/div[@data-provider and @data-pernight]/@data-pernight"
Hotel__tax = "//div[@data-prwidget-name='meta_h_text_links_simplified']/div/@data-taxesvalue"
Hotel__boardType = './/*[@class="details"]/h3/text()'
Hotel__address = "//span[@class='detail']/span/text()"
Hotel__starRating = "//div[@class='starRating detailListItem']//div[@data-element]/@class"
Hotel__Lattitude = '//meta[@property="og:latitude"]//@content'
Hotel__Longitude = '//meta[@property="og:longitude"]//@content'


RoomType__name = '//span[@class="a1"]//text()'
RoomType__price = '//span[@class="a1"]//text()'
