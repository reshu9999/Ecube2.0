import json
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from hotel.master.models import (CountryMaster,CityMaster,UserMaster,AirportCodeMaster,BoardTypeMaster,
                                HotelGroupMaster, PointOfSaleMaster,HotelMaster,StarRatingMaster,temphotelmaster)
from pdb import set_trace as st
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas as pd
import numpy as np
from django.http import JsonResponse, HttpResponse
import pymysql

def master_index(request):
    return render(request, 'hotel/master/master_index.html')

def master_country(request):
    '''
    Country Master related operations, table used "tbl_CountryMaster" and 
    model Used "CountryMaster"
    '''
    msg=None
    if request.method=='POST':
        '''
        This method check if the page is called in POST method to add or edit any existing data. 
        Here only timeZone and Active fields are allowed to edit, because Country name and code is 
        constant for program lifetime. 

        else get_create method could have been used. 
        '''
        if request.POST['ed_referenceNo']=='':
            if CountryMaster.objects.filter(code = request.POST['ed_Countrycode']):
                msg = "Sorry Country Code is already Exist"
            elif  CountryMaster.objects.filter(name__iexact = request.POST['ed_CountryName'].lower()):
                msg = "Sorry  "+request.POST['ed_CountryName']+" Country  already Exist in system"
            else:
                countryObj=CountryMaster(name=request.POST['ed_CountryName'],code=request.POST['ed_Countrycode'],
                                        timezone=request.POST['ed_TimeZone'],
                                        _active=1 if request.POST['ed_activeValue']=='Active' else 0)
                countryObj.save()
                msg="Record Added Successfully.."
        else:
            countryObj= CountryMaster.objects.filter(id=request.POST['ed_referenceNo']).update(
                                                name=request.POST['ed_CountryName'],code=request.POST['ed_Countrycode'],
                                                timezone=request.POST['ed_TimeZone'],
                                                _active=1 if request.POST['ed_activeValue']=='Active' else 0)
            msg="Record Modified Successfully..."
    
    countryList=[]
    #  countryList=[[i.name,i.code,i.timezone,i.active,i.id] for i in CountryMaster.objects.all()]
    countryFields=['CountryName','CountryCode','TimeZone','Active']
    return render(request,'hotel/master/master_country.html',{'CountryList':countryList,'CountryField':countryFields,'PageName':'CountryMaster','msg':msg})

def master_cities(request):
    '''
    Cities Master related Operations, table used "Cities" and model used "CityMaster"
    '''
    msg=None
    if request.method=='POST':
        '''
        This method will handle Create/Edit operations 
        '''
        if request.POST['ed_referenceNo']=='':
            if CityMaster.objects.filter(code = request.POST['ed_CityCode']):
                msg = "Sorry City Code is already Exist"
            else:
                cityObj=CityMaster(name=request.POST['ed_CityName'],code=request.POST['ed_CityCode'],
                                country_id=CountryMaster.objects.get(id=request.POST['ed_CountryID']).id,
                                _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                created_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                created_date=timezone.now(),
                                modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                modified_date=timezone.now())
                cityObj.save()
                msg="City is Added Successfully"
        else:
            cityObj=CityMaster.objects.filter(id=request.POST['ed_referenceNo']).update(code=request.POST['ed_CityCode'],
                                                                                country_id=CountryMaster.objects.get(id=request.POST['ed_CountryID']),
                                                                                _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                                                                modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                                                                modified_date=timezone.now()
                                                                                )
            msg="City is Modified Successfully"

    # countryList=[i.name for i in CountryMaster.objects.all()]
    #cityList=[[i.name,i.code,CountryMaster.objects.get(id=i.country_id).name,i.active,i.id] for i in CityMaster.objects.all()]
    # cityList=[[i.name,i.code,i.country.name,i.active,i.id] for i in CityMaster.objects.all()]
    cityList=[]
    countryList =[]
    cityFields=['CityName','CityCode','CountryName','Active']
    return render(request,'hotel/master/master_city.html',{'CityList':cityList,'CityField':cityFields,'CountryList':countryList,'msg':msg})

