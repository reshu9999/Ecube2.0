# App Imports
from hotel.models import RequestMaster, HotelCrawlRequestDetail,HotelFlightRequestInputDetail,HotelRequestInputDetail

# Package Imports
import pymysql
from pdb import set_trace as st
import pandas as pd
import datetime
# Core Imports
from eCube_UI_2.core.Add_Request import views as core_views
from decimal import Decimal
# Django Imports
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from hotel.master.models import StarRatingMaster


core_views.RequestManagementModels.MODELS_MAP = {
    'CrawlRequestDetail': HotelCrawlRequestDetail,
    'FieldGroupMapping': None,
    'RequestMaster': RequestMaster,
}
core_views.RequestManagementModels.check_required_models()


@csrf_exempt
def reparse_request_run(request, request_run_id):
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    reparse_query = "UPDATE tbl_RequestRunDetail SET FK_StatusId='10', RunMode='Reparse' WHERE RequestRunId='%s';" % request_run_id
    cur = db.cursor()
    cur.execute(reparse_query)
    db.commit()
    cur.close()
    db.close()
    return JsonResponse({'success': True, 'reparse_req_run': request_run_id})


@csrf_exempt
def reparse_sub_request(request, request_run_id, sub_request_id):
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    reparse_query = "UPDATE tbl_HotelCrawlRequestDetail SET StatusId=10 WHERE HotelCrawlRequestDetailId='%s';" % sub_request_id
    cur = db.cursor()
    cur.execute(reparse_query)
    db.commit()
    cur.close()

    reparse_query = "UPDATE tbl_RequestRunDetail SET FK_StatusId='10', RunMode='Reparse' WHERE RequestRunId='%s';" % request_run_id
    cur = db.cursor()
    cur.execute(reparse_query)
    db.commit()
    cur.close()

    db.close()
    return JsonResponse({'success': True, 'reparse_sub_req': sub_request_id})


@csrf_exempt
def pause_request_run(request, request_run_id):
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    pause_query = "UPDATE tbl_RequestRunDetail SET FK_StatusId=7 WHERE RequestRunId=%s;" % request_run_id
    cur = db.cursor()
    cur.execute(pause_query)
    db.commit()
    cur.close()
    db.close()
    return JsonResponse({'success': True, 'pause_req_run': request_run_id})


@csrf_exempt
def resume_request_run(request, request_run_id):
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    resume_query = "UPDATE tbl_RequestRunDetail SET FK_StatusId=5 WHERE RequestRunId=%s;" % request_run_id
    cur = db.cursor()
    cur.execute(resume_query)
    db.commit()
    cur.close()
    resume_query = "UPDATE tbl_HotelCrawlRequestDetail SET StatusId=5 WHERE RequestRunId=%s AND StatusId!=12;" % request_run_id
    cur = db.cursor()
    cur.execute(resume_query)
    db.commit()
    cur.close()
    db.close()
    return JsonResponse({'success': True, 'resume_req_run': request_run_id})


@csrf_exempt
def stop_request_run(request, request_run_id):
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    stop_query = "UPDATE tbl_RequestRunDetail SET FK_StatusId=6 WHERE RequestRunId=%s;" % request_run_id
    cur = db.cursor()
    cur.execute(stop_query)
    db.commit()
    cur.close()
    db.close()
    return JsonResponse({'success': True, 'stop_req_run': request_run_id})


@csrf_exempt
def delete_request_schedule(request, request_id):
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    set_safe_update = "SET SQL_SAFE_UPDATES=0;"
    delete_query = "DELETE FROM tbl_ScheduleDate WHERE SD_RequestId=%s AND Status='Pending';" % request_id
    cur = db.cursor()
    cur.execute(set_safe_update)
    cur.execute(delete_query)
    db.commit()
    cur.close()
    db.close()
    return JsonResponse({'success': True, 'del_req_schedule': request_id})



@csrf_exempt
def request_management(request):
    return render(request, 'hotel/req_management/aetos_index.html')



