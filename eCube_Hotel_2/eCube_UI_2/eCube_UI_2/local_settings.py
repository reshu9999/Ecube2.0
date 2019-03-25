# LOGIN SETTINGS
LOGIN_URL = '/login/'
POST_LOGIN_URL = '/DashBoard/Index/'
#FORGOT_PASSWORD_URL = '/login/'
FORGOT_PASSWORD_URL = '/login/forgot-password/'
CONFIRM_RESET_PASSWORD = '/user-management/confirm-reset-password/'
RESET_PASSWORD = '/user-management/reset-password/'
LOGIN_CHECK_URL = '/login/check-bli/'
# MEDIA_URL = '/gui/media/'

ALLOWED_HOSTS = ['ecube-hotel.eclerx.com','localhost', '10.100.18.86']
#SERVICES_IP = 'hotelmonitoruat.eclerx.com'
DJANGO_BASEURL = 'https://ecube-hotel.eclerx.com'
PUSH_DB_NAME = 'HotelMonitor_HotelBeds'
HOTEL_BEDS_RPT_TYPE ='HB'
HOTEL_BEDS_AVL_RPT_TYPE ='HBA'
SERVICES_IP = 'ecube-hotel.eclerx.com/mongo_api'
DJANGO_URL = 'localhost'

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_IDLE_TIMEOUT = 1800   #seconds
SCRIPT_DOWNLOAD_SERVER = "10.100.18.89"



BLI_SCRIPT_DIR = {
    '1': 'Hotelbeds/',
    '6': 'Hotelbeds_Availability/',
}

MAPPING = {'1':'HOTELBEDS','6':'HOTELBEDS_AVAILABILITY'}
HOTELBEDS = list()
HOTELBEDS_AVAILABILITY = list()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eCube_Centralized_DB',
        'USER': 'tech',
        'PASSWORD': 'eclerx#123',
        'HOST': '10.100.18.85',
        'PORT': '3306',
	    'OPTIONS': {
		    "init_command": "SET foreign_key_checks = 0;"
	    },
    }
}

DOMAINTAGS = {'ExpediaHotel':'Expediahotel',
              'TravelRepublic':'Travelrepublic',
              'Global Market H3':'DOTW',
              'HRS':'HRS',
              'STARWOOD_HOTELS':'Starwood',
              'Global Market H1':'GTA',
              'TripAdvisor':'Tripadvisor',
              'Agoda':'Agoda',
              'HYATT HOTELS_AND_RESORTS':'Hyatt',
              'Local Market B9':'LMB9',
              'Thomascook':'Thomascook',
              'Local Market H1':'HotelDoLMH1',
              'Local Market B1':'HotelDoLMB1',
              'ACCOR_HOTELS':'Accor',
              'Bedsonline':'Bedsonline',
              'Hotelopia':'Hotelopia',
              'Global Market H11':'Tourico',
              'Hotelbeds':'Hotelbeds',
              'Marriot':'Marriot',
              'Thomas Cook DE':'ThomascookDE',
              'Booking':'Booking',
              'Travco':'Travco',
              'Venere':'Venere',
              'ExpediaApp':'ExpediaApp',
              'Booking (Registered)':'BookingReg',
              'Global Market H1- Global Chains':'GTACHAIN',
              'HILTON_WORLDWIDE':'Hilton',
              'IHG':'IHG',
              'Best Western':'BestWestern',
              'Choice':'Choice',
              'Carlson Rezidor':'Carlson',
              'Wyndham':'Wyndham',
              'Ctrip':'Ctrip'
}

BATCH_UPLOAD_HOTEL_COLUMNS = [
    'Batch Name', 'Country', 'Destination', 'Hotel', 'Source Market', 'Adults', 'Children',
    'Check-in & Check-out date Dates', 'Advance Dates', 'Start & End Check-in date', 'Days',
    'Nights', 'Supplier 1', 'Supplier 2', 'Supplier 3', 'Supplier 4', 'Supplier 5', 'Supplier 6',
    'Supplier 7', 'Supplier 8', 'Supplier 9', 'Supplier 10', 'Supplier 11', 'Supplier 12', 'Supplier 13',
    'Supplier 14', 'Supplier 15', 'Supplier 16', 'Supplier 17', 'Supplier 18', 'Supplier 19', 'Supplier 20',
    'Schedule Duration', 'Schedule Frequency', 'Which Week?', 'Which Day of week/month?', 'Which Month?',
    'Which date of month?', 'Schedule Time'
]