def master_airport(request):
    msg=None
    if request.method=='POST':
        '''
        '''
        if request.POST['ed_referenceNo']=='':
            if AirportCodeMaster.objects.filter(code = request.POST['ed_AirportCode']):
                msg = "Sorry Airport Code is already Exist"
            else:
                airportObj=AirportCodeMaster(name=request.POST['ed_AirportName'],code=request.POST['ed_AirportCode'],
                                            country_id=CountryMaster.objects.get(id=request.POST['ed_CountryName']).id,
                                            city_id=CityMaster.objects.get(id=request.POST['ed_CityName']).id,
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            created_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            created_date=timezone.now(),
                                            modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            modified_date=timezone.now())
                airportObj.save()
                msg="Airport Details Added Successfully..."
        else:
            airportObj=AirportCodeMaster.objects.filter(id=request.POST['ed_referenceNo']).update(name=request.POST['ed_AirportName'],
                                            code=request.POST['ed_AirportCode'],
                                            country_id=CountryMaster.objects.get(id=request.POST['ed_CountryName']),
                                            city_id=CityMaster.objects.get(id=request.POST['ed_CityName']),
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            modified_date=timezone.now())

            msg="Aiport Details Modified Successfully.."

    countryList=[]
    cityList=[]
    airportList=[]
    airportFields=['AirportName','AirportCode','CountryName','CityName','Active']
    return render(request,'hotel/master/master_airport.html',{'AirportList':airportList,'AirportFields':airportFields,
                                                            'CityList':cityList,
                                                            'CountryList':countryList,'msg':msg})

def master_board(request):
    msg=None
    if request.method=='POST':
        if request.POST['ed_referenceNo']=='':
            if BoardTypeMaster.objects.filter(boardtypecode = request.POST['ed_BoardCode']):
                msg = "Sorry Board Type Code is already Exist"
            else:
                boardObj=BoardTypeMaster(boardtypecode=request.POST['ed_BoardCode'],boardtypedescription=request.POST['ed_BoardDesc'],
                                        _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                        createdby=UserMaster.objects.get(User_ID=request.session['UserID']),
                                        createddate=timezone.now(),
                                        modifiedby=UserMaster.objects.get(User_ID=request.session['UserID']),
                                        modifieddate=timezone.now())
                boardObj.save()
                msg="BoardTypeMaster Added Successfully..."
        else:
            baordObj=BoardTypeMaster.objects.filter(id=request.POST['ed_referenceNo']).update(boardtypecode=request.POST['ed_BoardCode'],
                                            boardtypedescription=request.POST['ed_BoardDesc'],
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            modifiedby=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            modifieddate=timezone.now())
            msg="BoardTypeMaster Modified Successfully..."

    boardList=[]
    boardFields=['BoardTypecode','BoardTypeDescription','Active']
    return render(request,'hotel/master/master_board.html',{'BoardList':boardList,'BoardFields':boardFields,'msg':msg})

def master_hotelgrp(request):
    msg=None
    if request.method=='POST':
        if request.POST['ed_referenceNo']=='':
            if HotelGroupMaster.objects.filter(group = request.POST['ed_HotelgrpName']):
                msg = "Sorry Hotel Group is already Exist"
            else:
                hotelgrpObj=HotelGroupMaster(group=request.POST['ed_HotelgrpName'],
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            created_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            created_date=timezone.now(),
                                            modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            modified_date=timezone.now())
                hotelgrpObj.save()
                msg="Hotel Group Master Added Successfully..."
        else:
            hotelgrpObj=HotelGroupMaster.objects.filter(id=request.POST['ed_referenceNo']).update(group=request.POST['ed_HotelgrpName'],
                                        _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                        modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                        modified_date=timezone.now())
            msg="Hotel Group Master Modified Successfully..."

    hotelgrpList=[[i.group,i.active,i.id] for i in HotelGroupMaster.objects.all()]
    hotelgrpFields=['HotelGroupName','Active']
    return render(request,'hotel/master/master_hotelgrp.html',{'HotelgrpList':hotelgrpList,'HotelgrpFields':hotelgrpFields,'msg':msg})