@csrf_exempt
def fetch_request(request):
    if request.method == 'GET' or request.is_ajax():
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        data_obj = core_views.request_management(request, db)
        data ={
            "reqList":data_obj
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def request_management_popup(request):
    if request.method == 'GET':
        request_run_id = request.GET.get('req_runid')

        results = sp_get_by_param('sp_GetRequestRunCompetitors', [int(request_run_id)])

        competitors = []
        for result in results:
            competitors.append({'id': result[0], 'name': result[1]})
        return render(request, 'hotel/req_management/req_man_popup.html', context={"competitors": competitors})
    else:
        return JsonResponse({"data": "success"})


@csrf_exempt
def edit_request_router(request):

    if request.method == 'POST' and request.is_ajax():
       
        editReqId = request.POST['req_id']
        HotelFlight = HotelFlightRequestInputDetail.objects.filter(requests=editReqId)
        Hotel = HotelRequestInputDetail.objects.filter(requests=editReqId)
        request.session['request_action'] = 'update_request'
        if not HotelFlight:
            url = reverse('hotel_create_request')
        else:
            url = reverse('hotel_plus_flight_request')
        
    context = {
        "Message": "Request created successfully", "flag": "0" ,"url": url 
    }
    return JsonResponse(context) 


def aetos_SP_all_operation_genric(sp_name, list_args):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        if not isinstance(list_args, list):
            list_args = [list_args]
        cursor = db.cursor()
        args = list_args
        cursor.callproc(procname=sp_name , args=args)
        cursor.close()
        db.commit()


def sp_get_by_param(sp_name , list_args):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        if not isinstance(list_args, list):
            list_args = [list_args]
        cursor = db.cursor()
        args = list_args
        cursor.callproc(procname=sp_name , args=args)
        records = cursor.fetchall()
        cursor.close()
        db.commit()
        return records


def get_psfail_data_from_mongo(field_id, field_type):
    client = MongoClient('mongodb://10.100.18.12:27017')
    db = client.HTMLDumps
    if field_type == '2':
        return db.ParsingErrorTracker.find({'subRequestId':int(field_id)})
    return db.ParsingErrorTracker.find({'requestRunId':int(field_id)})

@csrf_exempt
def download_psfail_excel(request):
    if request.method == 'POST' or request.is_ajax():
        field_id = request.POST['field_id']
        field_type = request.POST['field_type']
                
        result = get_psfail_data_from_mongo(field_id, field_type)
        response = []
        for res in result:                                
            result_dict = {
                'Country':res['Country'], 'DomainName':res['DomainName'], 'PointOfSale':res['PointOfSale'],
                'ParserScript':res['ParserScript'], 'RequestRunId':res['requestRunId'],'RequestId':res['requestId'],
                'HotelName': res['HotelName'], 'SubRequestId':res['subRequestId'], 'ScrapperScript':res['ScraperScript'],
                'ParserError':res['ParserError'],
            }
            response.append(result_dict)

        if response:
            df = pd.DataFrame(response)
            time = 'psfail_error_%s' % datetime.datetime.now()
            path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/psfail/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=['Country', 'DomainName', 'PointOfSale', 'ParserScript', 'RequestRunId', 'RequestId','HotelName', 'SubRequestId','ScrapperScript','ParserError'], index=False)
            writer.save()
            path = '/static/psfail/%s' % time + '.xlsx'
            return JsonResponse({'path': path, 'msg': 'File Downloaded Succesfully'}, safe=False)
        
    return JsonResponse({'path': '', 'msg': 'No Data Found'}, safe=False)


def get_pnf_data_from_mongo(field_id, field_type):
    client = MongoClient('mongodb://10.100.18.12:27017')
    db = client.HTMLDumps
    if field_type == '2':        
        return db.PNFData.find({'subRequestId':int(field_id)})
    return db.PNFData.find({'requestRunId':int(field_id)})

@csrf_exempt
def download_pnf_excel(request):
    if request.method == 'POST' or request.is_ajax():
        field_id = request.POST['field_id']
        field_type = request.POST['field_type']
                
        result = get_pnf_data_from_mongo(field_id, field_type)
        response = []
        for res in result:                                 
            result_dict = {
                'Country':res['country'], 'DomainName':res['DomainName'], 'PointOfSale':res['RequestInputs']['pos'], 'ParserScript':res['ParserScript'],
                'RequestRunId':res['requestRunId'], 'RequestId':res['requestId'], 'SubRequestId':res['subRequestId'],
                'ScrapperScript':res['ScraperScript'], 'ScrapperError':res['error_msg'], 'ErrorCode': res['error_code']
            }
            response.append(result_dict)

        if response:
            df = pd.DataFrame(response)
            time = 'pnf_error_%s' % datetime.datetime.now()
            path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/pnf/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=['Country', 'DomainName', 'PointOfSale', 'ParserScript', 'RequestRunId',     'RequestId','SubRequestId','ScrapperScript','ScrapperError', 'ErrorCode'], index=False)
            writer.save()
            path = '/static/pnf/%s' % time + '.xlsx'
            return JsonResponse({'path': path, 'msg': 'File Downloaded Succesfully'}, safe=False)
    
    return JsonResponse({'path': '', 'msg': 'No Data Found'}, safe=False)      


