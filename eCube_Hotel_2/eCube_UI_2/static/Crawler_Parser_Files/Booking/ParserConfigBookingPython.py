
maintable= '//div[@id="hotellist_inner"]'
sublist='//div[@id="hotellist_inner"]//div[contains(@class,"sr_item_content")]'

Hotel__name = '//h3[contains(@class,"sr-hotel__title")]//span[contains(@class,"sr-hotel__name")]/text()'
Hotel__starRating='//i[contains(@class,"star_track")]/span[contains(@class,"invisible")]/text()'

# Hotel__roomType = "//td[@class='roomName']/div/span[@class='room_link']"
Hotel__roomType="//td[@class='roomName']/div/span[@class='room_link']/text()[1]"
##Breakfast included

RoomType_details="//sup[@class='sr_room_reinforcement'][contains(text(),'Breakfast included')]/text()"
RoomType__directpay = '//sup[@class="sr_room_reinforcement"][contains(text(),"No prepayment needed")]/text()'

Hotel__price = '//td[contains(@class,"roomPrice  sr_discount")]//strong[contains(@class,"price")]/b/text()'
Hotel__currency = '//input[@name="selected_currency"]/@value'


Hotel__Lattitude = '//*[@type="application/ld+json"]/text()'
Hotel__Longitude = '//*[contains(@property, "longitude")]/@content'
Hotel__MaxAdults = './/*[contains(@class, "occupancy")]//*[@class="invisible_spoken"]/text()'
Hotel__Id = '//input[@name="hotel_id"]/@value'


currpath='//input[@name="selected_currency"]/@value'