def master_pos(request):
    msg=None
    if request.method=='POST':
        '''
        '''
        if request.POST['ed_referenceNo']=='':
            
            if PointOfSaleMaster.objects.filter(code = request.POST['ed_POSCode']):
                msg = "Sorry Point of Sale Code is already Exist"
            else:
                posObj=PointOfSaleMaster(point_of_sale=request.POST['ed_POS'],
                                        code=request.POST['ed_POSCode'],
                                        _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                        created_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                        created_date=timezone.now(),
                                        modified_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                        modified_date=timezone.now())
                posObj.save()
                msg="Point of Sale Added Successfully.."
        else:
            posObj=PointOfSaleMaster.objects.filter(id=request.POST['ed_referenceNo']).update(point_of_sale=request.POST['ed_POS'],
                                            code=request.POST['ed_POSCode'],
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            modified_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                            modified_date=timezone.now())
            msg="Point of Sale Modified Successfully.."
    
    posList=[]
    posFields=['PointOfSale','Code','Active']
    return render(request,'hotel/master/master_pos.html',{'POSList':posList,'POSFields':posFields,'msg':msg})

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
        return records

@csrf_exempt
def Bind_POS_master_name(request):
    if request.method == 'POST' or request.is_ajax():
        pos = sp_get_by_param('sp_GetCountryCityFromHotels',[13,0])
        data = {
            'pos': pos,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def Bind_sup_name_by_city(request):
    if request.method == 'POST' or request.is_ajax():
        city_id =   request.POST['city_id']
        supplier = sp_get_by_param('sp_GetCountryCityFromHotels',[20,city_id])
        data = {
            'supplier': supplier,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Delete_POS_master_name(request):
    

    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        
        htls_grp_main_dtls = PointOfSaleMaster.objects.filter(id=id).delete()
        pos = sp_get_by_param('sp_GetCountryCityFromHotels',[13,0])
        data = {
            'pos': pos,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_board_master_name(request):
    if request.method == 'POST' or request.is_ajax():
        board = sp_get_by_param('sp_GetCountryCityFromHotels',[14,0])
        data = {
            'board': board,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Delete_Board_master_name(request):
    

    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        
        htls_grp_main_dtls = BoardTypeMaster.objects.filter(id=id).delete()
        board = sp_get_by_param('sp_GetCountryCityFromHotels',[14,0])
        data = {
            'board': board,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_airport_master_name(request):
    if request.method == 'POST' or request.is_ajax():
        country = sp_get_by_param('sp_GetCountryCityFromHotels',[11,0])
        city = sp_get_by_param('sp_GetCountryCityFromHotels',[16,0])
        ap = sp_get_by_param('sp_GetCountryCityFromHotels',[15,0])
        data = {
            'country': country,
            'city': city,
            'ap': ap,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Delete_Airport_master_name(request):
    

    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
       
        htls_grp_main_dtls = AirportCodeMaster.objects.filter(id=id).delete()
        country = sp_get_by_param('sp_GetCountryCityFromHotels',[11,0])
        city = sp_get_by_param('sp_GetCountryCityFromHotels',[16,0])
        ap = sp_get_by_param('sp_GetCountryCityFromHotels',[15,0])
        data = {
            'country': country,
            'city': city,
            'ap': ap,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Bind_Country_master_name(request):
    if request.method == 'POST' or request.is_ajax():
        country = sp_get_by_param('sp_GetCountryCityFromHotels',[12,0])
        data = {
            'country': country,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Delete_Country_master_name(request):
    

    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        
        htls_grp_main_dtls = CountryMaster.objects.filter(id=id).delete()
        country = sp_get_by_param('sp_GetCountryCityFromHotels',[12,0])
        data = {
             'country': country,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_Hotel_master_name(request):
    if request.method == 'POST' or request.is_ajax():
        city_id = request.POST['city_id']
        supplier_ids = request.POST['supplier_id']
        # supplier_id = ','.join(supplier_ids)
        htls = sp_get_by_param('sp_GetCountryCitySupplierFromHotels',[city_id,supplier_ids])
        
        data = {
            'hotel': htls,
            
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_Hotel_master_country_name(request):
    if request.method == 'POST' or request.is_ajax():
        country = sp_get_by_param('sp_GetCountryCityFromHotels',[1,0])
        city = sp_get_by_param('sp_GetCountryCityFromHotels',[17,0])
        star = sp_get_by_param('sp_GetCountryCityFromHotels',[8,1])
        htls_status = sp_get_by_param('sp_GetCountryCityFromHotels',[19,0])
        # supplier = sp_get_by_param('sp_GetCountryCityFromHotels',[20,0])
        data = {
            'country': country,
            'city' :city,
            'star' :star,
            'htls_status':htls_status
            # 'supplier':supplier
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Bind_Hotel_master_city_name(request):
    if request.method == 'POST' or request.is_ajax():
        country_id = request.POST['country_id']
        city = sp_get_by_param('sp_GetCountryCityFromHotels',[3,country_id])
        data = {
            'city': city,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def Bind_city_master_name(request):
    if request.method == 'POST' or request.is_ajax():
        city = sp_get_by_param('sp_GetCountryCityFromHotels',[10,0])
        country = sp_get_by_param('sp_GetCountryCityFromHotels',[11,0])
        data = {
            'city': city,
            'country' : country
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Delete_City_master_name(request):
    

    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
       
        htls_grp_main_dtls = CityMaster.objects.filter(id=id).delete()
        city = sp_get_by_param('sp_GetCountryCityFromHotels',[10,0])
        data = {
             'city': city,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def update_Hotel_master(request):
    if request.method == 'POST' or request.is_ajax():
        city_id = request.POST['ed_HotelCity']
        hotelObj=HotelMaster.objects.filter(id=request.POST['ed_referenceNo']).update(
                                            website_hotel_id=request.POST['ed_HotelID'],
                                            name=request.POST['ed_HotelName'],
                                            address1=request.POST['ed_HotelAdd1'],
                                            city=CityMaster.objects.get(id=request.POST['ed_HotelCity']),
                                            star_rating = StarRatingMaster.objects.get(id=request.POST['ed_Star']) ,
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            post_code=request.POST['ed_PinCode'],
                                            created_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                            created_date=timezone.now(),
                                            modified_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                            modified_date=timezone.now(),
                                            Longitude = request.POST['ed_Long'],
                                            Latitude = request.POST['ed_Lat'],
                                            ContractManager = request.POST['ed_Contract'],
                                            DemandGroup = request.POST['ed_Demand'],
                                            YieldManager = request.POST['ed_Yield'],
                                            HotelStatusId = request.POST['drp_htls_status']
                                            
                                            )
        
        htls = sp_get_by_param('sp_GetCountryCityFromHotels',[6,city_id])
        data = {
            'htls': htls,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Add_New_Hotel_master(request):
    if request.method == 'POST' or request.is_ajax():
        
        if HotelMaster.objects.filter(website_hotel_id = request.POST['ed_HotelID']):
                msg = "Sorry Hotel ID is already Exist"
                htls=[]
        else:
            hotelObj=HotelMaster(website_hotel_id=request.POST['ed_HotelID'],
                                name=request.POST['ed_HotelName'],
                                address1=request.POST['ed_HotelAdd1'],
                                city=CityMaster.objects.get(id=request.POST['ed_HotelCity']),
                                star_rating = StarRatingMaster.objects.get(id=request.POST['ed_Star']) ,
                                _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                post_code=request.POST['ed_PinCode'],
                                created_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                created_date=timezone.now(),
                                modified_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                modified_date=timezone.now(),
                                Longitude = request.POST['ed_Long'],
                                Latitude = request.POST['ed_Lat'],
                                ContractManager = request.POST['ed_Contract'],
                                DemandGroup = request.POST['ed_Demand'],
                                YieldManager = request.POST['ed_Yield'],
                                HotelStatusId = request.POST['drp_htls_status'],
                                competitorId = 1
                                
                                )
            hotelObj.save()
            msg="Hotel Added Successfully...."
            htls = sp_get_by_param('sp_GetCountryCityFromHotels',[6,request.POST['ed_HotelCity']])
        data = {
            'htls': htls,
             'msg':msg
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Delete_Hotel_master_name(request):
    

    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        
        htls_grp_main_dtls = HotelMaster.objects.filter(id=id).delete()
        city_id = request.POST['city_id']
        sup_id = request.POST['sup_id']
        # htls = sp_get_by_param('sp_GetCountryCityFromHotels',[6,city_id])
        htls = sp_get_by_param('sp_GetCountryCitySupplierFromHotels',[city_id,sup_id])
        data = {
            'hotel': htls,
            
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

def master_hotel(request):
    msg=None
    if request.method=='POST':
        '''
        '''
        if request.POST['ed_referenceNo']=='':
            if HotelMaster.objects.filter(website_hotel_id = request.POST['ed_HotelID']):
                msg = "Sorry Hotel ID is already Exist"
            else:
                hotelObj=HotelMaster(website_hotel_id=request.POST['ed_HotelID'],
                                    name=request.POST['ed_HotelName'],address1=request.POST['ed_HotelAdd1'],address2=request.POST['ed_HotelAdd2'],
                                    city=CityMaster.objects.get(id=request.POST['ed_HotelCity']),
                                    brand=request.POST['ed_Brand'],
                                    star_rating = StarRatingMaster.objects.get(id=request.POST['ed_Star']) ,
                                    _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                    post_code=request.POST['ed_PinCode'],match_status=request.POST['ed_MatchStatus'],
                                    description=request.POST['ed_Description'],is_processed=request.POST['ed_IsProcessed'],
                                    match_hotel_name=request.POST['ed_MatchHotelName'],dipbag_sync_id=request.POST['ed_DipBagSyncId'],
                                    is_mailed=request.POST['ed_IsMailed1'],is_mailed1=request.POST['ed_IsMailed'],
                                    created_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                    created_date=timezone.now(),
                                    modified_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                    modified_date=timezone.now())
                hotelObj.save()
                msg="Hotel Added Successfully...."
        else:
            hotelObj=HotelMaster.objects.filter(id=request.POST['ed_referenceNo']).update(website_hotel_id=request.POST['ed_HotelID'],
                                            name=request.POST['ed_HotelName'],address1=request.POST['ed_HotelAdd1'],address2=request.POST['ed_HotelAdd2'],
                                            # city=CityMaster.objects.get(name=request.POST['ed_HotelCity']),
                                            city=request.POST['ed_HotelCity'],
                                            brand=request.POST['ed_Brand'], 
                                            star_rating=request.POST['ed_Star'],
                                            _active=1 if request.POST['ed_activeValue']=='Active' else 0,
                                            post_code=request.POST['ed_PinCode'],match_status=request.POST['ed_MatchStatus'],
                                            description=request.POST['ed_Description'],is_processed=request.POST['ed_IsProcessed'],
                                            match_hotel_name=request.POST['ed_MatchHotelName'],dipbag_sync_id=request.POST['ed_DipBagSyncId'],
                                            is_mailed=request.POST['ed_IsMailed1'],is_mailed1=request.POST['ed_IsMailed'],
                                            modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                            modified_date=timezone.now())
                                            
            msg="Hotel Modified Successfully...."
    # hotelList=[[i.website_hotel_id,i.name,i.address1,i.address2,i.city.name,i.brand,StarRatingMaster.objects.get(id=i.star_rating_id).starrating,
                # i.post_code,i.match_status,i.description, i.is_processed,i.match_hotel_name,
                # i.dipbag_sync_id,i.is_mailed,i.is_mailed1,i.active,i.id] for i in HotelMaster.objects.order_by("-id")[:500]]
    hotelList = []
    hotelFields=['HotelID','Name','City','Rating','PINCode','Active']
    cityList=[]
    
    return render(request,'hotel/master/master_hotel.html',{'HotelList':hotelList,'CityList':cityList, 'HotelFields':hotelFields,'msg':msg})

   
def sp_get(sp_name):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                        user=settings.DATABASES['default']['USER'],
                        passwd=settings.DATABASES['default']['PASSWORD'],
                        db=settings.DATABASES['default']['NAME'])
        cursor = db.cursor()
        cursor.callproc(procname=sp_name)
        records = cursor.fetchall()
        cursor.close()
        return records

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
        records = cursor.fetchall()
        cursor.close()
        return records


@csrf_exempt
def Download_hotel_master(request):
    if request.method == 'POST' or request.is_ajax():
        country_id = int(request.POST['country'])
        city_id = request.POST['city']
        supplier_ids = request.POST['supplier']
        # supplier_id = ','.join(supplier_ids)
        hotels = sp_get_by_param('sp_GetCountryCitySupplierFromHotels', [city_id, supplier_ids])
        countryname = CountryMaster.objects.get(id=country_id).name
        list1 = []
        path = ""

        for hotel in hotels:
            print('Hotel = ', hotel)
            dict1 = {"Country": countryname, "City": hotel[2], "Supplier": hotel[17], "WebSiteHotelId": hotel[6], "Hotel Name": hotel[1]}
            list1.append(dict1)

        if len(list1) > 0:
            df = pd.DataFrame(list1)
            time = 'Hotel_master_download_excel_%s' % timezone.now() + ''
            path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Download_hotel_master/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1',
                        columns=['Country', 'City', 'Supplier', 'WebSiteHotelId', 'Hotel Name'], index=False)
            writer.save()
            path = '/static/Excel_file_Download_hotel_master/%s' % time + '.xlsx'
        return JsonResponse({"msg": "Excel file generated successfully", "results": list1, "path": path})

    return JsonResponse({"msg": "Invalid Method", "results": [], "path": ""})

    
@csrf_exempt
def Hotel_master_upload_excel(request):
    if request.method == 'GET' or request.is_ajax():
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        count =len(dataFrame.columns)
        if (count ==19 and dataFrame.columns[0]=='Website hotel code' and dataFrame.columns[2]=='Star rating'
                and dataFrame.columns[1]=='Hotelname' and dataFrame.columns[5]=='Country name'):
            table_name = 'temphotelmaster_excel'
            temphotelmaster.objects.all().delete()
            
            import sqlalchemy
            database_username = settings.DATABASES['default']['USER']
            database_password = settings.DATABASES['default']['PASSWORD']
            database_ip       = settings.DATABASES['default']['HOST']
            database_name     = settings.DATABASES['default']['NAME']
            database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(database_username, database_password, 
                                                        database_ip, database_name))
            dataFrame.to_sql(con=database_connection, name= table_name, if_exists='append')
            lst = [1,request.session['UserID']]
            sp_res_1 = aetos_SP_all_operation_genric('spExcelUploadHotelMaster',lst)
            list1 = []
            dict1 = {}
            for Sp_res in sp_res_1:
                dict1 = {"Websitehotelcode": Sp_res[0], "Hotelname": Sp_res[1], "StarRating" : Sp_res[2], "Address1" : Sp_res[3],  "Country_code" : Sp_res[4],"Country_name" : Sp_res[5], "Updated_Country_name" : Sp_res[6], "Zip_code" : Sp_res[7],"longitude" : Sp_res[8],"latitude" : Sp_res[9], "city_code" : Sp_res[10], "city_name" : Sp_res[11], "updatedcityname" : Sp_res[12], "hotelstatus" : Sp_res[13], "ErrorStatus": Sp_res[14]}
                list1.append(dict1)
            if len(list1) > 0:
                df = pd.DataFrame(list1)
                time = 'Hotel_master_error_output_excel_%s' % timezone.now() + ''
                path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                writer = pd.ExcelWriter(path)
                df.to_excel(writer, 'Sheet1', columns=['Websitehotelcode', 'Hotelname','StarRating', 'Address1','Country_code', 'Country_name','Updated_Country_name',  'Zip_code', 'longitude', 'latitude', 'city_code', 'updatedcityname', 'hotelstatus' , 'ErrorStatus'], index=False)
                writer.save()
                path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                count=len(list1)
            else :
                    count= "0"
                    path=""
            
            data = {
                    'htl_grp_dtls': "file uploded successfully",
                    'Path':path,
                    'count':count,
                    'error':'0',
            }
            os.remove(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
            return JsonResponse(data, safe=False)

        else :
            data = {
                'error':'1',
                'htl_grp_dtls': "Excel file template are not matched !!!",
            }
            return JsonResponse(data, safe=False)

    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Country_master_upload_excel(request):
    if request.method == 'GET' or request.is_ajax():
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        count =len(dataFrame.columns)
        if (count ==4 and dataFrame.columns[0]=='CountryName' and dataFrame.columns[2]=='TimeZone'
                and dataFrame.columns[1]=='CountryCode' and  dataFrame.columns[3]=='Status'):
            list1 = []
            dict1 = {}
            suucc_count =0
            dataFrame = dataFrame.replace(np.nan, '', regex=True)
            for item in dataFrame.values.tolist():
                if(not (item[0] == '') and not (item[1] == '') and not (item[3] == '') and  (item[3]==0 or item[3]==1)):
                    if CountryMaster.objects.filter(code = item[1]):
                            dict1 = {"CountryName": item[0], "CountryCode": item[1],"TimeZone": item[2], "Status" : item[3],"ErrorStatus":"Sorry CountryCode  is already Exist" }
                            list1.append(dict1)
                    elif  CountryMaster.objects.filter(name__iexact = item[0].lower()):
                            dict1 = {"CountryName": item[0], "CountryCode": item[1],"TimeZone": item[2], "Status" : item[3],"ErrorStatus":"Sorry "+ item[0]+"   is already Exist in system" }
                            list1.append(dict1)
                    else:
                        countryObj=CountryMaster(name=item[0],code=item[1],
                                        timezone=item[2],
                                        _active=item[3])
                        countryObj.save()
                        suucc_count =suucc_count+1
                else:
                    dict1 = {"CountryName": item[0], "CountryCode": item[1],"TimeZone": item[2], "Status" : item[3],"ErrorStatus":"Please check your input" }
                    list1.append(dict1)
            if len(list1) > 0:
                df = pd.DataFrame(list1)
                time = 'country_master_error_output_excel_%s' % timezone.now() + ''
                path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                writer = pd.ExcelWriter(path)
                df.to_excel(writer, 'Sheet1', columns=['CountryName', 'CountryCode','TimeZone','Status', 'ErrorStatus'], index=False)
                writer.save()
                path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                count=len(list1)
            else :
                    count= "0"
                    path=""
            country = sp_get_by_param('sp_GetCountryCityFromHotels',[12,0])
            data = {
                    'htl_country_dtls': " out of  "+str( dataFrame.shape[0])+"  records  "+ str(suucc_count)+"  records inserted successfully ,  "+str(dataFrame.shape[0]-suucc_count)+" records failed !!!",
                    'Path':path,
                    'count':count,
                    'error':'0',
                    'country':country
            }
            os.remove(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
            return JsonResponse(data, safe=False)

        else :
            data = {
                'error':'1',
                'htl_country_dtls': "Excel file template are not matched !!!",
            }
            return JsonResponse(data, safe=False)

    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

  

    
@csrf_exempt
def Pos_master_upload_excel(request):
    if request.method == 'GET' or request.is_ajax():
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        count =len(dataFrame.columns)
        if (count ==3 and dataFrame.columns[0]=='Point of sale' and dataFrame.columns[2]=='Status'
                and dataFrame.columns[1]=='Code' ):
            list1 = []
            dict1 = {}
            suucc_count =0
            dataFrame = dataFrame.replace(np.nan, '', regex=True)
            for item in dataFrame.values.tolist():
                if(not (item[0] == '') and not (item[1] == '') and  not (item[2] == '') and  (item[2]==0 or item[2]==1)):
                    if PointOfSaleMaster.objects.filter(code = item[1]):
                            dict1 = {"Point of sale": item[0], "Code": item[1], "Status" : item[2],"ErrorStatus":"Sorry Point of Sale Code is already Exist" }
                            list1.append(dict1)
                    else:
                        posObj=PointOfSaleMaster(point_of_sale=item[0],
                                                    code=item[1],
                                                    _active= item[2],
                                                    created_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                                    created_date=timezone.now(),
                                                    modified_by=UserMaster.objects.get(User_ID=request.user.User_ID),
                                                    modified_date=timezone.now())
                        posObj.save()
                        suucc_count =suucc_count+1
                else:
                    dict1 = {"Point of sale": item[0], "Code": item[1], "Status" : item[2],"ErrorStatus":"Please check your input" }
                    list1.append(dict1)
            if len(list1) > 0:
                df = pd.DataFrame(list1)
                time = 'pos_master_error_output_excel_%s' % timezone.now() + ''
                path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                writer = pd.ExcelWriter(path)
                df.to_excel(writer, 'Sheet1', columns=['Point of sale', 'Code','Status', 'ErrorStatus'], index=False)
                writer.save()
                path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                count=len(list1)
            else :
                    count= "0"
                    path=""
            pos = sp_get_by_param('sp_GetCountryCityFromHotels',[13,0])
            data = {
                    'htl_pos_dtls': " out of  "+str( dataFrame.shape[0])+"  records  "+ str(suucc_count)+"  records inserted successfully ,  "+str(dataFrame.shape[0]-suucc_count)+" records failed !!!",
                    'Path':path,
                    'count':count,
                    'error':'0',
                    'pos':pos
            }
            os.remove(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
            return JsonResponse(data, safe=False)

        else :
            data = {
                'error':'1',
                'htl_pos_dtls': "Excel file template are not matched !!!",
            }
            return JsonResponse(data, safe=False)

    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

    
@csrf_exempt
def City_master_upload_excel(request):
    if request.method == 'GET' or request.is_ajax():
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        count =len(dataFrame.columns)
        if (count ==4 and dataFrame.columns[0]=='City Name'  and dataFrame.columns[1]=='City Code'
               and dataFrame.columns[2]=='Country Name'
               and dataFrame.columns[3]=='Status' ):
            list1 = []
            dict1 = {}
            suucc_count =0
            dataFrame = dataFrame.replace(np.nan, '', regex=True)
            for item in dataFrame.values.tolist():
                if(not (item[0] == '') and not (item[1] == '') and  not (item[2] == '') and  (item[3]==0 or item[3]==1)):
                    if CityMaster.objects.filter(code = item[1]):
                            dict1 = {"City Name": item[0], "City Code": item[1], "Country Name" : item[2],"Status" : item[3],"ErrorStatus":"Sorry city Code is already Exist" }
                            list1.append(dict1)
                    else:
                        countryid =CountryMaster.objects.filter(name=item[2]).values("id")
                        if(countryid):
                            
                            if (len(str(item[1]))<11):
                                cityObj=CityMaster(name=item[0],
                                        code=item[1],
                                        country_id= countryid[0]["id"],
                                        _active = item[3],
                                        created_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                        created_date=timezone.now(),
                                        modified_by=UserMaster.objects.get(User_ID=request.session['UserID']),
                                        modified_date=timezone.now())
                                cityObj.save()
                                suucc_count =suucc_count+1
                            else :
                                dict1 = {"City Name": item[0], "City Code": item[1], "Country Name" : item[2],"Status" : item[3],"ErrorStatus":""+ item[1]+" city code should be less than 11 character " }
                                list1.append(dict1)
                        else:
                            dict1 = {"City Name": item[0], "City Code": item[1], "Country Name" : item[2],"Status" : item[3],"ErrorStatus":""+ item[2]+" Country not present in database" }
                            list1.append(dict1)
                else:
                    dict1 = {"City Name": item[0], "City Code": item[1], "Country Name" : item[2],"Status" : item[3],"ErrorStatus":"Please check your inputs !!" }
                    list1.append(dict1)
            if len(list1) > 0:
                df = pd.DataFrame(list1)
                time = 'city_master_error_output_excel_%s' % timezone.now() + ''
                path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                writer = pd.ExcelWriter(path)
                df.to_excel(writer, 'Sheet1', columns=['City Name', 'City Code','Country Name', 'Status',"ErrorStatus"], index=False)
                writer.save()
                path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                count=len(list1)
            else :
                    count= "0"
                    path=""
            city = sp_get_by_param('sp_GetCountryCityFromHotels',[10,0])
            data = {
                    'htl_city_dtls': " out of  "+str( dataFrame.shape[0])+"  records  "+ str(suucc_count)+"  records inserted successfully ,  "+str(dataFrame.shape[0]-suucc_count)+" records failed !!!",
                    'Path':path,
                    'count':count,
                    'error':'0',
                    'city':city
            }
            os.remove(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
            return JsonResponse(data, safe=False)

        else :
            data = {
                'error':'1',
                'htl_city_dtls': "Excel file template are not matched !!!",
            }
            return JsonResponse(data, safe=False)

    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

     

     


