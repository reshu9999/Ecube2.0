LP__hotelName = ''


Hotel__name = '//hotel/@name'
Hotel__address = '//ItemDetails//HotelInformation//AddressLines//child::text()'
Hotel__starRating = '//hotel/@categorycode'
Hotel__Lattitude = '//hotel/@latitude'
Hotel__Longitude = '//hotel/@longitude'
# Hotel__zonename = '//hotel/@zonename'
Hotel__hotelcode= '//hotel/@code'
Hotel__currency = '//hotel/@currency'
Hotel__contract = "./@ratekey"
Hotel__classification = "./@rateclass"

Hotel__elems = '//HotelDetails//Hotel'
Hotel__roomAvailability = "./@allotment" #to be used with price element
Hotel__roomCode = "./@code" #to be used with roomContainer
Hotel__opaque = "./@packaging"
Hotel__directPayment = "./@paymenttype" #to be used with price element
Hotel__commission = "./@commission" #to be used with price element

Hotel__netPrice = "./@net" #to be used with price element
Hotel__sellingPrice = "./@sellingrate" # to be used with price element
Hotel__cost = "./cost/@amount"

Roomtype__containers = "//rooms/room"
RoomType__type = './@name'
RoomType__priceblocks = './/rate'
RoomType__boardType = './@boardcode'
RoomType__price = './@net'
RoomType__currency = '//hotel/@Currency'
RoomType__promotion = './/promotion/@name'
RoomType__promotioncode = './/promotion/@code'

RoomType__category_id = '//RoomCategories//RoomCategory/@Id'
# Hotel__costTaxpercentincval = "./tax/@percent"
Hotel__costTaxpercentboolval = "./tax/@included"

# Hotel__costTaxamtincval = "./tax/@clientamount"
# Hotel__costTaxamtboolval = "./tax/@included"
# Hotel__costTaxamtcurrval = "./tax/@clientcurrency"

Hotel__promotions = "./promotions/promotion/@name"
Hotel__offers = "./offers/offer/@name"