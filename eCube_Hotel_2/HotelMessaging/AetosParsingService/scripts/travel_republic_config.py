LP__hotelName = ''


Hotel__name = '//h1[@class="new-hotel-name"]/text()'
Hotel__address = '//div[@class="hotel-address"]/text()'
Hotel__starRating = '//div[@class="hotel-star-holder"]//span[not(@class)]/text()'
Hotel__latitude = '//script'
Hotel__longitude = '//script'
Hotel__supplier = '\w*Supplier\w*[:\s"a-zA-Z",]'


RoomType__type = '//td[not(@class)][1]//div[1]/text()'
RoomType__boardType = '//td[not(@class)][1]//div[@class="board-type-desc"]/text()'
RoomType__price = '//td[@class="column-cost"]//span[@class="hotel-room-cost"]/text()'
RoomType__payment = '//td[@class="column-center"]'
RoomType__payAtHotel = '//div[@class="payAtHotelIcon"]'
RoomType__promotion = '//td[not(@class)][1]//div[@class="board-type-desc"]//div[@class="room-info-links"]'
