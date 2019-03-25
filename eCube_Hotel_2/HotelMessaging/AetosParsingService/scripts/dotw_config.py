LP__hotelName = ''


Hotel__address = '//address//strong/text()'
Hotel__latitude = '//div[@class="result_icons_container"][1]/p[2]/a/@data-lat'
Hotel__longitude = '//div[@class="result_icons_container"][1]/p[2]/a/@data-lng'

RoomType__type = '//div[@class="search-details-container"]//div[@class="rooms-details"]//div[contains(@class,"rdRow")]//div[@class="roomTypeText"]/text()'
RoomType__boardType = '//div[@class="search-details-container"]//div[@class="rooms-details"]//div[contains(@class,"rdRow")]//div[@class="boardBasis"]//span/text()'
RoomType__price = '//div[@class="search-details-container"]//div[@class="rooms-details"]//div[contains(@class,"rdRow hidden") or @class="rdRow"]'
RoomType__board = '//div[@class="rooms-details"]//div[contains(@class,"rdRow")]//div[@class="boardBasis"]'
RoomType__promotion = '//input[@name="promotionsJson"]/@value'
RoomType__currency = '//div[@class="search-details-container"]//div[@class="rooms-details"]//div[contains(@class,"rdRow hidden") or @class="rdRow"]'
