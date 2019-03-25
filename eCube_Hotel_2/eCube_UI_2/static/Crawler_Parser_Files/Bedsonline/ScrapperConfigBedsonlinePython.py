visitHomePage = False
requestType = {
    'request': True,
    'driver': False
}


hotelCodesXpath = "//Table/nvcrWebSiteHotelId/text()"
# hotelCodesXpath = "//item/nvcrWebSiteHotelId/text()"
Hotel_chainXpath="//Table/nvcrHotelChain/text()"
shaSignatureXpath = "//textarea[@id='output']/text()"

hotelXpath = "//hotels/hotel"
hotelNameXpath = "./@name"
hotelCodeXpath = "./@code"
hotel_ZoneName = "//hotel/@destinationcode"

def getAPIKey(pos):
    if pos.upper() == "Argentina".upper():
        return "86955vnzqsmzdbsvmhe24b5n", "r5rhHfqWKa"
    if pos.upper() == "Australia".upper():
        return "ut3afy3c8upkzgqt7tvuk9yh", "yMRevTUJdE"
    if pos.upper() == "Colombia".upper():
        return "uc24fhjkskjbw723b7wm2tmc", "NPerPDvu7S"
    if pos.upper() == "Costa Rica".upper():
        return "x9ggt3yxkj7r5aadvhmppjc8", "2n6MQzAMbV"
    if pos.upper() == "France".upper():
        return "ek8q8zfphm9z8pntufbxw896", "szwK2xx2vU"
    if pos.upper() == "Germany".upper():
        return "nrqhbq4vhdq4s4uzmaskmcfk", "Gc6bSnhUEp"
    if pos.upper() == "Greece".upper():
        return "f6bzfr7gezmtdzrqfpf2hz7j", "9djqSDAzcU"
    if pos.upper() == "Hong Kong".upper():
        return "s86xpwrj8vrfcyfj4ect6k8v", "x7brMqtw4k"
    if pos.upper() == "India".upper():
        return "gmtqkjsr496au964zefkef8w", "eDRkmRxm5b"
    if pos.upper() == "Indonesia".upper():
        return "rvcgrj2wmz6dv9ms5n7gtz3f", "97HvnpxRN8"
    if pos.upper() == "Malaysia".upper():
        return "6nqm5wtxxbrb3d52dqradj6x", "9aGabwvS3j"
    if pos.upper() == "Mexico".upper():
        return "66ccq7tj7m9qj5n82zvkp9kh", "rBFXX8qJgM"
    if pos.upper() == "Portugal".upper():
        return "r6syk3guamkcvgvgnk36gmec", "yfsr4DfMhm"
    if pos.upper() == "Saudi Arabia".upper():
        return "jz3pyxt8zfqmcqcmaak8x3fn", "umSnGRKtpM"
    if pos.upper() == "Singapore".upper():
        return "dp2fhpqtrfamg94ef6jjtuwh", "5yaqPwsA2x"
    if pos.upper() == "South Korea".upper():
        return "uscvfuty5fdhamv4f6ngjmv3", "kKgzw8URck"
    if pos.upper() == "Spain".upper():
        return "z45pg9amr938ymxr7cztk77h", "2a4DaTCrWF"
    if pos.upper() == "Thailand".upper():
        return "yhhh28f5fyzzyewn2ynr878r", "nvAQBCvEBq"
    if pos.upper() == "United Kingdom".upper():
        return "x72mngycs2kuurg767dwdw6z", "Gm9hjsNEsv"
    if pos.upper() == "UNITED STATES - USA".upper():
        return "dtwdehg68czcvaxck5h4cqbh", "SyDbKFRb7C"

