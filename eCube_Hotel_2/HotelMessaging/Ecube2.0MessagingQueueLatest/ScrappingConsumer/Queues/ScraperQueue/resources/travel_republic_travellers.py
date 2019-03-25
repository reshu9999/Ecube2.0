travellers_data_dict = {
    1: {
        "adults": 1,
        "children": 0,
        "childAges": [],
    },
    2: {
        "adults": 2,
        "children": 0,
        "childAges": [],
    },
    3: {
        "adults": 2,
        "children": 1,
        "childAges": [6,],
    },
    4: {
        "adults": 2,
        "children": 2,
        "childAges": [6,8],
    }
}

city_multi_code = {
    'ABERDEEN': 2,
    'ALANYA': 8,
    'ANTALYA': 18,
    'AUSTRIAN ALPS': 4,
    'AZORES': 8,
    'BARCELONA': 2,
    'BENIDORM - COSTA BLANCA': 3,
    'BERLIN': 2,
    'BOURNEMOUTH': 3,
    'BRISTOL': 2,
    'BRUSSELS': 2,
    'CHANNEL ISLANDS': 2,
    'COPENHAGEN': 2,
    'COSTA BRAVA AND COSTA BARCELONA-MARESME': 5,
    'COSTA DE LA LUZ (CADIZ)': 2,
    'COSTA DE LA LUZ (HUELVA)': 9,
    'DUBLIN': 6,
    'DUSSELDORF': 5,
    'EDINBURGH': 5,
    'ESTORIL COAST': 3,
    'FRANKFURT': 5,
    'FRENCH ALPS': 8,
    'GLASGOW': 4,
    'HELSINKI': 2,
    'HURGHADA': 2,
    'KUSADASI': 2,
    'LAKE GARDA': 2,
    'LAS VEGAS - NV': 3,
    'LEEDS': 3,
    'LIVERPOOL': 3,
    'LONDON': 5,
    'LOS ANGELES - CA': 13,
    'MANCHESTER': 4,
    'MARRAKECH': 2,
    'MUNICH': 4,
    'NEAPOLITAN RIVIERA': 4,
    'NEW YORK AREA - NY': 18,
    'NEWCASTLE-UPON-TYNE': 2,
    'NICE': 2,
    'ORLANDO AREA - FLORIDA - FL': 2,
    'PARIS': 2,
    'PORTO AND NORTH OF PORTUGAL': 2,
    'PYRENEES - CATALAN': 3,
    'SALOU AREA / COSTA DORADA': 9,
    'SAN FRANCISCO AREA - CA': 6,
    'SIDE': 8,
    'SITGES AREA - COSTA DEL GARRAF': 2,
    'SPLIT-MIDDLE DALMATIA': 2,
    'VALENCIA': 3,
    'VARNA / BLACK SEA RESORTS': 2,
    'W. CAPE-CAPE TOWN-GARDEN ROUTE': 2,
    'WASHINGTON D.C. - DC': 4
}

