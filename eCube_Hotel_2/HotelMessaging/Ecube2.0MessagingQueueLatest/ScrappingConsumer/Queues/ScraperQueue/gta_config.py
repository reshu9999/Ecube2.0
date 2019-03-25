# getData() function : xpaths

# REQUIRED
visitHomePage = True
requestType = {
    'request': True,
    'driver': True,
}


hotelLinksXpath = '//ResponseDetails//SearchHotelPricePaxResponse//HotelDetails//Hotel'


hotelCodeXpath = '//Item/@Code'
hotelCityCodeXpath = '//City/@Code'
hotelNameXpath = '//Item/text()'


roomDetailsInContainersXpath = '//PaxRoomSearchResults//PaxRoom//RoomCategories'
pricesInContainersXpath = '//PaxRoomSearchResults//PaxRoom//RoomCategories'
roomBoardType = '//PaxRoomSearchResults//PaxRoom//RoomCategories'
paymentType = '//PaxRoomSearchResults//PaxRoom//RoomCategories'
promotionType = '//PaxRoomSearchResults//PaxRoom//RoomCategories'


request_listener_url = 'https://rs.gta-travel.com/wbsapi/RequestListenerServlet'
hotel_url = 'https://rs.gta-travel.com/wbsapi/RequestListenerServlet'