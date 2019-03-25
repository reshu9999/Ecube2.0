LP__hotelName = ''


Hotel__name = '//div[@id="detailsHead"]//h2//span[@class="title"]/text()'
Hotel__address = '//div[@class="contentTitle"]//div//address/text()'
Hotel__starRating = '//div[@class="contentTitle"]//span[not(text())]/@class'
Hotel__latitude = '//meta[contains(@property, "latitude")]/@content'
Hotel__longitude = '//meta[contains(@property, "longitude")]/@content'

RoomType__name = '//div[@class="textWrap "]//h4/text()'
RoomType__type = '//div[@class="textWrap "]//p/text()'
RoomType__price = '//div//h4[contains(@class,"price")]/text()'
RoomType__promotion = '//div[contains(@class,"textWrap")]//span[contains(@class,"hasTariff")]/@class'
RoomType__boardType = '//div//div[@class="supplements"]/text()'