city_mapping = {
    "TOKYO": "Tokyo, Japan",
    "RIVIERA MAYA / PLAYA DEL CARMEN": "Riviera Maya, Mexico",
    "BANGKOK": "Bangkok, Thailand",
    "ALICANTE - COSTA BLANCA": "Costa Blanca, Spain",
    "ISTANBUL": "Istanbul, Turkey",
    "AGADIR": "Agadir, Morocco",
    "MENORCA": "Menorca, Spain",
    "PRAGUE": "Prague, Czech Republic",
    "GRAN CANARIA": "Gran Canaria, Spain",
    "SALOU AREA / COSTA DORADA": {
        1: "Costa Dorada, Spain",
        2: "l'Espluga de Francolí, Tarragona, Spain",
        3: "Falset, Tarragona, Spain",
        4: "La Selva del Camp, Tarragona, Spain",
        5: "Montbrio del Camp, Tarragona, Spain",
        6: "Pratdip, Tarragona, Spain",
        7: "Reus, Tarragona, Spain",
        8: "Tortosa, Tarragona, Spain",
        9: "Valls, Tarragona, Spain"
    },
    "SINGAPORE": "Singapore, Singapore",
    "RIO DE JANEIRO": "Rio de Janeiro, Brazil",
    "SYDNEY - NSW": "Sydney, New South Wales, Australia",
    "HELSINKI": {
        1: "Helsinki, Finland",
        2: "Vantaa, Finland"
    },
    "BURGOS": "Burgos, Spain",
    "MUMBAI": "Mumbai, Maharashtra, India",
    "SIERRA NEVADA": "Sierra Nevada, Granada, Spain",
    "COPENHAGEN": {
        1: "Copenhagen Capital Region, Denmark",
        2: "Roskilde, Zealand Sjaelland, Denmark"
    },
    "BUDAPEST": "Budapest, Hungary",
    "CORDOBA": "Cordoba, Spain",
    "ZANZIBAR": "Zanzibar, Tanzania",
    "CRETE": "Crete, Greece",
    "BARBADOS": "Barbados, Barbados",
    "FRENCH ALPS": {
        1: "Haute-Savoie, France",
        2: "Hautes-Alpes, France",
        3: "Alpes-de-Haute-Provence, France",
        4: "Savoie, France",
        5: "Isere, France",
        6: "La Lechere, France",
        7: "Auron, Cote d'Azur, France",
        8: "Isola 2000, Cote d'Azur, France"
    },
    "PORTO AND NORTH OF PORTUGAL": {
        1: "Northern Portugal, Portugal",
        2: "Porto, Portugal",
        3: "Mondim De Basto, Northern Portugal, Portugal",
        4: "Chaves, Northern Portugal, Portugal",
        5: "Canicada, Northern Portugal, Portugal"
    },
    "GUANGHZHOU": "Guangzhou, China",
    "MARRAKECH": {
        1: "Marrakech, Morocco",
        2: "Ouirgane, High Atlas, Morocco"
    },
    "NEW ORLEANS - LA": "New Orleans, Louisiana, USA",
    "GENEVA": "Geneva, Switzerland",
    "CORFU": "Corfu, Greece",
    "THESSALONIKI": "Thessalonika, Greece",
    "ZANTE": "Zante (Zakinthos), Greece",
    "VALLADOLID": "Valladolid, Spain",
    "SAN JOSE / CENTRAL VALLEY": "San Jose  Central Valley, Costa Rica",
    "LYON": "Lyon, Rhône, France",
    "STOCKHOLM": "Stockholm, Sweden",
    "SANTORINI": "Santorini, Greece",
    "LEEDS": {
        1: "Leeds, West Yorkshire, United Kingdom",
        2: "Ilkley, West Yorkshire, United Kingdom",
        3: "Harrogate, North Yorkshire, United Kingdom"
    },
    "PYRENEES - CATALAN": {
        1: "Pyrenees - Catalan, Spain",
        2: "Lles De Cerdanya, Lleida, Spain",
        3: "Seva, Barcelona, Spain"
    },
    "WASHINGTON D.C. - DC": {
        1: "Woodbridge, Virginia, USA",
        2: "Bethesda, Maryland, USA",
        3: "Takoma Park, Maryland, USA",
        4: "Washington, D.C., USA"
    },
    "DELHI AND NCR": "Delhi, India",
    "EDINBURGH": {
        1: "Edinburgh, United Kingdom",
        2: "Falkirk, United Kingdom",
        3: "West Lothian, United Kingdom",
        4: "Musselburgh, Edinburgh, United Kingdom",
        5: "East Lothian, United Kingdom"
    },
    "BOGOTA": "Bogota, Colombia",
    "DOHA": "Doha, Qatar",
    "JAEN": "Jaen, Spain",
    "TOLEDO": "Toledo, Spain",
    "LONDON": {
        1: "London, United Kingdom",
        2: "Basildon, Essex, United Kingdom",
        3: "Gatwick Airport (LGW), London, United Kingdom",
        4: "Luton Airport, Luton Airport, United Kingdom",
        5: "Stansted Airport (STN), London, United Kingdom"
    },
    "CHIANG MAI": "Chiang Mai, Thailand",
    "NEAPOLITAN RIVIERA": {
        1: "Amalfi Coast, Italy",
        2: "Ischia, Campania, Italy",
        3: "Positano, Amalfi Coast, Italy",
        4: "Sorrento Coast, Italy"
    },
    "LOS ANGELES - CA": {
        1: "Los Angeles, California, USA",
        2: "Capo Beach, California, USA",
        3: "Beverly Hills, California, USA",
        4: "Fillmore, California, USA",
        5: "Irvine, California, USA",
        6: "Murrieta, California, USA",
        7: "Oxnard, California, USA",
        8: "San Gabriel, California, USA",
        9: "Valencia, California, USA",
        10: "Simi Valley, California, USA",
        11: "Thousand Oaks, California, USA",
        12: "Van Nuys, California, USA",
        13: "Reseda, California, USA"
    },
    "COUNTY CORK": "Cork, Ireland",
    "KEMER": "Kemer Antalya, Antalya, Turkey",
    "SALVADOR DA BAHIA - COSTA DO SAUIPE": "Salvador de la Bahia - Costa Do Sauipe, Brazil",
    "MADRID": "Madrid, Spain",
    "ESTORIL COAST": {
        1: "Estoril Coast, Portugal",
        2: "Ericeira, Lisbon, Portugal",
        3: "Oeiras, Lisbon, Portugal"
    },
    "KUALA LUMPUR": "Kuala Lumpur, Malaysia",
    "ABERDEEN": {
        1: "Aberdeen, United Kingdom",
        2: "Aberdeenshire, United Kingdom"
    },
    "JAKARTA": "Jakarta, Java, Indonesia",
    "SIDE": {
        1: "Cenger, Antalya, Turkey",
        2: "Side, Antalya, Turkey",
        3: "Kizilagac, Antalya, Turkey",
        4: "Manavgat, Antalya, Turkey",
        5: "Colakli, Antalya, Turkey",
        6: "Titreyengöl, Antalya, Turkey",
        7: "Orensehir, Antalya, Turkey",
        8: "Kumkoy, Antalya, Turkey"
    },
    "CAPPADOCIA": "Central Anatolia Region, Turkey",
    "KUSADASI": {
        1: "Kusadasi, Turkey",
        2: "Izmir, Turkey"
    },
    "MIAMI AREA - FL": "Miami, Florida, USA",
    "BIRMINGHAM": "Birmingham, West Midlands, United Kingdom",
    "NEW YORK AREA - NY": {
        1: "New York City, USA",
        2: "Brooklyn, New York State, USA",
        3: "Hasbrouck Heights, New Jersey, USA",
        4: "Westbury, New York State, USA",
        5: "Queens, New York State, USA",
        6: "Ozone Park, New York City, USA",
        7: "Astoria, New York City, USA",
        8: "Farmingville, New York State, USA",
        9: "East Hampton, New York State, USA",
        10: "Rockville Centre, New York State, USA",
        11: "Westbury, New York State, USA",
        12: "Kingston, New York State, USA",
        13: "Long Island City, New York State, USA",
        14: "Nanuet, New York State, USA",
        15: "Harrison, New Jersey, USA",
        16: "Kenilworth, New Jersey, USA",
        17: "Clifton, New Jersey, USA",
        18: "Staten Island, New York City, USA"
    },
    "ALMERIA COAST-ALMERIA": "Almeria Coast, Spain",
    "IXTAPA - ZIHUATANEJO": "Ixtapa, Mexico",
    "COSTA DEL SOL": "Costa del Sol, Spain",
    "LIMA": "Lima, Peru",
    "BRISTOL": {
        1: "Bristol Airport, Bristol, United Kingdom",
        2: "Bristol, United Kingdom"
    },
    "HAMMAMET": "Hammamet, Tunisia",
    "BRUSSELS": {
        1: "Brussels, Belgium",
        2: "Wavre, Wallonia, Belgium"
    },
    "SEOUL": "Seoul, South Korea",
    "BOSTON - MA": "Boston, Massachusetts, USA",
    "ISTRIA": "Istria, Croatia",
    "MACAU": "Macau, Macau",
    "SAO PAULO": "Sao Paulo, Brazil",
    "SPLIT-MIDDLE DALMATIA": {
        1: "Split / Dalmatian Riviera, Croatia",
        2: "Drvenik, Dubrovnik Riviera, Croatia"
    },
    "DUBAI": "Dubai, United Arab Emirates",
    "SHARM EL SHEIKH -DAHAB": "Sharm el Sheikh, Egypt",
    "COSTA DE LA LUZ (CADIZ)": "CAD",
    "ROME": "Rome (Province), Italy",
    "TAIPEI": "Taipei, Taiwan",
    "ALGARVE": "Algarve, Portugal",
    "PUNTA CANA": "Punta Cana, Dominican Republic",
    "GAUTENG- JOHANNESBURG": "Gauteng, South Africa",
    "DUSSELDORF": {
        1: "Hagen, North Rhine-Westphalia, Germany",
        2: "Krefeld, North Rhine-Westphalia, Germany",
        3: "Remscheid, North Rhine-Westphalia, Germany",
        4: "Mönchengladbach, North Rhine-Westphalia, Germany",
        5: "Düsseldorf, North Rhine-Westphalia, Germany"
    },
    "NAIROBI": "Nairobi, Kenya",
    "SANTIAGO DE CHILE": "Santiago de Chile, Chile",
    "MARMARIS": "Dalaman, Turkey",
    "LANZAROTE": "Lanzarote, Spain",
    "MONTEVIDEO": "Montevideo, Uruguay",
    "CANNES": "Cannes, Côte d'Azur, France",
    "SKIATHOS": "Skiathos, Greece",
    "MADEIRA": "Madeira, Portugal",
    "ANDORRA": "Andorra, Andorra",
    "COSTA DE LA LUZ (HUELVA)": "Costa de la Luz, Spain",
    "BENIDORM - COSTA BLANCA": {
        1: "Benidorm, Costa Blanca, Spain",
        2: "El Albir, Costa Blanca, Spain",
        3: "Cala Finestrat, Costa Blanca, Spain"
    },
    "SOFIA": "Sofía, Bulgaria",
    "LAS VEGAS - NV": {
        1: "Henderson, Nevada, USA",
        2: "Boulder City, Nevada, USA",
        3: "Las Vegas, USA"
    },
    "TENERIFE": "Tenerife, Spain",
    "GIRONA": "Girona, Spain",
    "MOSCOW": "Moscow, Russia",
    "KEFALONIA": "Kefalonia, Greece",
    "IBIZA": "Ibiza, Spain",
    "IZMIR": "Izmir, Turkey",
    "MANCHESTER": {
        1: "Manchester, United Kingdom",
        2: "Warrington, Cheshire, United Kingdom",
        3: "Buxton, Cheshire, United Kingdom",
        4: "Burnley, Lancashire, United Kingdom"
    },
    "MAURITIUS ISLANDS": "Mauritius",
    "BLACKPOOL": "Blackpool, Lancashire, United Kingdom",
    "TALLINN": "Tallinn, Estonia",
    "FLORENCE": "Florence Province, Italy",
    "SALAMANCA": "Salamanca, Spain",
    "KOS": "Kos, Greece",
    "HAVANA": "Havana, Cuba",
    "PARIS": {
        1: "Paris, France",
        2: "Pantin, Paris, France"
    },
    "LISBON": "Province of Lisbon, Portugal",
    "COUNTY GALWAY": "Galway, Ireland",
    "CHANNEL ISLANDS": {
        1: "Jersey, United Kingdom",
        2: "Guernsey, United Kingdom"
    },
    "SAN FRANCISCO AREA - CA": {
        1: "San Francisco, California, USA",
        2: "Brentwood, California, USA",
        3: "Corte Madera, California, USA",
        4: "Novato, California, USA",
        5: "San Mateo, California, USA",
        6: "Vallejo, California, USA"
    },
    "AZORES": {
        1: "Terceira, The Azores, Portugal",
        2: "Pico, The Azores, Portugal",
        3: "Faial, The Azores, Portugal",
        4: "Santa Maria, The Azores, Portugal",
        5: "Graciosa, The Azores, Portugal",
        6: "Sao Jorge, The Azores, Portugal",
        7: "Flores, The Azores, Portugal",
        8: "Sao Miguel, The Azores, Portugal"
    },
    "WARSAW": "Warsaw, Poland",
    "BODRUM": "Bodrum, Turkey",
    "NAPLES": "Campania, Italy",
    "HAWAII - OAHU - HI": "Hawaii, USA",
    "PHUKET": "Phuket, Thailand",
    "SHANGHAI": "Shanghai, China",
    "MEXICO CITY": "Mexico City, Mexico",
    "FUERTEVENTURA": "Fuerteventura, Spain",
    "BELFAST": "County Antrim, United Kingdom",
    "GLASGOW": {
        1: "Glasgow, United Kingdom",
        2: "Strathaven, South Lanarkshire, United Kingdom",
        3: "Renfrewshire, United Kingdom",
        4: "North Lanarkshire, United Kingdom"
    },
    "HALKIDIKI": "Halkidiki, Greece",
    "FETHIYE-OLUDENIZ": "Dalaman, Turkey",
    "ACAPULCO": "Acapulco, Mexico",
    "MALTA": "Malta",
    "COSTA BRAVA AND COSTA BARCELONA-MARESME": {
        1: "Costa Brava, Spain",
        2: "Vilassar De Mar, Barcelona, Spain",
        3: "Sant Feliu de Boada, Girona, Spain",
        4: "Playa de Pals, Costa Brava, Spain",
        5: "Caldes d'Estrac, Barcelona, Spain"
    },
    "LA MANGA - COSTA CALIDA": "La Manga - Costa Calida, Spain",
    "PANAMA CITY": "Panama City, Panama, Panama",
    "GOA": "Goa, India",
    "AMSTERDAM AND VICINITY": "Amsterdam, Netherlands",
    "PACIFIC NORTH COAST / GUANACASTE": "Liberia  Rincon de la Vieja, Pacific North Coast, Costa Rica",
    "BARCELA": {
        1: "Barcelona, Spain",
        2: "Montserrat, Barcelona, Spain"
    },
    "LIVERPOOL": {
        1: "Liverpool, Merseyside, United Kingdom",
        2: "Frodsham, Cheshire, United Kingdom",
        3: "Southport, Merseyside, United Kingdom"
    },
    "KRAKOW": "Krakow, Poland",
    "BOURNEMOUTH": {
        1: "Bournemouth, Dorset, United Kingdom",
        2: "Lymington, Dorset, United Kingdom",
        3: "Poole, Dorset, United Kingdom"
    },
    "GUIPUZCOA - SAN SEBASTIAN": "Guipuzcoa, Spain",
    "FRANKFURT": {
        1: "Frankfurt, Germany",
        2: "Mörfelden, Hesse, Germany",
        3: "Königstein im Taunus, Hesse, Germany",
        4: "Maintal, Hesse, Germany",
        5: "Wetzlar, Hesse, Germany"
    },
    "TORONTO": "Toronto, Ontario, Canada",
    "CHICAGO - IL": "Chicago, Illinois, USA",
    "CANTABRIA": "Cantabria, Spain",
    "OSLO": "Oslo, Norway",
    "LOS CABOS": "Los Cabos, Mexico",
    "A CORUNA": "La Coruna, Spain",
    "GUADALAJARA & VICINITY": "Guadalajara, Spain",
    "KEDAH / LANGKAWI": "Langkawi, Northern Peninsular, Malaysia",
    "NORTHERN CYPRUS": "Northern Cyprus, North Cyprus",
    "PAPHOS": "Paphos, Cyprus",
    "HO CHI MINH CITY (SAIGON) AND SOUTH": "Ho Chi Minh City - Saigon, Vietnam",
    "MAJORCA": "Majorca, Spain",
    "COSTA DE AZAHAR": "Costa de Azahar, Spain",
    "BERLIN": {
        1: "Berlin, Germany",
        2: "Brandenburg, Germany"
    },
    "ORLANDO AREA - FLORIDA - FL": {
        1: "Orlando, Florida, USA",
        2: "Howey-in-the-Hills, Florida, USA"
    },
    "HURGHADA": {
        1: "Hurghada, Egypt",
        2: "El Gouna, Northern Red Sea, Egypt"
    },
    "VARNA / BLACK SEA RESORTS": {
        1: "Varna, Bulgaria",
        2: "Obzor, Bourgas, Bulgaria"
    },
    "ALANYA": {
        1: "Alanya, Antalya, Turkey",
        2: "Okurcalar, Antalya, Turkey",
        3: "Turkler, Antalya, Turkey",
        4: "Avsallar, Antalya, Turkey",
        5: "Incekum, Antalya, Turkey",
        6: "Konakli, Antalya, Turkey",
        7: "Mahmutlar, Antalya, Turkey",
        8: "Payallar, Antalya, Turkey"
    },
    "BUENOS AIRES": "Buenos Aires, Argentina",
    "BELEK": "Belek, Antalya, Turkey",
    "VIZCAYA - BILBAO": "Vizcaya, Spain",
    "PUERTO VALLARTA": "Puerto Vallarta, Mexico",
    "MALAGA": "Malaga, Spain",
    "VALENCIA": "Valencia, Spain",
    "SOUTH SARDINIA": "Sardinia, Italy",
    "DUBLIN": "Dublin, Ireland",
    "SEVILLE": "Seville, Spain",
    "MILAN": "Milan (Province), Italy",
    "ASTURIAS": "Asturias, Spain",
    "FORT LAUDERDALE - HOLLYWOOD AREA - FL": "Fort Lauderdale, Florida, USA",
    "W. CAPE-CAPE TOWN-GARDEN ROUTE": {
        1: "Western Cape Province, South Africa",
        2: "Garden Route, South Africa"
    },
    "GRANADA": "Granada, Spain",
    "MYKONOS": "Mykonos, Greece",
    "BEIJING PEKING": "Beijing, China",
    "MONACO": "Monaco, Monaco",
    "BOURGAS / BLACK SEA RESORTS": "Bourgas, Bulgaria",
    "MUNICH": {
        1: "Bavaria, Germany",
        2: "Salmdorf, Bavaria, Germany",
        3: "Starnberg, Lake Starnberg, Germany",
        4: "Munich, Germany"
    },
    "ARUBA": "Aruba, Aruba",
    "RHODES": "Rhodes, Greece",
    "VIENNA": "Vienna, Austria",
    "VARADERO": "Varadero, Cuba",
    "ALENTEJO": "Alentejo, Portugal",
    "NASSAU": "Nassau, Bahamas",
    "PATTAYA-CHONBURI": "Pattaya, Thailand",
    "CANCUN (AND VICINITY)": "Cancun, Mexico",
    "MALDIVES": "Maldives, Maldives",
    "CARTAGENA": "Cartagena, Colombia",
    "ATHENS": "Athens, Greece",
    "PYRENEES - ARAGON": "Pyrenees - Aragon, Spain",
    "NEWCASTLE-UPON-TYNE": {
        1: "Tyne and Wear, United Kingdom",
        2: "Northumberland, United Kingdom"
    },
    "ST PETERSBURG": "St Petersburg, Russia",
    "KOH SAMUI": "Koh Samui, Thailand",
    "PENANG": "Penang Island, Northern Peninsular, Malaysia",
    "YORK": "North Yorkshire, United Kingdom",
    "MELBOURNE - VIC": "Melbourne, Victoria, Australia",
    "CADIZ / JEREZ": "Costa De La Luz, Spain",
    "DUBROVNIK-SOUTH DALMATIA": "Dubrovnik Riviera, Croatia",
    "VENICE (AND VICINITY)": "Venice (Province), Italy",
    "NICE": {
        1: "Nice, Côte d'Azur, France",
        2: "Cagnes-sur-Mer, Côte d'Azur, France"
    },
    "LAKE GARDA": {
        1: "Lake Garda, Italy",
        2: "Lonato del Garda, Lombardy, Italy"
    },
    "HONG KONG": "Hong Kong, Hong Kong",
    "AYIA NAPA": "Ayia Napa, Cyprus",
    "COSTA DE VALENCIA": "Costa de Valencia, Spain",
    "ANTALYA": {
        1: "Antalya, Turkey",
        2: "Kemer Antalya, Antalya, Turkey",
        3: "Cenger, Antalya, Turkey",
        4: "Side, Antalya, Turkey",
        5: "Kizilagac, Antalya, Turkey",
        6: "Manavgat, Antalya, Turkey",
        7: "Colakli, Antalya, Turkey",
        8: "Titreyengöl, Antalya, Turkey",
        9: "Orensehir, Antalya, Turkey",
        10: "Kumkoy, Antalya, Turkey",
        11: "Alanya, Antalya, Turkey",
        12: "Okurcalar, Antalya, Turkey",
        13: "Turkler, Antalya, Turkey",
        14: "Avsallar, Antalya, Turkey",
        15: "Incekum, Antalya, Turkey",
        16: "Konakli, Antalya, Turkey",
        17: "Mahmutlar, Antalya, Turkey",
        18: "Payallar, Antalya, Turkey"
    },
    "BALI": "Bali, Indonesia",
    "MONTEGO BAY (AND VICINITY)": "Montego Bay, Jamaica, Jamaica",
    "KRABI": "Krabi, Thailand",
    "ZURICH": "Zurich, Switzerland",
    "SITGES AREA - COSTA DEL GARRAF": {
        1: "Costa Dorada, Spain",
        2: "Castelldefels, Barcelona, Spain"
    },
    "AUSTRIAN ALPS": {
        1: "Tyrol, Austria",
        2: "Salzburg, Austria",
        3: "Vorarlberg, Austria",
        4: "Carinthia, Austria"
    },
    "INVERNESS": "Highlands, United Kingdom",
    "ABU DHABI": "Abu Dhabi, United Arab Emirates"
}