def getMasterCurrency(city, pos):
    if city.upper() == "Cairns - QLD".upper() and pos.upper() =="Australia".upper():
        return "AUD", "AU"
    if city.upper() == "Adelaide - SA".upper() and pos.upper() =="Spain".upper():
        return "EUR", "ES"
    if city.upper() == "The Hague".upper() and pos.upper() =="Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Beijing Peking".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Wroclaw".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Colmar".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Melbourne - VIC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Dusseldorf".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Cologne / Bonn".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "HAMBURG".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Lille".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Grenoble".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "North Coast - NSW".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Dortmund".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Stuttgart".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Hannover".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "NICE".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "CANNES".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Brisbane - QLD".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Brisbane - QLD".upper() and pos.upper() == "Australia".upper():
        return "EUR", "AU"
    if city.upper() == "Belo Horizonte".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "St Malo".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Deauville".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Auckland".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Auckland".upper() and pos.upper() == "Australia".upper():
        return "EUR", "AU"
    if city.upper() == "WARSAW".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "La Rochelle".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Pittsburgh - PA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "San Francisco Area -CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Richmond - VA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Charlotte - NC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Otago- Queenstown".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Otago- Queenstown".upper() and pos.upper() == "Australia".upper():
        return "EUR", "AU"
    if city.upper() == "Rio de Janeiro".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Birmingham - AL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Aix-en-Provence".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Nuremberg".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Basel".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Essen".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "BRISTOL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Rotterdam".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Leipzig".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Leeds".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sheffield".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Puglia".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Curitiba".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Dresden".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "French Alps".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Reims".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Savannah - GA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Adelaide - SA".upper() and pos.upper() == "United Kingdom".upper():
        return "AUD", "UK"
    if city.upper() == "Adelaide - SA".upper() and pos.upper() == "Australia".upper():
        return "AUD", "AU"
    if city.upper() == "New Orleans - LA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Fort Lauderdale - Hollywood Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Jacksonville Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "MALTA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MALTA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "MONTREAL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "BALI".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Jakarta".upper() and pos.upper() == "INDONESIA".upper():
        return "USD", "ID"
    if city.upper() == "BARCELONA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "FLORENCE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Costa Brava and Costa Barcelona-Maresme".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Rimini".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Bournemouth".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Montpellier".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "A Coruna".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "BELFAST".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "BALI".upper() and pos.upper() == "INDONESIA".upper():
        return "USD", "ID"
    if city.upper() == "MILAN".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Amsterdam and vicinity".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Beijing Peking".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Tours".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "CHIANG MAI".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "GENEVA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SEOUL".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Calgary".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Split-Middle Dalmatia".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Bangalore".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "San Francisco Area - CA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Dallas - TX".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Dallas - TX".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "HAMBURG".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Tel Aviv".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Myrtle Beach - SC".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Dusseldorf".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Dusseldorf".upper() and pos.upper() == "Spain".upper():
        return "GBP", "ES"
    if city.upper() == "Cologne / Bonn".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Cologne / Bonn".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "GENEVA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MANCHESTER".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MANCHESTER".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Lima".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Koh Samui".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Seattle - WA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Seattle - WA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Side".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MILAN".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "ISTANBUL".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Marmaris".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Stuttgart".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Grand Canyon National Park Area - AZ".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"


    if city.upper() == "Peloponesse".upper() and pos.upper() == "GREECE".upper():
        return "EUR", "GR"
    if city.upper() == "TORONTO".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "TORONTO".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Kyoto".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Kyoto".upper() and pos.upper() == "United Kingdom".upper():
        return "JPY", "UK"
    if city.upper() == "FRANKFURT".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "BERLIN".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MALAGA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Buenos Aires".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "ALGARVE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Hanoi and North".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "FUERTEVENTURA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Kedah / Langkawi".upper() and pos.upper() == "MALAYSIA".upper():
        return "MYR", "MY"
    if city.upper() == "Orlando Area - Florida - FL".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Portland - OR".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Hawaii - Maui - HI".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "BARCELONA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Washington D.C. - DC".upper() and pos.upper() == "United Kingdom".upper():
        return "USD", "UK"
    if city.upper() == "LANZAROTE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "LANZAROTE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "BODRUM".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "CRETE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Los Angeles - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Las Vegas - NV".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Rio de Janeiro".upper() and pos.upper() == "MEXICO".upper():
        return "USD", "MX"
    if city.upper() == "Rio de Janeiro".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "London".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "IBIZA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Denver - CO".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Denver - CO".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Delhi and NCR".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Delhi".upper() and "NCR".upper() and pos.upper() == "Spain".upper():
        return "GBP", "ES"
    if city.upper() == "GRAN CANARIA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "VIENNA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Hawaii - Oahu - HI".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "ANDORRA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Neapolitan Riviera".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "New Orleans - LA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Salzburg".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Palm Beach Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Bandung".upper() and pos.upper() == "INDONESIA".upper():
        return "USD", "ID"
    if city.upper() == "Majorca".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Houston - TX".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Houston - TX".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Salt Lake City - UT".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Salt Lake City - UT".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Buenos Aires".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Metro Manila".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Corsica".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "Maldives".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Zaragoza".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "MALAGA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Halkidiki".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Philadelphia - PA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Salou Area / Costa Dorada".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Santiago de Chile".upper() and pos.upper() == "MEXICO".upper():
        return "USD", "MX"
    if city.upper() == "Pyrenees - Catalan".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SEVILLE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "HONG KONG".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Lake Garda".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Sitges Area - Costa del Garraf".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Almeria Coast-Almeria".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Almeria Coast-Almeria".upper() and pos.upper() == "Spain".upper():
        return "GBP", "ES"
    if city.upper() == "Riviera Maya / Playa del Carmen".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Alicante - Costa Blanca".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Verona".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "TURIN".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Aberdeen".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MUNICH".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Chicago - IL".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Mexico City".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Golfe de Saint Tropez".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "PRAGUE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Dubrovnik-South Dalmatia".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Ankara".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Sydney - NSW".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Sydney - NSW".upper() and pos.upper() == "Australia".upper():
        return "AUD", "AU"
    if city.upper() == "Strasbourg".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "Mexico City".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "Amsterdam and vicinity".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Zurich".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "ASTURIAS".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "LISBON".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "TENERIFE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Sharm el Sheikh -Dahab".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Sharm el Sheikh -Dahab".upper() and pos.upper() == "GERMANY".upper():
        return "GBP", "DE"
    if city.upper() == "Stockholm".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Mumbai".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MADRID".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "FRANKFURT".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "FRANKFURT".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Halkidiki".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MARSEILLE".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "FUERTEVENTURA".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Blackpool".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "London".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Buenos Aires".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Buenos Aires".upper() and pos.upper() == "Argentina".upper():
        return "GBP", "AR"
    if city.upper() == "Merida - Yucatan".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "Phoenix Area - AZ".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Phoenix Area - AZ".upper() and pos.upper() == "Spain".upper():
        return "USD", "ES"
    if city.upper() == "Abu Dhabi".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Abu Dhabi".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Hammamet".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Hammamet".upper() and pos.upper() == "Germany".upper():
        return "GBP", "DE"
    if city.upper() == "San Diego - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Estoril Coast".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "CORFU".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Washington D.C. - DC".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Washington D.C. - DC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Los Cabos".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "Majorca".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Porto and North of Portugal".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Vizcaya - Bilbao".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Boston - MA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "ALGARVE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Naples".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MENORCA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Scottsdale - AZ".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "WARSAW".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Biarritz".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SANTORINI".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "SANTORINI".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "PRAGUE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "RIGA".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Atlanta - GA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Atlanta - GA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "FLORENCE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "BERLIN".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "AGADIR".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MARRAKECH".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "GRANADA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SINGAPORE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Avignon".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Kusadasi".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Zurich".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Fort Myers Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "LYON".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "LYON".upper() and pos.upper() == "France".upper():
        return "EUR", "FR"
    if city.upper() == "Baltimore - MD".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Edinburgh".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Taipei".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "TAIPEI".upper() and pos.upper() == "HONG KONG".upper():
        return "USD", "HK"
    if city.upper() == "Boston - MA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Bogota".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Central Guanacaste Liberia".upper() and pos.upper() == "COSTA  RICA".upper():
        return "USD", "CR"
    if city.upper() == "Dublin".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Newcastle-upon-Tyne".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Costa De La Luz (Cadiz)".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Salvador de la Bahia".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "San Jose - Silicon Valley - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "MADRID".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Nassau".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Ho Chi Minh City (Saigon) and South".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Santiago de Chile".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Antalya".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "COSTA DEL SOL".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "BERLIN".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Medellin".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "New York Area - NY".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Pattaya-Chonburi".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Brussels".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Pyrenees - Aragon".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "San Antonio - TX".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "San Antonio - TX".upper() and pos.upper() == "Spain".upper():
        return "USD", "US"
    if city.upper() == "Cancun (and vicinity)".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "MOSCOW".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MOSCOW".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sofia".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "California Coast - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "BUCHAREST".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "W. Cape-Cape Town-Garden Route".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "SAO PAULO".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Benidorm - Costa Blanca".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SEVILLE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Cadiz / Jerez".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Kos".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Doha".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "San Jose / Central Valley".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "RHODES".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Hua Hin-Cha Am-Pranburi".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Cancun (and vicinity)".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Aruba".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Kusadasi".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Santiago de Chile".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Centre Portugal".upper() and pos.upper() == "PORTUGAL".upper():
        return "EUR", "PT"
    if city.upper() == "Centre Portugal".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "BUDAPEST".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Barbados".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Navarra".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "GRAN CANARIA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Venice (and vicinity)".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Venice (and vicinity)".upper() and pos.upper() == "Spain".upper():
        return "GBP", "ES"
    if city.upper() == "Alanya".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "RIGA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Amsterdam and vicinity".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Thessaloniki".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Istria".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Chicago - IL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Chicago - IL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "DUBAI".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "DUBAI".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "BOLOGNA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Skiathos".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "AGADIR".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Guangzhou".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Guangzhou".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "PUNTA CANA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "PHUKET".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "ACAPULCO".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "Majorca".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Nashville - TN".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Lago de Garda".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Porto and North of Portugal".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Istria".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "TOULOUSE".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "Alentejo".upper() and pos.upper() == "PORTUGAL".upper():
        return "EUR", "PT"
    if city.upper() == "Alentejo".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Kedah / Langkawi".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Lake Garda".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "SAO PAULO".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "VALENCIA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "San Francisco Area - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Dublin".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Pontevedra".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Belek".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "IBIZA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Lourdes".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Clearwater Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Krabi".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Palm Springs - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "MARRAKECH".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "St Petersburg".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "COSTA DE ALMERIA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Memphis - TN".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Minneapolis - MN".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Riviera Maya / Playa del Carmen".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Benidorm - Costa Blanca".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Paris".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Gdansk".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Edinburgh".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Siem Reap - North".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Casablanca".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "KRAKOW".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Panama City".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Tokyo".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "COSTA DEL SOL".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Los Angeles - CA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Riviera Maya / Playa del Carmen".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "Varna / Black Sea Resorts".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Cancun (and vicinity)".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "BUDAPEST".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Orlando Area - Florida - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Orlando Area - Florida - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "COSTA DE AZAHAR".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "TENERIFE".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Central and North Greece".upper() and pos.upper() == "GREECE".upper():
        return "EUR", "GR"
    if city.upper() == "ROME".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "ROME".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Cantabria".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Belek".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Fez".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "Costa Brava and Costa Barcelona-Maresme".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "GRANADA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "ATHENS".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Bordeaux".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "MYKONOS".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Oslo".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "PUNTA CANA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "New York Area - NY".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SINGAPORE".upper() and pos.upper() == "INDONESIA".upper():
        return "USD", "ID"
    if city.upper() == "SINGAPORE".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Ixtapa - Zihuatanejo".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "PUERTO VALLARTA".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "ISTANBUL".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MUNICH".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Tampa - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "FUERTEVENTURA".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Nantes".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "Miami Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Paris".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Paris".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "BANGKOK".upper() and pos.upper() == "United Kingdom".upper():
        return "THB", "UK"
    if city.upper() == "Estoril Coast".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Costa De La Luz (Huelva)".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "North Sardinia".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Austin - TX".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Austin - TX".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Gauteng- Johannesburg".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Gauteng- Johannesburg".upper() and pos.upper() == "Spain".upper():
        return "GBP", "ES"
    if city.upper() == "North Sardinia".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Helsinki".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Penang".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Penang".upper() and pos.upper() == "INDONESIA".upper():
        return "USD", "ID"
    if city.upper() == "Zante".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "NICE".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Cordoba".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Montego Bay".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Guadalajara and Vicinity".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "New York Area - NY".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Melbourne - VIC".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Melbourne - VIC".upper() and pos.upper() == "Australia".upper():
        return "AUD", "AU"
    if city.upper() == "Melbourne - VIC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Las Vegas - NV".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "KUALA LUMPUR".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "ATHENS".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "SHANGHAI".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "SHANGHAI".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Monterrey".upper() and pos.upper() == "MEXICO".upper():
        return "MXN", "MX"
    if city.upper() == "Monterrey".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Oslo".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "VIENNA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "California Wine Country - CA".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Vancouver".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Azores".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Azores".upper() and pos.upper() == "PORTUGAL".upper():
        return "EUR", "PT"
    if city.upper() == "Los Cabos".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "MUNICH".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Salou Area / Costa Dorada".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "LISBON".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "TENERIFE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "COPENHAGEN".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "TALLINN".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Hawaii - Oahu - HI".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "KRAKOW".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Charleston - SC".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Riviera Maya / Playa del Carmen".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "COPENHAGEN".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "GLASGOW".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Genoa".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "GRAN CANARIA".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Amman".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "Bahrain".upper() and pos.upper() == "SAUDI ARABIA".upper():
        return "EUR", "SA"

    return mastercurrency1(city,pos)