@csrf_exempt
def File_download_excel_req_man(request):
    if request.method == 'GET' or request.is_ajax():
        req_run_id = request.POST['req_run_id']
        req_id = request.POST['req_id']
        lst = [req_id,req_run_id,'']
        sp_res_1 = sp_get_by_param('sp_LastResult',lst)
        list1 = []
        dict1 = {} 
        l_list = []

        for Sp_res in sp_res_1:
            s_list = []
            for res in Sp_res:
                if res == '{}' or res == '{' or res == '}':
                    res = ''
                s_list.append(res)
            l_list.append(s_list)
               
                    

        for Sp_res in l_list:            
            Dates = datetime.datetime.strptime(Sp_res[3], "%m/%d/%Y")
            Dates = datetime.datetime.strftime(Dates, "%d/%m/%Y")
            Timestamp = datetime.datetime.strptime(Sp_res[1], "%m/%d/%Y %H:%M")
            Timestamp = datetime.datetime.strftime(Timestamp, "%d/%m/%Y %H:%M")

            if request.session.get('bli_id') == '6': #Availability
                dict1 = {'Timestamp' :Timestamp,	'Company':Sp_res[2],	'Dates':Dates	,'Nights':Sp_res[4],	'Hotel':Sp_res[5],	'Hotel Id':Sp_res[6]	,'PointOfSale':Sp_res[7],	'City':Sp_res[8],	'State':Sp_res[9],	'Country':Sp_res[10],	'Daily Rate': chk_digit(Sp_res[11]),	'Rcode':Sp_res[12],	'Tax':Sp_res[13]	,'RoomType':Sp_res[14],	'RoomCode':Sp_res[15],	'Supplier Hotel':Sp_res[16],	'Cancellation Policy':Sp_res[17],	'Star Rating':Sp_res[18],	'Price':Sp_res[20],	'Currency':Sp_res[21],	'BreakFast':Sp_res[22],	'Availability':Sp_res[23],	'Board':Sp_res[24],	'Unique code':Sp_res[25],	'Status':Sp_res[26],	'PageURL':Sp_res[27],	'Hotel Code':chk_digit(Sp_res[28]),	'Contract Name':Sp_res[29],	'Classification':Sp_res[30],	'B2B':Sp_res[32],	'Com.Ofici':Sp_res[33],	'Com.Canal':Sp_res[34],	'Com.Neta':Sp_res[35],	'NetPrice':Sp_res[41],	'SellingPrice':Sp_res[42],	'Commision':Sp_res[43],	'DirectPayment':Sp_res[44],	'SellingPriceMandatory':Sp_res[45],	'Integration':Sp_res[31],	'Promotion':Sp_res[47],	'Promotion Description':Sp_res[48],	'HTL ORDER OF APPEARANCE': chk_digit(Sp_res[49]),	'Type of Event':Sp_res[51],	'Supplier':Sp_res[53],	'Room Availability':Sp_res[54],	'Paxs':Sp_res[55],	'Opaque Rate':Sp_res[56],	'Lead Time':Sp_res[57],	'Account Name':Sp_res[58],	'Dynamic Property':Sp_res[59],	'HM Hotel ID':Sp_res[52],	'HotelAddress':Sp_res[60],	'Supplier Hotel URL':Sp_res[66],	'Competitor Hotel ID': chk_digit(Sp_res[67]),	'Longitude': chk_digit(Sp_res[68]),	'Latitude': chk_digit(Sp_res[69])}                

            else:     
               dict1 = {'Timestamp' :Timestamp,	'Company':Sp_res[2],	'Dates':Dates	,'Nights':Sp_res[4],	'Hotel':Sp_res[5],	'Hotel Id':Sp_res[6]	,'PointOfSale':Sp_res[7],	'City':Sp_res[8],	'State':Sp_res[9],	'Country':Sp_res[10],	'Daily Rate': chk_digit(Sp_res[11]),	'Rcode':Sp_res[12],	'Tax':Sp_res[13]	,'RoomType':Sp_res[14],	'RoomCode':Sp_res[15],	'Supplier Hotel':Sp_res[16],	'Cancellation Policy':Sp_res[17],	'Star Rating':Sp_res[18],	'Price':Sp_res[20],	'Currency':Sp_res[21],	'BreakFast':Sp_res[22],	'Availability':Sp_res[23],	'Board':Sp_res[24],	'Unique code':Sp_res[25],	'Status':Sp_res[26],	'PageURL':Sp_res[27],	'Hotel Code':chk_digit(Sp_res[28]),	'Contract Name':Sp_res[29],	'Classification':Sp_res[30],	'B2B':Sp_res[32],	'Com.Ofici':Sp_res[33],	'Com.Canal':Sp_res[34],	'Com.Neta':Sp_res[35],	'NetPrice':Sp_res[41],	'SellingPrice':Sp_res[42],	'Commision':Sp_res[43],	'DirectPayment':Sp_res[44],	'SellingPriceMandatory':Sp_res[45],	'Integration':Sp_res[31],	'Promotion':Sp_res[47],	'Promotion Description':Sp_res[48],	'HTL ORDER OF APPEARANCE': chk_digit(Sp_res[49]),	'Type of Event':Sp_res[51],	'Supplier':Sp_res[53],	'Room Availability':Sp_res[54],	'Paxs':Sp_res[55],	'Opaque Rate':Sp_res[56],	'Lead Time':Sp_res[57],	'Account Name':Sp_res[58],	'Dynamic Property':Sp_res[59],	'HMHotelID':Sp_res[52],	'HotelAddress':Sp_res[60],	'nvcrSupplierHotelURL':Sp_res[66],	'nvcrCompetitorHotelID': chk_digit(Sp_res[67]),	'nvcrLongitude': chk_digit(Sp_res[68]),	'nvcrLatitude': chk_digit(Sp_res[69]),	'Cost':Sp_res[70],	'CostCurrency':Sp_res[71],	'CostTaxPercent':Sp_res[72],	'Included':Sp_res[73],	'TAXNotIncluded':Sp_res[74],	'NotIncluded1':Sp_res[75],	'TAXIncluded':Sp_res[76],	'CurrencyIncluded':Sp_res[77],	'Included2':Sp_res[78],'TAX_NotIncluded':Sp_res[79],	'CurrencyNotIncluded':Sp_res[80],	'Notincluded2':Sp_res[81],'RoomChar':Sp_res[82],'ZoneName':Sp_res[83]}
        
            list1.append(dict1)

        if len(list1) > 0:
            df = pd.DataFrame(list1)
            time = 'Report_output_excel_%s' % datetime.datetime.now() + ''
            path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            if request.session.get('bli_id') == '6': #Availability
                columns = ['Timestamp',	'Company',	'Dates'	,'Nights',	'Hotel',	'Hotel Id'	,'PointOfSale',	'City',	'State',	'Country',	'Daily Rate',	'Rcode',	'Tax'	,'RoomType',	'RoomCode',	'Supplier Hotel',	'Cancellation Policy',	'Star Rating',	'Price',	'Currency',	'BreakFast',	'Availability',	'Board',	'Unique code',	'Status',	'PageURL',	'Hotel Code',	'Contract Name',	'Classification',	'B2B',	'Com.Ofici',	'Com.Canal',	'Com.Neta',	'NetPrice',	'SellingPrice',	'Commision',	'DirectPayment',	'SellingPriceMandatory',	'Integration',	'Promotion',	'Promotion Description',	'HTL ORDER OF APPEARANCE',	'Type of Event',	'Supplier',	'Room Availability',	'Paxs',	'Opaque Rate',	'Lead Time',	'Account Name',	'Dynamic Property',	'HM Hotel ID',	'HotelAddress',	'Supplier Hotel URL',	'Competitor Hotel ID', 'Longitude', 'Latitude']

            else:
                columns = ['Timestamp',	'Company',	'Dates'	,'Nights',	'Hotel',	'Hotel Id'	,'PointOfSale',	'City',	'State',	'Country',	'Daily Rate',	'Rcode',	'Tax'	,'RoomType',	'RoomCode',	'Supplier Hotel',	'Cancellation Policy',	'Star Rating',	'Price',	'Currency',	'BreakFast',	'Availability',	'Board',	'Unique code',	'Status',	'PageURL',	'Hotel Code',	'Contract Name',	'Classification',	'B2B',	'Com.Ofici',	'Com.Canal',	'Com.Neta',	'NetPrice',	'SellingPrice',	'Commision',	'DirectPayment',	'SellingPriceMandatory',	'Integration',	'Promotion',	'Promotion Description',	'HTL ORDER OF APPEARANCE',	'Type of Event',	'Supplier',	'Room Availability',	'Paxs',	'Opaque Rate',	'Lead Time',	'Account Name',	'Dynamic Property',	'HMHotelID',	'HotelAddress',	'nvcrSupplierHotelURL',	'nvcrCompetitorHotelID',	'nvcrLongitude',	'nvcrLatitude',	'Cost',	'CostCurrency',	'CostTaxPercent',	'Included',	'TAXNotIncluded',	'NotIncluded1',	'TAXIncluded',	'CurrencyIncluded',	'Included2','TAX_NotIncluded',	'CurrencyNotIncluded',	'Notincluded2','RoomChar','ZoneName']


            df.to_excel(writer, 'Sheet1', columns=columns, index=False)
            writer.save()
            path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
            count=len(list1)
        else :
            count= "0"
            path=""
        data = {
            'Path':path,
            'count':count
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



def chk_digit (item):
    try:
        item = Decimal(item)
    except Exception as e:
        pass
    return item


def convert_star_code(star_List,val):
    starcode="Pendi"
    for star in star_List:
        if (star["starrating"]==str(val)):
            starcode= star["starratingcode"]
            break
    return starcode


@csrf_exempt
def File_download_excel_req_man_mongo(request):
    if request.method == 'GET' or request.is_ajax():
        req_run_id = request.POST['req_run_id']
        req_id = request.POST['req_id']
        star_List = list(StarRatingMaster.objects.values('starrating', 'starratingcode'))
        # star_code = convert_star_code(star_List, 5)
        client = MongoClient('mongodb://10.100.18.12:27017')
        mongo_db = client.HTMLDumps
        result = mongo_db.CrawlResponseData.find({'requestRunId': int(req_run_id)})
        list1 = []
        dict1 = {}
        
        for Sp_res in result:
        
            for room_type in Sp_res["hotel"]["room_types"]:
        
                dict1 = {
                 'subRequestId': Sp_res["subRequestId"],
                 'GroupName' :Sp_res["GroupName"], 
                 'call_func' :Sp_res["call_func"], 
                 'RequestUrl' :Sp_res["RequestUrl"], 
                 'requestId' :Sp_res["requestId"], 
                 'DomainId' :Sp_res["DomainID"], 
                 'ScraperScript' :Sp_res["ScraperScript"],
                  'ParserScript' :Sp_res["ParserScript"],
                   'requestRunId' :Sp_res["requestRunId"],
                     'PointOfSale' :Sp_res["PointOfSale"] ,
                      'BusinessType' :Sp_res["BusinessType"] ,
                       'DomainName' :Sp_res["DomainName"], 
                       'CompetitorName' :Sp_res["RequestInputs"]["CompetitorName"], 
                       'city' :Sp_res["RequestInputs"]["city"],
                       'competitorId' :Sp_res["RequestInputs"]["competitorId"],
                        'starRating' : convert_star_code(star_List,Sp_res["hotel"].get("starRating", ""))  ,
                        'board' :Sp_res["RequestInputs"]["board"],
                        'RequestUrl' :Sp_res["RequestInputs"]["RequestUrl"],
                        'children' :Sp_res["RequestInputs"]["children"],
                        'CrawlMode' :Sp_res["RequestInputs"]["CrawlMode"], 
                        'city_zone': Sp_res["hotel"].get("city_zone",""),
                         'page_path': Sp_res["hotel"].get("page_path",""),
                           'longitude': Sp_res["hotel"].get("longitude",""),
                            'total_hotel': Sp_res["hotel"].get("total_hotel",""),
                             'address': Sp_res["hotel"].get("address",""),
                             'website_id': Sp_res["hotel"].get("website_id",""), 
                             'POS': Sp_res["RequestInputs"]["pos"],
                             'latitude': Sp_res["hotel"].get("latitude",""), 
                              'adults': Sp_res["RequestInputs"]["adults"],
                              'checkIn': Sp_res["RequestInputs"]["checkIn"],
                              'checkOut': Sp_res["RequestInputs"]["checkOut"],
                              'nights': Sp_res["RequestInputs"]["nights"],
                              'country': Sp_res["RequestInputs"]["country"],
                              'hotelName': Sp_res["hotel"].get("hotelName",""), 
                 'promotionDesc' : room_type.get("promotionDesc","") ,
                 'paymentOption' : room_type.get("paymentOption",""),
                 'availability' : room_type.get("availability",""),
                  'currency' : room_type.get("currency",""),
                  'price' : room_type.get("price",""),
                  'board_code' : room_type.get("board_code",""),
                  'daily_price' : room_type.get("daily_price",""),
                  'type' : room_type.get("type",""),
                  'promotion' : room_type.get("promotion",""),}
                list1.append(dict1)
        
        if len(list1) > 0:
            df = pd.DataFrame(list1)
            time = 'Report_output_excel_%s' % datetime.datetime.now() + ''
            path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=['subRequestId','GroupName','call_func','RequestUrl','requestId','DomainId','DomainName','BusinessType','ScraperScript', 'ParserScript','requestRunId','country','hotelName','PointOfSale','city','checkOut','checkIn','competitorId',
            'children','adults','CompetitorName','board','nights','starRating','RequestUrl','CrawlMode','POS',
            'latitude','longitude','address','website_id','city_zone',
            'total_hotel','page_path','promotionDesc','paymentOption','availability','currency','price','board_code','daily_price','type','promotion'], index=False)
            writer.save()
            path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
            count=len(list1)
        else :
            count= "0"
            path=""
        data = {
            'Path':path,
            'count':count
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Pnf_Recrwal(request):
    if request.method == 'GET' or request.is_ajax():
        request_run_id = request.POST['id']

        list_args = [request_run_id]
        sp_res =  aetos_SP_all_operation_genric('sp_SetRequest',list_args)
        data = {
            'Req_man': "Pnf recrawl started successfully",
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Recrwal(request):
    if request.method == 'GET' or request.is_ajax():
        requId = request.POST['requId']
        req_run_id = request.POST['req_run_id']
        list_args = [req_run_id, 'request_run']
        client = MongoClient('mongodb://10.100.18.11:27017')
        collection = client.HTMLDumps.HTMLRepository
        collection.remove({'requestRunId': int(req_run_id)})
        sp_res =  aetos_SP_all_operation_genric('sp_PushToRecrawl',list_args)
        data = {
            'Req_man': "Recrawl started successfully",
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Sub_Recrwal(request):
    if request.method == 'POST' or request.is_ajax():
        requId = request.POST['requId']
        req_run_id = request.POST['req_run_id']
        sub_id = request.POST['sub_id']
        list_args = [sub_id, 'sub_request']
        print('sp args = ', list_args)
        print('started sp_PushToRecrawl at ', datetime.datetime.now())
        aetos_SP_all_operation_genric('sp_PushToRecrawl',list_args)
        print('ended sp_PushToRecrawl at ', datetime.datetime.now())
        data = {
            'Req_man': "Recrawl started successfully",
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_modal(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        supplier_list = None

        if 'suppliers[]' in request.POST:
            supplier_list = request.POST.getlist('suppliers[]')

        check_in_dates = request.POST.get('check_in_dates', '')
        suppliers = ''

        if supplier_list:
            suppliers = ",".join(supplier_list)

        list_args = [id, suppliers, check_in_dates]
        sp_res =  sp_get_by_param('sp_HotelGetCrawlRequestDetails',list_args)
        data = {
            'Req_man': sp_res,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_Second_modal(request):
    if request.method == 'GET' or request.is_ajax():
        sub_dip_id = request.POST['id']
        dip_id = request.POST['sec_id']
        list_args = [sub_dip_id,dip_id]
        sp_res =  sp_get_by_param('sp_getHotel_req_second_popup_data',list_args)
        data = {
            'Req_man': sp_res,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)