currency = {
 'ABERDEEN': 'GBP',
 'AGADIR': 'EUR',
 'ALGARVE': 'EUR',
 'ALICANTE - COSTA BLANCA': 'EUR',
 'ALMERIA COAST': 'EUR',
 'AMALFI COAST': 'EUR',
 'ANDORRA': 'EUR',
 'ARUBA': 'USD',
 'ATHENS': 'EUR',
 'BARCELONA': 'EUR',
 'BELEK': 'EUR',
 'BELFAST': 'GBP',
 'BENIDORM - COSTA BLANCA': 'EUR',
 'BERLIN': 'EUR',
 'BIRMINGHAM': 'GBP',
 'BLACKPOOL': 'GBP',
 'BOURGAS / BLACK SEA RESORTS': 'EUR',
 'BRISTOL': 'GBP',
 'CANNES': 'EUR',
 'COPENHAGEN CAPITAL REGION': 'EUR',
 'CORFU': 'EUR',
 'COSTA BRAVA AND COSTA BARCELONA-MARESME': 'EUR',
 'COSTA DEL SOL': 'EUR',
 'DUBLIN': 'EUR',
 'DUBROVNIK RIVIERA': 'EUR',
 'EDINBURGH': 'GBP',
 'ESTORIL COAST': 'EUR',
 'FETHIYE-OLUDENIZ': 'EUR',
 'FRENCH ALPS': 'EUR',
 'FUERTEVENTURA': 'EUR',
 'GARDEN ROUTE': 'EUR',
 'GAUTENG- JOHANNESBURG': 'EUR',
 'GLASGOW': 'GBP',
 'GOA': 'EUR',
 'GRAN CANARIA': 'EUR',
 'GRANADA': 'EUR',
 'HALKIDIKI': 'EUR',
 'HAMMAMET': 'EUR',
 'HAVANA': 'GBP',
 'HELSINKI': 'EUR',
 'HURGHADA': 'EUR',
 'IBIZA': 'EUR',
 'ISCHIA': 'EUR',
 'ISTRIA': 'EUR',
 'KEFALONIA': 'EUR',
 'KUSADASI': 'EUR',
 'LAKE GARDA': 'EUR',
 'LANZAROTE': 'EUR',
 'LISBON': 'EUR',
 'LIVERPOOL': 'GBP',
 'LONDON': 'GBP',
 'MADEIRA': 'EUR',
 'MADRID': 'EUR',
 'MAJORCA': 'EUR',
 'MALAGA': 'EUR',
 'MALDIVES': 'EUR',
 'MANCHESTER': 'GBP',
 'MARRAKECH': 'EUR',
 'MAURITIUS ISLANDS': 'EUR',
 'MENORCA': 'EUR',
 'MYKONOS': 'EUR',
 'NAPLES': 'EUR',
 'NEWCASTLE-UPON-TYNE': 'GBP',
 'NICE': 'EUR',
 'OSLO': 'EUR',
 'PAPHOS': 'EUR',
 'PORTO AND NORTH OF PORTUGAL': 'EUR',
 'POSITANO': 'EUR',
 'SALOU AREA / COSTA DORADA': 'EUR',
 'SANTORINI': 'EUR',
 'SHARM EL SHEIKH -DAHAB': 'EUR',
 'SITGES AREA - COSTA DEL GARRAF': 'EUR',
 'SORRENTO COAST': 'EUR',
 'SPLIT-MIDDLE DALMATIA': 'EUR',
 'TENERIFE': 'EUR',
 'THESSALONIKA': 'EUR',
 'ZANTE': 'EUR'
}