def mastercurrency1(city, pos):

    if city.upper() == "Perth - WA".upper() and pos.upper() == "AUSTRALIA".upper():
        return "AUD", "AU"
    if city.upper() == "Austrian Alps".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Cairo".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Cairo".upper() and pos.upper() == "Germany".upper():
        return "EUR", "DE"
    if city.upper() == "Djerba".upper() and pos.upper() == "FRANCE".upper():
        return "EUR", "FR"
    if city.upper() == "Djerba".upper() and pos.upper() == "GERMANY".upper():
        return "EUR", "DE"
    if city.upper() == "Cannes".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Daytona Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Sicily".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Side".upper() and pos.upper() == "Germany".upper():
        return "EUR", "DE"
    if city.upper() == "Memphis - TN".upper() and pos.upper() == "United Kingdom".upper():
        return "USD", "UK"
    if city.upper() == "Siena".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Osaka".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Cocoa Area - FL".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Canadian Rockies".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Niagara Falls".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Ottawa".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Quebec".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Vancouver Island".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Zion National Park - UT".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "USD", "US"
    if city.upper() == "Pacific North Coast / Guanacaste".upper() and pos.upper() == "COSTA RICA".upper():
        return "USD", "CR"
    if city.upper() == "MADEIRA".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "MENORCA".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Djerba".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "MARSEILLE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Corsica".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Bordeaux".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Central and North Greece".upper() and pos.upper() == "United Kingdom".upper():
        return "GBP", "UK"
    if city.upper() == "MARSEILLE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Nantes".upper() and pos.upper() == "spain".upper():
        return "EUR", "ES"
    if city.upper() == "Montpellier".upper() and pos.upper() == "spain".upper():
        return "EUR", "ES"
    if city.upper() == "Peloponesse".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Strasbourg".upper() and pos.upper() == "spain".upper():
        return "EUR", "ES"
    if city.upper() == "TOULOUSE".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Golfe de Saint Tropez".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
    if city.upper() == "Jakarta".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "BANGKOK".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sydney - NSW".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Los Angeles - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Jeddah".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Madinah".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Riyadh".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Makkah".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Gold Coast - QLD".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Gold Coast - QLD".upper() and pos.upper() == "Australia".upper():
        return "EUR", "AU"
    if city.upper() == "Albuquerque - NM".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Baltimore - MD".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Memphis - TN".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Colorado Springs - CO".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Oklahoma City - OK".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Tulsa - OK".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Fukuoka".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Buffalo - NY".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Detroit - MI".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "California Wine Country - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Fort Myers Area - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sanya".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Charlotte - NC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Richmond - VA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "San Francisco Area - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Louisville - KY".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Fort Worth - TX".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Savannah - GA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Muscat".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "San Jose - Silicon Valley - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Raleigh/Durham - NC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Minneapolis - MN".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Nashville - TN".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sacramento - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Charleston - SC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Hua Hin-Cha Am-Pranburi".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Bali".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Bali".upper() and pos.upper() == "Australia".upper():
        return "AUD", "AU"
    if city.upper() == "Calgary".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Great Smokies - NC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Hong Kong".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Bandung".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Las Vegas - NV".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Kansas City - MO".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Portland - OR".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Cincinnati - OH".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Philadelphia - PA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Columbus - OH".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Baton Rouge - LA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Berlin".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Miami Area - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Charleston - SC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "San Diego - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Cleveland - OH".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Shenzhen".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Boston - MA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Milwaukee - WI".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Puerto Rico Island".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Puerto Rico Island".upper() and pos.upper() == "UNITED STATES - USA".upper():
        return "EUR", "US"
    if city.upper() == "California Coast - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Tokyo".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Delaware - DE".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Ontario - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Reno - NV".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Okinawa".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Thessaloniki".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Oakland - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "MONTREAL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Kansas City - MO".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "TORONTO".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "SEOUL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Jacksonville Area - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Salzburg".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Vancouver".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Taipei".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Tucson - AZ".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Edmonton".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Macau".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Virginia Beach - VA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Indianapolis - IN".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "KUALA LUMPUR".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Raleigh/Durham - NC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Tampa - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Palm Springs - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Mauritius Islands".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Zagreb".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Birmingham".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Cardiff".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Cairns - QLD".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Gdansk".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "LIVERPOOL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Perth - WA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Tropical North Coast - QLD".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Chennai (Madras)".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sochi".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Reading".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sunshine Coast - QLD".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Bruges".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Antwerp".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Luxembourg".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Coventry".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Salvador da Bahia - Costa Do Sauipe".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Mumbai".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Pune".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "GLASGOW".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Zanzibar".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "St Louis - MO".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Lake Tahoe - CA/NV".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Corpus Christi - TX".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Belgrade".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Nassau".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Kuantan and Pahang".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Greensboro - NC".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Sarasota Area - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Bratislava".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Fort Lauderdale - Hollywood Area - FL".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "San Francisco Area - CA".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Neapolitan Riviera".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Sicily".upper() and pos.upper() == "United Kingdom".upper():
        return "EUR", "UK"
    if city.upper() == "Swiss Alps".upper() and pos.upper() == "Spain".upper():
        return "EUR", "ES"
    if city.upper() == "Vancouver Island".upper() and pos.upper() == "SPAIN".upper():
        return "EUR", "ES"
