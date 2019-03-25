LP__hotelName = ''


Hotel__name = '//ItemDetails//Item/text()'
Hotel__address = '//ItemDetails//HotelInformation//AddressLines//child::text()'
Hotel__starRating = '//ItemDetails//HotelInformation//StarRating//text()'
Hotel__latitude = '//ItemDetails//HotelInformation//GeoCodes//Latitude/text()'
Hotel__longitude = '//ItemDetails//HotelInformation//GeoCodes//Longitude/text()'


Hotel__elems = '//HotelDetails//Hotel'


RoomType__type = '//RoomCategory//Description/text()'
RoomType__boardType = '//RoomCategory//Meals//Basis/@Code'
RoomType__price = '//RoomCategory//ItemPrice/text()'
RoomType__currency = '//RoomCategory//ItemPrice/@Currency'
RoomType__promotion = '//RoomCategory//ItemPrice'


RoomType__category_id = '//RoomCategories//RoomCategory/@Id'
