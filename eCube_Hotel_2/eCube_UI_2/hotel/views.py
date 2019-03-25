# Package Imports
import os
import json
import pymysql
import csv
import calendar
import datetime
import pandas as pd
import numpy as np
import requests
from io import StringIO
from time import strptime
from functools import reduce
from pdb import set_trace as st
from pymongo import MongoClient
from django.db.models import Q
from django.utils import timezone

# App Imports
from hotel.utils import (AjaxFileUploader, dates_between, AetosResponse, ExcelBatchUploadHandler, ServiceCallHandler,
                        dailySchedular,weeklySchedular,monthlySchedular,onceSchedular)

from hotel.master.models import (AirportCodeMaster, CityMaster, CountryMaster, HotelMaster, CompetitorMaster,
                                 RoomTypeMaster, StarRatingMaster, BoardTypeMaster, BookingPeriodMaster,
                                 RequestModeMaster,UserMaster,FieldGroupMaster)

from hotel.models import (HotelPOS, HotelFlightRequestsDateDetail, HotelFlightRequestInputDetail, FlightSearchType,
                          HotelRequestInputDetail, HotelRequestsDateDetail, HotelFlightRequestsDateDetail, RequestMaster,
                          ScheduleDate, ScheduleMaster, ScheduleTypeMaster, KeywordRule, HotelStandardization,
                          HotelNameSpecialChars, Competitor, HotelGroup, HotelGroupDetail, Cities, Hotels,
                          teamLeadtime, teamLeadtime_adhoc,batchcrawldata,Filed_master,Filed_group_mapping_detail,teammatchunmatched,temp_hotel_only,temp_hotel_Flight)

from hotel.user_management.models import BliMaster

# Django Imports
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, render_to_response
from functools import reduce
from os import listdir
from os.path import isfile, join



class VisibleDomain:

    def __init__(self,bliId):
        self.bliId = bliId
        print("BLIIIII",bliId)

    def getDomain(self,request):
        supList = getattr(settings,settings.MAPPING[self.bliId])
        if supList:
            print("Domains******",supList)
            return supList
        else:
            self.populateDomain(request)

        return self.getDomain(request)


    def populateDomain(self,request):
        bli_id = dict(request.session)['bli_id']
        Crawlersfiles = [f for f in listdir('/home/tech/AetosQueue/Crawling/scripts/'+settings.BLI_SCRIPT_DIR[bli_id]+'') if isfile(join('/home/tech/AetosQueue/Crawling/scripts/'+settings.BLI_SCRIPT_DIR[bli_id]+'', f))]
        populateSup = list()
        print("Crawlersfiles***********",Crawlersfiles)
        if Crawlersfiles:

            suppliers = []
            for i in Crawlersfiles:
                suppliers.append(sp_get_by_param('sp_Get_Supplier_Name', i))

            for i in suppliers:
                for j in i:
                    dicsuppliers = {}
                    dicsuppliers['id'] = j[0]
                    dicsuppliers['Name'] = j[1]
                    populateSup.append(dicsuppliers)
        setattr(settings, settings.MAPPING[self.bliId], populateSup)


# Create your views here.
def index(request, request_id = None):
  
    if request.method == 'GET':
        if request_id:
            request.session['requestid'] = request_id
        else:
            if 'requestid' in request.session:
                del request.session['requestid']
            if 'batch_items' in request.session:
                del request.session['batch_items']
            if 'request_title' in request.session:
                del request.session['request_title']
            if 'request_description' in request.session:
                del request.session['request_description']
        context = {}
        if request_id:
            flag = 1
            if request_id == 'excel_upload':
                request_ids = request.session['batch_items']
                requests = RequestMaster.objects.filter(id__in=request_ids).order_by('-id')
                request_id = request_ids[0]
                request.session['requestid'] = request_id
            else:
                requests = RequestMaster.objects.filter(id=request_id).order_by('-id')

            hotelrequestinputs = HotelRequestInputDetail.objects.filter(requests__in=requests)
            request.session['request_title'] = requests.first().title
            request.session['request_description'] = requests.first().description


            data_list = []
            for hf in hotelrequestinputs:
                serialise_data = {}
                if hf.hotels_id != None :
                    serialise_data = lambda  hr, hri: {

                        'id': hri.id,
                        'hotel_request': {
                            'request_title': hr.title,
                            'request_desc': hr.description
                        },
                        'booking': {
                            'pos' : hri.pointofsales.id,
                            'adult_count': hri.adults,
                            'children_count': hri.children,
                            'country' :hri.countries.id,
                            'city': hri.cities.id,
                            'hotel': ",".join([str(hri.hotels.id)]),
                            'room_type': hri.roomtype,
                            'board_type': hri.boardtype,
                            'star_rating': hri.starrating,
                            'suppliers': hri.suppliers,
                            'no_of_nights': hri.rentallength,
                            'bookingperiods' : hri.bookingperiods_id,
                            'id' : hri.id,
                            'batch_id' : hri.requests.id
                        },
                        'crawl': {'mode': hri.crawlmode},
                        'airport': {'to': 'IN', 'from': 'BGI'},
                        'country': { 'pos': hri.pointofsales.posale},
                        'country_id': {'to': hri.countries.name, 'from': hri.cities.name,'hotel_name':hri.hotels.name}
                    }


                    data_list.append([serialise_data(sub_req.requests, sub_req) for sub_req in hotelrequestinputs if sub_req.id == hf.id])
                else:
                    serialise_data = lambda  hr, hri: {

                        'id': hri.id,
                        'hotel_request': {
                            'request_title': hr.title,
                            'request_desc': hr.description
                        },
                        'booking': {
                            'pos' : hri.pointofsales.id,
                            'adult_count': hri.adults,
                            'children_count': hri.children,
                            'country' :hri.countries.id,
                            'city': hri.cities.id,
                            'room_type': hri.roomtype,
                            'board_type': hri.boardtype,
                            'star_rating': hri.starrating,
                            'suppliers': hri.suppliers,
                            'no_of_nights': hri.rentallength,
                            'bookingperiods' : hri.bookingperiods_id,
                            'id' : hri.id,
                            'batch_id' : hri.requests.id
                        },
                        'crawl': {'mode': hri.crawlmode},
                        'airport': {'to': 'IN', 'from': 'BGI'},
                        'country': { 'pos': hri.pointofsales.posale},
                        'country_id': {'to': hri.countries.name, 'from': hri.cities.name}
                    }

                    data_list.append([serialise_data(sub_req.requests, sub_req) for sub_req in hotelrequestinputs if sub_req.id == hf.id])

                for i in data_list:
                    for x in i :
                        if hf.bookingperiods_id == 1:
                            if x['id'] == hf.id:

                                x['booking']['week_days'] = hf.DaysOfWeek
                                x['booking']['fromdate'] = hf.fromdate.strftime('%m/%d/%Y')
                                x['booking']['todate'] = hf.todate.strftime('%m/%d/%Y')
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''

                        elif hf.bookingperiods_id == 2:

                            if x['id'] == hf.id:

                                x['booking']['advance_dates'] = hf.advancedates
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''

                        elif hf.bookingperiods_id == 3:

                            if x['id'] == hf.id:

                                x['booking']['advance_dates'] = hf.advancedates
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''



                        else:

                            if x['id'] == hf.id:

                                x['booking']['advance_dates'] = hf.advancedates
                                x['booking']['week_days'] = hf.DaysOfWeek

                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''




            hidden_data_list = data_list[:3]
            show_data_list = data_list[3:]
            context.update({
                'data_list': data_list,
                'hidden_data_list':hidden_data_list,
                'show_data_list':show_data_list,
                'data_list_count': len(data_list)
            })
            if len(context['data_list']) != 0:
                lists = reduce(lambda x,y: x+y,context['data_list'])
                context_string = json.dumps({c['id']: c for c in lists.copy()})
                context.update({'json_string': context_string})
            if request.session.get('batch_items'):
                context.update(
                    {'batch_items': RequestMaster.objects.filter(id__in=request.session['batch_items']).order_by('-id'),
                     'selected_request_id': int(request_id)
                     }
                )
        else:
            flag = 0

        posales = HotelPOS.objects.filter(
            _active=True).values('id', 'posale')
        dicposales = {}
        for i in posales:
            dicposales[i['id']] = i['posale']

        countries = CountryMaster.objects.filter(_active=True).values(
            'id', 'name').order_by('name')

        diccountries = {}
        for i in countries:
            diccountries[i['id']] = i['name']

        roomtypes = RoomTypeMaster.objects.filter(
            _active=True).values('id', 'roomtype')
        dicroomtypes = {}
        for i in roomtypes:
            dicroomtypes[i['id']] = i['roomtype']

        boardtypes = BoardTypeMaster.objects.filter(
            _active=True).values('id', 'boardtypedescription')
        dicboardtypes = {}

        for i in boardtypes:
            dicboardtypes[i['id']] = i['boardtypedescription']

        starratings = StarRatingMaster.objects.filter(
            _active=True).values('id', 'starrating')
        dic_starratings = {}

        for i in starratings:
            dic_starratings[i['id']] = i['starrating']

        hotels = []
        dichotels = {}
        for i in hotels:
            dichotels[i['id']] = i['name']

        bli_id = dict(request.session)['bli_id']
        obj = VisibleDomain(bli_id)

        supList = obj.getDomain(request)
        print("\n\n\n lasun supList")
        print(supList)

        context.update({
            'pointofsales': dicposales, 'countries': diccountries, 'roomtypes': dicroomtypes, 'boardtypes': dicboardtypes,
            'starratings': dic_starratings, 'suppliers':supList , 'hotels': dichotels, "flag": flag
        })

        return render(request, 'hotel/hotel_create_request.html', context)


@csrf_exempt
def HotelDeleteRequest(request):
    if request.method == 'POST' and request.is_ajax():  
       
        deleteId = request.POST['deletereqId']

        HotReId = HotelRequestInputDetail.objects.get(id=deleteId)
        reqMasterId = HotReId.requests.id
        HotelRequestsDateDetail.objects.filter(hotelrequestinputdetailsid = deleteId).delete()
        HotelRequestInputDetail.objects.filter(id=deleteId).delete()
        context = {
        "Message": "Request deleted successfully", "delete_id": reqMasterId
        }
        return JsonResponse(context)


@csrf_exempt
def HotelDeleteRequestAll(request):
    if request.method == 'POST' and request.is_ajax():
        deleteId = request.POST['deletereqId']

        sub_requests = HotelRequestInputDetail.objects.filter(requests__id=deleteId).distinct()
        sub_request_ids = list(sub_requests.values_list('id', flat=True))
        HotelRequestsDateDetail.objects.filter(hotelrequestinputdetailsid__in=sub_request_ids).delete()
        sub_requests.delete()
        context = {
            "Message": "Request deleted successfully", "delete_id": deleteId
        }
        return JsonResponse(context)


@csrf_exempt
def BindCities(request):
    if request.method == 'POST' and request.is_ajax():
        
        if json.loads(request.POST['CountryId']) == '' or json.loads(request.POST['CountryId']) == None:
            pass
        else:
            countryid = int(json.loads(request.POST['CountryId']))
        context = {}
        try:
            country = CountryMaster.objects.get(id=countryid)
           
        except:
            context = {
                "cities": ""
            }
            return JsonResponse(context)
        cities = list(CityMaster.objects.filter(country=country, _active=True).values(
            'id', 'name').order_by('name'))
        context = {
            "cities": cities
        }
        return JsonResponse(context)


@csrf_exempt
def BindHotels(request):
    if request.method == 'POST' and request.is_ajax():
        # if "UserID" in request.session:
        CityId = json.loads(request.POST['CityId'])
        if CityId != '0':

            Cityobject = CityMaster.objects.get(id=CityId)
            hotels = list(HotelMaster.objects.filter(city=Cityobject,competitorId = 1,_active=True).values('id', 'name'))
          
            if hotels:
                hotels = hotels
            else:
                hotels = ''
            context = {
                "Hotels": hotels
            }
            return JsonResponse(context)

@csrf_exempt
def allHotels(request):
    if request.method == 'POST' and request.is_ajax():
        # if "UserID" in request.session:
        reqtId = json.loads(request.POST['reqt_Id'])
        if reqtId != '':
            hotelrequestinputs = HotelRequestInputDetail.objects.filter(requests=reqtId).exclude(hotels__isnull=True)
            hotels = []
            allHotels = {}
            
            for i in hotelrequestinputs:
               
                allHotels[i.hotels.id] = i.hotels.name

            if allHotels:
                hotels = allHotels
            else:
                hotels = ''
            context = {
                "Hotels": hotels
            }
            return JsonResponse(context)

@csrf_exempt
def FlightBindHotels(request):
    if request.method == 'POST' and request.is_ajax():
          
        airportCode = json.loads(request.POST['AirportId'])
    
        airportObject =  AirportCodeMaster.objects.get(id = airportCode)
     
        Cityobject = CityMaster.objects.get(id=airportObject.city.id)

        hotels = list(HotelMaster.objects.filter(city=Cityobject,competitorId = 1,_active=True).values('id', 'name'))
        
        if hotels:
            hotels = hotels
        else:
            hotels = ''
        context = {
            "Hotels": hotels
        }
        return JsonResponse(context)


@csrf_exempt
def BindAirports(request):
    if request.method == 'POST' and request.is_ajax():
        if json.loads(request.POST['CityId']) == '' or json.loads(request.POST['CityId']) == None:
            pass
        else:
            cityid = int(json.loads(request.POST['CityId']))

        context = {}
        try:
            city = CityMaster.objects.get(id=cityid)

        except:
            context = {
                "airports": ""
            }
            return JsonResponse(context)
        airports = list(
            AirportCodeMaster.objects.filter(city=city, _active=True).values('id', 'code').order_by('name'))

        context = {
            "airports": airports
        }
        return JsonResponse(context)


@csrf_exempt
def HotelSaveRequest(request):
    if request.method == 'POST' and request.is_ajax():
            

        # if "UserID" in request.session:
            requestmodel = json.loads(request.POST['requestmodel'])
            destinationmodel = json.loads(request.POST['destinationmodel'])
            daterangemodel = json.loads(request.POST['daterangemodel'])
            upload_file = request.FILES.get('upload_file', None)
    
            requestname = requestmodel['requestname']
            requestdesc = requestmodel['requestdesc']
            requesthotel = RequestModeMaster.objects.get(id=2)  # HotelMaster Mode
            req_id=requestmodel['hotel_req_id']        

           

            if req_id != None and req_id != '':

                #print('\nhotel id "%s" exists\n' % str(req_id))
                HotReId = HotelRequestInputDetail.objects.get(id=req_id)
                reqMasterId = HotReId.requests.id
                
                RequestMaster.objects.filter(id=reqMasterId).update(title=requestname,
                description=requestdesc, requestmodeid=requesthotel, author=request.user.User_ID)
                requestobject = RequestMaster.objects.get(id=reqMasterId)
                HotelRequestsDateDetail.objects.filter(hotelrequestinputdetailsid = req_id).delete()
                HotelRequestInputDetail.objects.filter(id=req_id).delete()
                save_hotel(requestobject,requestmodel,destinationmodel,daterangemodel,upload_file,request)
                flag = 1

            elif request.session.get('requestid'):

                req_master_id = request.session.get('requestid')
                #print('\nrequest id "%s" exists in session \n' % str(req_master_id))
                RequestMaster.objects.filter(id=req_master_id).update(title=requestname,
                description=requestdesc, requestmodeid=requesthotel, author=request.user.User_ID)
                requestobject = RequestMaster.objects.get(id=req_master_id)
                save_hotel(requestobject,requestmodel,destinationmodel,daterangemodel,upload_file,request)
                flag = 0
  
            else:
                #print('\nfresh request\n')
                requestmaster = RequestMaster.objects.create(
                    title=requestname, description=requestdesc, requestmodeid=requesthotel, author=request.user.User_ID,
                    BLI_id=request.session.get('bli_id')
                )
                request.session['requestid'] = requestmaster.id
                try:
                    requestobject = RequestMaster.objects.get(id=requestmaster.id)  # Fetch Request object
                except:  # Issue in Request Master
                    context = {"data": ""}
                    return JsonResponse(context)
                save_hotel(requestobject,requestmodel,destinationmodel,daterangemodel,upload_file,request)
                flag = 0
    context = {
        "Message": "Request created successfully", "flag": flag, "request_id": requestobject.id
    }
    return JsonResponse(context)


def save_hotel(requestobject,requestmodel,destinationmodel,daterangemodel,upload_file,request):

    bookingid = daterangemodel['BookingPeriod']

    pos = requestmodel['pos']
    adults = requestmodel['adults']
    children = requestmodel['children']
    all_hotel = requestmodel['all_hotel_val']


    FromDate = None
    ToDate = None
    CheckIndates = None
    CheckOutdates = None
    advancedates = None
    hotelrequestinputdetailsid = None

    country = destinationmodel['country']
    city = destinationmodel['city']
    crawlmode = destinationmodel['crawlmode']
    # hotels = destinationmodel['hotels']
    suppliers = daterangemodel['suppliers']
    if destinationmodel['roomtype'] :
        roomtype = destinationmodel['roomtype']
        roomtype = ''.join(roomtype)
    else:
        roomtype = ""
    if destinationmodel['boardtype']:
        boardtype = destinationmodel['boardtype']
        boardtype = ', '.join(boardtype)
    else:
        boardtype = ""
    if destinationmodel['starrating']:
        starrating = destinationmodel['starrating']
        starrating = ', '.join(starrating)
    else:
        starrating = ''

    if bookingid == 1:
        FromDate = datetime.datetime.strptime(
            daterangemodel['fromdate'], '%m/%d/%Y')
        ToDate = datetime.datetime.strptime(daterangemodel['todate'], '%m/%d/%Y')
        CheckIndates = daterangemodel['CheckIndates']['CheckInDates']
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']

    elif bookingid == 2:
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']
        advancedates = daterangemodel['CheckInDates']['CheckInDates']

    elif bookingid == 3:
        advancedates = daterangemodel['CheckInDates']['CheckInDates']
        advancedates1 = advancedates 
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']

    else:
        
        advancedates = daterangemodel['CheckInDates']['CheckInDates']
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']

    
    hotelpos = HotelPOS.objects.get(id=pos)
    CityObject = CityMaster.objects.get(id=city)
    CountryObject = CountryMaster.objects.get(id=country)
    bookingperiodobject = BookingPeriodMaster.objects.get(id=bookingid, _active=True)
    flag = True
    flag1= True
    bli_id_session = request.session.get('bli_id')
    if (bli_id_session=='1'):
        rpy_type= settings.HOTEL_BEDS_RPT_TYPE
    else :
        rpy_type= settings.HOTEL_BEDS_AVL_RPT_TYPE

    if all_hotel =="true":
        hotelobject = None        
        if advancedates is not None:
            if bookingid == 3 or bookingid == 4 or bookingid == 2:
                if flag == True:
                    advancedates = ', '.join(advancedates)
                    flag = False
        else:
            advancedates = None
        if CheckIndates is not None:
            
            if bookingid == 1 or bookingid == 4:
                if flag1 == True:
                    CheckIndates = ', '.join(CheckIndates)
                    flag1 = False
                    
        else:
            CheckIndates = None

        hotelRequestInputDetail = HotelRequestInputDetail.objects.create(requests=requestobject, bookingperiods=bookingperiodobject, pointofsales=hotelpos, adults=adults,
                                                                            children=children, crawlmode=crawlmode, hotels=hotelobject, advancedates=advancedates, cities=CityObject, countries=CountryObject,
                                                                            suppliers=', '.join(suppliers), fromdate=FromDate,starrating=starrating, boardtype=boardtype, roomtype=roomtype,
                                                                            todate=ToDate, DaysOfWeek=CheckIndates, rentallength=', '.join(CheckOutdates),reporttype=rpy_type)

    else:
        hotels, suppliers = get_hotels_suppliers_from_file(upload_file)
        for id in hotels:
            hotelobject = HotelMaster.objects.filter(website_hotel_id=id).first()
            if advancedates is not None:
                if bookingid == 3 or bookingid == 4 or bookingid == 2:
                    if flag == True:
                        advancedates = ', '.join(advancedates)
                        flag = False
            else:
                advancedates = None
            if CheckIndates is not None:
                
                if bookingid == 1 or bookingid == 4:
                    if flag1 == True:
                        CheckIndates = ', '.join(CheckIndates)
                        flag1 = False
                        
            else:
                CheckIndates = None

            hotelRequestInputDetail = HotelRequestInputDetail.objects.create(requests=requestobject, bookingperiods=bookingperiodobject, pointofsales=hotelpos, adults=adults,
                                                                                children=children, crawlmode=crawlmode, hotels=hotelobject, advancedates=advancedates, cities=CityObject, countries=CountryObject,
                                                                                suppliers=', '.join(suppliers), fromdate=FromDate,starrating=starrating, boardtype=boardtype, roomtype=roomtype,
                                                                                todate=ToDate, DaysOfWeek=CheckIndates, rentallength=', '.join(CheckOutdates),reporttype=rpy_type)
            hotelRequestInputDetail = HotelRequestInputDetail.objects.get(id=hotelRequestInputDetail.id)
            

            if bookingid == 1:  # Date Range
                for date in dates_between(FromDate, ToDate):
                    for chckindate in CheckIndates.split(', '):
                        if date.strftime('%a') == chckindate[0:3]:
                            for nngihts in list(map(int, CheckOutdates)):
                                checkoutdate = date + datetime.timedelta(days=nngihts)
                                HotelRequestsDateDetail.objects.create(
                                    hotelrequestinputdetailsid=hotelRequestInputDetail, checkindate=date.date(), checkoutdate=checkoutdate)

                
            elif bookingid == 2:  # Advance Days
                pass

            elif bookingid == 3:  # Multiple Check In Dates
                for checkindates in advancedates1:
                    for nngihts in list(map(int, CheckOutdates)):
                        checkindate = datetime.datetime.strptime(
                            checkindates, '%m/%d/%Y').strftime('%m/%d/%Y')
                        checkoutdate = datetime.datetime.strptime(
                            checkindate, '%m/%d/%Y') + datetime.timedelta(days=nngihts)
                        HotelRequestsDateDetail.objects.create(hotelrequestinputdetailsid=hotelRequestInputDetail, checkindate=datetime.datetime.strptime(
                            checkindate, '%m/%d/%Y'), checkoutdate=checkoutdate)
                
            else:  # Advance Weeks
                pass
    
    #hotelrequestinputdetailsid = hotelrequestinputdetailsid
    context = {
        "Message": "Request created successfully", "flag": "0", "request_id": requestobject.id
    }
    return JsonResponse(context)
# else:
#     return redirect(reverse('UserLogin'))


def get_hotels_suppliers_from_file(upload_file):
    filename = upload_file.name
    fs = FileSystemStorage(location=settings.HOTEL_MEDIA_UPLOAD)
    uploaded_filename = fs.save(filename, upload_file)
    uploaded_filepath = os.path.join(settings.HOTEL_MEDIA_UPLOAD, uploaded_filename)

    if uploaded_filepath.endswith('.xlsx') or uploaded_filepath.endswith('.xls'):
        dataframe = pd.read_excel(uploaded_filepath)
    else:
        dataframe = pd.read_csv(uploaded_filepath)

    list_hotels = []
    list_suppliers = []

    if "WebSiteHotelId" in dataframe.columns.values:
        for rows in dataframe.iterrows():
            list_hotels.append(rows[1]['WebSiteHotelId'])

    if "Supplier" in dataframe.columns.values:
        for rows in dataframe.iterrows():
            list_suppliers.append(rows[1]['Supplier'])

    supplier_ids = list(Competitor.objects.filter(name__in=list_suppliers).values_list('id', flat=True).distinct())
    supplier_ids = list(map(str, supplier_ids))
    list_hotels = list(set(list_hotels))

    return list_hotels, supplier_ids


@csrf_exempt
def FlightSaveRequest(request):
  
    if request.method == 'POST' and request.is_ajax():
           
        # if "UserID" in request.session:

            requestmodel = json.loads(request.POST['requestmodel'])
            destinationmodel = json.loads(request.POST['destinationmodel'])
            daterangemodel = json.loads(request.POST['daterangemodel'])
            requestname = requestmodel['requestname']
            requestdesc = requestmodel['requestdesc']
            req_id=requestmodel['hotel_req_id']

      
            requesthotel = RequestModeMaster.objects.get(id=3)

           
            if req_id != None and req_id != '':
            
                HotReId = HotelFlightRequestInputDetail.objects.get(id=req_id)
                reqMasterId = HotReId.requests.id
                
                RequestMaster.objects.filter(id=reqMasterId).update(title=requestname,
                description=requestdesc, requestmodeid=requesthotel, author=request.user.User_ID)
                requestobject = RequestMaster.objects.get(id=reqMasterId)
                HotelFlightRequestsDateDetail.objects.filter(hotelflightrequestinputdetailsId = req_id).delete()
                HotelFlightRequestInputDetail.objects.filter(id=req_id).delete()
                save_flight(requestobject,requestmodel,destinationmodel,daterangemodel)
                flag = 1

            elif request.session.get('requestid'):
                req_master_id = request.session.get('requestid')
                RequestMaster.objects.filter(id=req_master_id).update(title=requestname,
                description=requestdesc, requestmodeid= requesthotel, author=request.user.User_ID)
                requestobject = RequestMaster.objects.get(id=req_master_id)
                save_flight(requestobject,requestmodel,destinationmodel,daterangemodel)
                flag = 0

            else:

                requestmaster = RequestMaster.objects.create(
                    title=requestname, description=requestdesc, requestmodeid=requesthotel, author=request.user.User_ID)
                request.session['requestid'] = requestmaster.id
       
                try:
                    requestobject = RequestMaster.objects.get(id=requestmaster.id)  # Fetch Request object
                except:  # Issue in Request Master
                    context = {"data": ""}
                    return JsonResponse(context)
                save_flight(requestobject,requestmodel,destinationmodel,daterangemodel)
                flag = 0
                
    context = {
        "Message": "Request created successfully", "flag": flag, "request_id": requestobject.id
    }
    return JsonResponse(context)


def save_flight(requestobject,requestmodel,destinationmodel,daterangemodel):     
 
    bookingid = daterangemodel['BookingPeriod']

    pos = requestmodel['pos']
    adults = requestmodel['adults']
    children = requestmodel['children']
    reporttype = requestmodel['reporttype']
    all_hotel_flight = requestmodel['all_hotel_val']

    if requestmodel['drp_mul_grp_name'] :
        drp_mul_grp_name = requestmodel['drp_mul_grp_name']
            #drp_mul_grp_name = ''.join(drp_mul_grp_name)
    else:
        drp_mul_grp_name = ""
    
    # if requestmodel['Hotel_grp'] :
    #         Hotel_grp = requestmodel['Hotel_grp']
    #         Hotel_grp = ''.join(Hotel_grp)
    #     else:
    #         Hotel_grp = ""
    


    FromDate = None
    ToDate = None
    CheckIndates = None
    CheckOutdates = None
    advancedates = None

    requesthotel = RequestModeMaster.objects.get(id=3)
    airportCodeFrom = None
    airportCodeTo = None
    hotelpos = HotelPOS.objects.get(id=pos)
    suppliers = daterangemodel['suppliers']


    if bookingid == 1:
        FromDate = datetime.datetime.strptime(daterangemodel['fromdate'], '%m/%d/%Y')
        ToDate = datetime.datetime.strptime(daterangemodel['todate'], '%m/%d/%Y')
        CheckIndates = daterangemodel['CheckIndates']['CheckInDates']
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']
        CheckIndates1 = CheckIndates

    elif bookingid == 2:
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']
        advancedates = daterangemodel['CheckInDates']['CheckInDates']

    elif bookingid == 3:
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']
        advancedates = daterangemodel['CheckInDates']['CheckInDates']
        advancedates1 = advancedates
        

    else:
       
        advancedates = daterangemodel['CheckInDates']['CheckInDates']
        CheckOutdates = daterangemodel['CheckOutDates']['CheckOutDates']   

    if destinationmodel['mode'] == 1:
        airportCodeFrom = destinationmodel['FromAir']
        airportCodeTo = destinationmodel['ToAir']
        crawlmode = destinationmodel['crawlmode']
        hotels = destinationmodel['hotels']
        if destinationmodel['roomtype'] :
            roomtype = destinationmodel['roomtype']
            roomtype = ''.join(roomtype)
        else:
            roomtype = ""
        if destinationmodel['boardtype']:
            boardtype = destinationmodel['boardtype']
            boardtype = ', '.join(boardtype)
        else:
            boardtype = ""
        if destinationmodel['starrating']:
            starrating = destinationmodel['starrating']
            starrating = ', '.join(starrating)
        else:
            starrating = ''


        bookingperiodobject = BookingPeriodMaster.objects.get(id=bookingid, _active=True)
        fromairportcode_obj = AirportCodeMaster.objects.get(id=airportCodeFrom)
        toairportcode_obj = AirportCodeMaster.objects.get(id=airportCodeTo)
        #bookingperiodobject = BookingPeriodMaster.objects.get(id=1, _active=True)
        flightSearchTypeID_obj = FlightSearchType.objects.get(id=1)
        flag = True
        flag1= True
        all_hotels = []
      
        for i in hotels:
            for j in i:
                all_hotels.append(j)
        all_hotels = list(set(all_hotels))

        if all_hotel_flight == 'true':
            hotelobject = None   
            if advancedates is not None:
                if bookingid == 3 or bookingid == 4 or bookingid == 2:
                    if flag == True:
                        advancedates = ', '.join(advancedates)
                        flag = False
            else:
                advancedates = None
            if CheckIndates is not None:
                
                if bookingid == 1 or bookingid == 4:
                    if flag1 == True:
                        CheckIndates = ', '.join(CheckIndates)
                        flag1 = False
                        
            else:
                CheckIndates = None


            hotelFlightRequestInputDetails = HotelFlightRequestInputDetail.objects.create(requests=requestobject, bookingperiods=bookingperiodobject, pointofsales=hotelpos, adults=adults,
                                                                                        children=children, crawlmode=crawlmode, fromAirportCodeId=fromairportcode_obj,
                                                                                        toAirportCodeId=toairportcode_obj, hotels=hotelobject,StarRating=starrating,boardtype=boardtype, roomtype=roomtype,
                                                                                        suppliers=', '.join(suppliers), flightSearchTypeID=flightSearchTypeID_obj, fromdate=FromDate,
                                                                                        todate=ToDate,advancedates=advancedates, DaysOfWeek=CheckIndates, rentallength=', '.join(CheckOutdates),reporttype = reporttype,HotelGroupId=drp_mul_grp_name)

        else:
    
            for id in all_hotels:
                hotelobject = HotelMaster.objects.get(id=id)
                if advancedates is not None:
                    if bookingid == 3 or bookingid == 4 or bookingid == 2:
                        if flag == True:
                            advancedates = ', '.join(advancedates)
                            flag = False
                else:
                    advancedates = None
                if CheckIndates is not None:
                    
                    if bookingid == 1 or bookingid == 4:
                        if flag1 == True:
                            CheckIndates = ', '.join(CheckIndates)
                            flag1 = False
                            
                else:
                    CheckIndates = None


                hotelFlightRequestInputDetails = HotelFlightRequestInputDetail.objects.create(requests=requestobject, bookingperiods=bookingperiodobject, pointofsales=hotelpos, adults=adults,
                                                                                            children=children, crawlmode=crawlmode, fromAirportCodeId=fromairportcode_obj,
                                                                                            toAirportCodeId=toairportcode_obj, hotels=hotelobject,StarRating=starrating,boardtype=boardtype, roomtype=roomtype,
                                                                                            suppliers=', '.join(suppliers), flightSearchTypeID=flightSearchTypeID_obj, fromdate=FromDate,
                                                                                            todate=ToDate,advancedates=advancedates, DaysOfWeek=CheckIndates, rentallength=', '.join(CheckOutdates),reporttype = reporttype,HotelGroupId=drp_mul_grp_name)

                hotelFlightRequestInputDetails = HotelFlightRequestInputDetail.objects.get(
                    id=hotelFlightRequestInputDetails.id)

                if bookingid == 1:  # Date Range
                    for date in dates_between(FromDate, ToDate):
                        for chckindate in CheckIndates.split(', '):
                            if date.strftime('%a') == chckindate[0:3]:
                                for nngihts in list(map(int, CheckOutdates)):
                                    checkoutdate = date + datetime.timedelta(days=nngihts)
                                    HotelFlightRequestsDateDetail.objects.create(
                                        hotelflightrequestinputdetailsId=hotelFlightRequestInputDetails, checkindate=date.date(), checkoutdate=checkoutdate)

                elif bookingid == 2:  # Advance Days
                    pass

                elif bookingid == 3:  # Multiple Check In Dates
                    for checkindates in advancedates1:
                        for nngihts in list(map(int, CheckOutdates)):
                            checkindate = datetime.datetime.strptime(
                                checkindates, '%m/%d/%Y').strftime('%m/%d/%Y')
                            checkoutdate = datetime.datetime.strptime(
                                checkindate, '%m/%d/%Y') + datetime.timedelta(days=nngihts)
                            HotelFlightRequestsDateDetail.objects.create(
                                hotelflightrequestinputdetailsId=hotelFlightRequestInputDetails,checkindate=datetime.datetime.strptime(
                                checkindate, '%m/%d/%Y'), checkoutdate=checkoutdate)

                else:  # Advance Weeks
                    pass
    else:
        airportCodeFrom = destinationmodel['FromAirport']
        airportCodeTo = destinationmodel['ToAirport']
        

        bookingperiodobject = BookingPeriodMaster.objects.get(id=bookingid, _active=True)
        fromairportcode_obj = AirportCodeMaster.objects.get(id=airportCodeFrom)
        toairportcode_obj = AirportCodeMaster.objects.get(id=airportCodeTo)
        flightSearchTypeID_obj = FlightSearchType.objects.get(id=2)
        flag = True
        flag1= True

        if advancedates is not None:
            if bookingid == 3 or bookingid == 4 or bookingid == 2:
                if flag == True:
                    advancedates = ', '.join(advancedates)
                    flag = False
        else:
            advancedates = None
        if CheckIndates is not None:
            
            if bookingid == 1 or bookingid == 4:
                if flag1 == True:
                    CheckIndates = ', '.join(CheckIndates)
                    flag1 = False
                    
        else:
            CheckIndates = None
        

        hotelFlightRequestInputDetails = HotelFlightRequestInputDetail.objects.create(requests=requestobject, bookingperiods=bookingperiodobject, pointofsales=hotelpos, adults=adults,
                                                                                        children=children, fromAirportCodeId=fromairportcode_obj, toAirportCodeId=toairportcode_obj, hotels=None,
                                                                                        StarRating=None, boardtype=None, roomtype=None, suppliers=', '.join(suppliers), flightSearchTypeID=flightSearchTypeID_obj, fromdate=FromDate,
                                                                                        todate=ToDate, advancedates=advancedates,DaysOfWeek=CheckIndates, rentallength=', '.join(CheckOutdates),HotelGroupId=drp_mul_grp_name)

        hotelFlightRequestInputDetails = HotelFlightRequestInputDetail.objects.get(id=hotelFlightRequestInputDetails.id)

        if bookingid == 1:  # Date Range
            for date in dates_between(FromDate, ToDate):
                for chckindate in CheckIndates.split(', '):
                    if date.strftime('%a') == chckindate[0:3]:
                        for nngihts in list(map(int, CheckOutdates)):
                            checkoutdate = date + datetime.timedelta(days=nngihts)
                            HotelFlightRequestsDateDetail.objects.create(
                                hotelflightrequestinputdetailsId=hotelFlightRequestInputDetails, checkindate=date.date(), checkoutdate=checkoutdate)

        elif bookingid == 2:  # Advance Days
            pass

        elif bookingid == 3:  # Multiple Check In Dates
            for checkindates in advancedates1:
                for nngihts in list(map(int, CheckOutdates)):
                    checkindate = datetime.datetime.strptime(
                        checkindates, '%m/%d/%Y').strftime('%m/%d/%Y')
                    checkoutdate = datetime.datetime.strptime(
                        checkindate, '%m/%d/%Y') + datetime.timedelta(days=nngihts)
                    HotelFlightRequestsDateDetail.objects.create(
                        hotelflightrequestinputdetailsId=hotelFlightRequestInputDetails,checkindate=datetime.datetime.strptime(
                        checkindate, '%m/%d/%Y'), checkoutdate=checkoutdate)

        else:  # Advance Weeks
            pass

    context = {
        "Message": "Request created successfully", "flag": "0", "request_id": requestobject.id
    }
    return JsonResponse(context)


@csrf_exempt
def FlightDeleteRequest(request):
    if request.method == 'POST' and request.is_ajax():  
       
        deleteId = request.POST['deletereqId']

        HotReId = HotelFlightRequestInputDetail.objects.get(id=deleteId)
        reqMasterId = HotReId.requests.id

        HotelFlightRequestsDateDetail.objects.filter(hotelflightrequestinputdetailsId = deleteId).delete()
        HotelFlightRequestInputDetail.objects.filter(id=deleteId).delete()
        context = {
        "Message": "Request deleted successfully", "delete_id": reqMasterId
        }
        return JsonResponse(context)


@csrf_exempt
def EditReq(request):
    if request.method == 'POST' and request.is_ajax():
        editReqId = request.POST['req_id']
        HotelFlight = HotelFlightRequestInputDetail.objects.filter(requests=editReqId)
        Hotel = HotelRequestInputDetail.objects.filter(requests=editReqId)
        url =''
        
        
    context = {
        "Message": "Request created successfully", "flag": "0" ,"url": url 
            }
    return JsonResponse(context)   

@csrf_exempt
def emailSave(request):
    if request.method == 'POST' and request.is_ajax():

        emailSaveReqId = json.loads(request.POST['emailDetails'])
        if emailSaveReqId['scheduleReqId']:
            scheduleReqId = emailSaveReqId['scheduleReqId']
        else:
            scheduleReqId = ''
        
        if emailSaveReqId['email']:
            email = emailSaveReqId['email']
        else:
            email = ''
        if emailSaveReqId['cc']:
            cc = emailSaveReqId['cc']
        else:
            cc = ''

        RequestMaster.objects.filter(id=scheduleReqId).update(email=email,email_cc=cc)
        
        
    context = {
        "Message": "Request created successfully", "flag": "0" 
            }
    return JsonResponse(context)  


@csrf_exempt
def StopReq(request):
    if request.method == 'POST' and request.is_ajax():
        stopReqId = request.POST['req_id']
        reportFlag = RequestMaster.objects.get(id=stopReqId)
        flag = 0
      
        if reportFlag.reportFlag == 0:
            RequestMaster.objects.filter(id=stopReqId).update(reportFlag = 1 )
            flag = 1
        else:
            RequestMaster.objects.filter(id=stopReqId).update(reportFlag = 0 )
            flag = 0
        
    context = {
        "Message": "Request created successfully .Report Set to (%d)" %flag, "flag": flag  
            }
    return JsonResponse(context)

@csrf_exempt
def download(request):
    path = os.path.join(settings.MEDIA_ROOT, 'format_templates/batch_schedule_upload.xls')
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(path)
            return response
    raise http404

def batch_upload_template_hotel(request):
    path = os.path.join(settings.HOTEL_MEDIA_DOWNLOAD, 'batch_upload_template_Hotel_Only.xlsx')
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(path)
            return response

def batch_upload_template_flight(request):
    path = os.path.join(settings.HOTEL_MEDIA_DOWNLOAD, 'batch_upload_template_Hotel_Flight.xlsx')
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(path)
            return response


@csrf_exempt
def batch_input_upload_hotel(request):
        if request.method == 'POST' or request.is_ajax():
            filepath = None
            for k, v in request.FILES.items():
                filepath = v
            fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
            uploaded_filename = fs.save(str(filepath), filepath)
            dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)

            count =len(dataFrame.columns)
            #if (count == 39  and  list(dataFrame.columns) == settings.BATCH_UPLOAD_HOTEL_COLUMNS):
            if (count == 39):
                temp_hotel_only.objects.all().delete()
                
                import sqlalchemy
                database_username = settings.DATABASES['default']['USER']
                database_password = settings.DATABASES['default']['PASSWORD']
                database_name = settings.DATABASES['default']['NAME']
                database_ip = settings.DATABASES['default']['HOST']
                database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                    format(database_username, database_password, 
                                                            database_ip, database_name))
                dataFrame.to_sql(con=database_connection, name='temp_Hotel_UI', if_exists='append')

                results = sp_get_by_param('sp_RequestScheduleValidation',['H'])
                error_list = []
                for Sp_res in results:
                    print('Sp_res+++++', Sp_res)
                    dict1 = {"Batch Name": Sp_res[1], "Country": Sp_res[2], "Destination" : Sp_res[3],
                             "Hotel" : Sp_res[4],  "Source Market" : Sp_res[5],"Adults" : Sp_res[6],
                             "Children" : Sp_res[7], "Check-in & Check-out date Dates" : Sp_res[8],
                             "Advance Dates": Sp_res[9],"Start & End Check-in date":Sp_res[10],
                             "Days":Sp_res[11],"Nights":Sp_res[12],"Supplier 1":Sp_res[13],
                             "Supplier 2":Sp_res[14],"Supplier 3":Sp_res[15],"Supplier 4":Sp_res[16],
                             "Supplier 5":Sp_res[17],"Supplier 6":Sp_res[18],"Supplier 7":Sp_res[19],
                             "Supplier 8":Sp_res[20],"Supplier 9":Sp_res[21],"Supplier 10":Sp_res[22],
                             "Supplier 11":Sp_res[23],"Supplier 12":Sp_res[24],"Supplier 13":Sp_res[25],
                             "Supplier 14":Sp_res[26],"Supplier 15":Sp_res[27],"Supplier 16":Sp_res[28],
                             "Supplier 17":Sp_res[29],"Supplier 18":Sp_res[30],"Supplier 19":Sp_res[31],
                             "Supplier 20":Sp_res[32],"Schedule Duration":Sp_res[33],"Schedule Frequency":Sp_res[34],
                             "Which Week?":Sp_res[35],"Which Day of week/month?":Sp_res[36],"Which Month?":Sp_res[37],
                             "Which date of month?":Sp_res[38],"Schedule Time":Sp_res[39],"Error":Sp_res[40] }
                    error_list.append(dict1)
                if error_list:
                    df = pd.DataFrame(error_list)
                    time = 'Hotel_request_error_output_%s' % timezone.now() + ''
                    path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                    writer = pd.ExcelWriter(path)
                    #columns = settings.BATCH_UPLOAD_HOTEL_COLUMNS.append("Error")

                    columns = [
                        'Batch Name', 'Country', 'Destination', 'Hotel', 'Source Market', 'Adults', 'Children',
                        'Check-in & Check-out date Dates', 'Advance Dates', 'Start & End Check-in date', 'Days',
                        'Nights', 'Supplier 1', 'Supplier 2', 'Supplier 3', 'Supplier 4', 'Supplier 5', 'Supplier 6',
                        'Supplier 7', 'Supplier 8', 'Supplier 9', 'Supplier 10', 'Supplier 11', 'Supplier 12', 'Supplier 13',
                        'Supplier 14', 'Supplier 15', 'Supplier 16', 'Supplier 17', 'Supplier 18', 'Supplier 19', 'Supplier 20',
                        'Schedule Duration', 'Schedule Frequency', 'Which Week?', 'Which Day of week/month?', 'Which Month?',
                        'Which date of month?', 'Schedule Time', 'Error'
                    ]

                    df.to_excel(writer, 'Sheet1', columns=columns, index=False)
                    writer.save()
                    path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                    data = {
                        'download_link': path,
                        'msg': 'Error in excel file.',
                        'msg_type': 'Error'
                    }
                    return JsonResponse(data, safe=False)
                else:
                    try:
                        #print('before databse entry datetime = ',datetime.datetime.now())
                        file_upload = AjaxFileUploader(request).uploads[0]
                        upload_handler = ExcelBatchUploadHandler(file_upload)
                        h_new_batches, invalid_batches_path = upload_handler.update_db_hotel(request)
                        #print('after databse entry datetime = ',datetime.datetime.now())
                        if h_new_batches == None or len(h_new_batches) == 0:
                            raise Exception('BatchNone')
                        
                        data = {
                            'download_link': file_upload.download_link,
                            'msg' : 'Batch Uploaded successfully.',
                            'msg_type': 'Success'
                        }

                        if h_new_batches:
                            request.session['batch_items'] = list(h_new_batches.values_list('id', flat=True))
                            data.update({'h_new_batches': list(h_new_batches.values_list('id', flat=True))})
                        if invalid_batches_path:
                            invalid_batches_path = settings.STATIC_URL + invalid_batches_path
                            data.update(download_link=invalid_batches_path)
                            data.update(msg="Batches created successfully while some batches were incorrect. click to download error log.")
                            data.update(msg_type="SuccessError")
                        return JsonResponse(data, safe=False)
                        
                    except Exception as e:
                        if str(e)=="blankFile":
                            msg="Value can not be blank while upload"
                        elif str(e) == "BatchNone":
                            msg = 'Data is blank or data is mismatch. Please try It Again!'
                        else:
                            raise e
    
                        data = {
                            'download_link': '',
                            'msg' : msg,
                            'msg_type': 'Error'
                        }
                                            
                        return JsonResponse(data, safe=False)
            else : 
                    data =  {
                        'download_link': '',
                        'msg' : "Uploaded excel format is not valid !!!!",
                        'msg_type': 'Error'
                    } 
                    return JsonResponse(data, safe=False)  
        else:
            return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def batch_input_upload_flight(request):
        if request.method == 'GET' or request.is_ajax():
            filepath = None
            for k, v in request.FILES.items():
                filepath = v
            fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
            uploaded_filename = fs.save(str(filepath), filepath)
            dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
            count =len(dataFrame.columns)
           
            if (count == 41  and  dataFrame.columns[0]=='Batch Name' ):
                table_name = 'temp_Hotel_Flight_UI'
                temp_hotel_Flight.objects.all().delete()
                
                import sqlalchemy
                database_username = settings.DATABASES['default']['USER']
                database_password = settings.DATABASES['default']['PASSWORD']
                database_ip       = settings.DATABASES['default']['HOST']
                database_name     = settings.DATABASES['default']['NAME']
                database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                    format(database_username, database_password, 
                                                            database_ip, database_name))
                dataFrame.to_sql(con=database_connection, name= table_name, if_exists='append')
                
                lst = ['HF']
                sp_res_1 = sp_get_by_param('sp_RequestScheduleValidation',lst)
                # sp_res_1 = []
                count =0
                path =''
                if (len(sp_res_1)>0) :
                    list1 = []
                    dict1 = {}
                    for Sp_res in sp_res_1:
                        dict1 = {"Batch Name": Sp_res[1], "Country": Sp_res[2], "Destination" : Sp_res[3], "Hotel" : Sp_res[4],  "Source Market" : Sp_res[5],"Adults" : Sp_res[6], "Children" : Sp_res[7], "Check-in & Check-out date Dates" : Sp_res[8], "Advance Dates": Sp_res[9],"Start & End Check-in date":Sp_res[10],"Days":Sp_res[11],"Nights":Sp_res[12],"Departure Airport Code":Sp_res[13],"Arrival Airport Code":Sp_res[14],"Supplier 1":Sp_res[15],"Supplier 2":Sp_res[16],"Supplier 3":Sp_res[17],"Supplier 4":Sp_res[18],"Supplier 5":Sp_res[19],"Supplier 6":Sp_res[20],"Supplier 7":Sp_res[21],"Supplier 8":Sp_res[22],"Supplier 9":Sp_res[23],"Supplier 10":Sp_res[24],"Supplier 11":Sp_res[25],"Supplier 12":Sp_res[26],"Supplier 13":Sp_res[27],"Supplier 14":Sp_res[28],"Supplier 15":Sp_res[29],"Supplier 16":Sp_res[30],"Supplier 17":Sp_res[31],"Supplier 18":Sp_res[32],"Supplier 19":Sp_res[33],"Supplier 20":Sp_res[34],"Schedule Duration":Sp_res[35],"Schedule Frequency":Sp_res[36],"Which Week?":Sp_res[37],"Which Day of week/month?":Sp_res[38],"Which Month?":Sp_res[39],"Which date of month?":Sp_res[40],"Schedule Time":Sp_res[41],"Error":Sp_res[42] }
                        list1.append(dict1)
                    if len(list1) > 0:
                        df = pd.DataFrame(list1)
                        time = 'Hotel_request_error_output_%s' % timezone.now() + ''
                        path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                        writer = pd.ExcelWriter(path)
                        df.to_excel(writer, 'Sheet1', columns=["Batch Name", "Country", "Destination", "Hotel","Source Market","Adults","Children", "Check-in & Check-out date Dates", "Advance Dates","Start & End Check-in date","Days","Nights","Departure Airport Code","Arrival Airport Code","Supplier 1","Supplier 2","Supplier 3","Supplier 4","Supplier 5","Supplier 6","Supplier 7","Supplier 8","Supplier 9","Supplier 10","Supplier 11","Supplier 12","Supplier 13","Supplier 14","Supplier 15","Supplier 16","Supplier 17","Supplier 18","Supplier 19","Supplier 20","Schedule Duration","Schedule Frequency","Which Week?","Which Day of week/month?","Which Month?","Which date of month?","Schedule Time","Error"], index=False)
                        writer.save()
                        path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                        count=len(list1)
                    else :
                            count= "0"
                            path=""
                    data =          {
                                    'download_link': path,
                                    'msg' : "",
                                } 
                    return JsonResponse(data, safe=False)            
                else :

                    try:

                        file_upload = AjaxFileUploader(request).uploads[0]
                        upload_handler = ExcelBatchUploadHandler(file_upload)
                        hf_new_batches = upload_handler.update_db_flight(request)
                        if hf_new_batches == None or len(hf_new_batches) == 0:
                            raise Exception('BatchNone')
                        msg = ''
                        
                    except Exception as e:
                        if str(e)=="blankFile":
                            msg="Value can not be blank while upload"
                        elif str(e) == "BatchNone":
                            msg = 'Data is blank or data is mismatch. Please try It Again!'
                        else:
                            raise e
                        
                    response = {
                        'download_link': file_upload.download_link,
                        'msg' : msg
                    }
                    if hf_new_batches:
                        request.session['batch_items'] = list(hf_new_batches.values_list('id', flat=True))
                        response.update({'hf_new_batches': list(hf_new_batches.values_list('id', flat=True))})
                    return AetosResponse.success_api_response(response, 'upload successful')
            else : 
                    data =  {
                                    'download_link': '',
                                    'msg' : "Uploaded excel format is not valid !!!!",
                        } 
                    return JsonResponse(data, safe=False)  
        else:
            return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def batch_input_upload_sp(request):
    from sqlalchemy import create_engine
    if not (request.method == 'POST' and request.is_ajax()):
        return AetosResponse.failure_api_response(dict(), 'only post and ajax calls allowed')

    file_upload = AjaxFileUploader(request).uploads[0]

    engine_string = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
        settings.DATABASES['default']['USER'],
        settings.DATABASES['default']['PASSWORD'],
        settings.DATABASES['default']['HOST'],
        settings.DATABASES['default']['PORT'],
        settings.DATABASES['default']['NAME']
    )

    cnx = create_engine(engine_string, echo=False)

    xls = pd.ExcelFile(file_upload.uploaded_path)

    df_hotel = pd.read_excel(xls, 'Hotel')
    df_package = pd.read_excel(xls, 'Package')

    db = pymysql.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        passwd=settings.DATABASES['default']['PASSWORD'],
        db=settings.DATABASES['default']['NAME']
    )
    # db = pymysql.connect(host=settings.DATABASES['default']['HOST'], user=settings.DATABASES['default']['USER'], passwd=settings.DATABASES['default']['PASSWORD'], db=settings.DATABASES['default']['NAME'])

    cur = db.cursor()

    query = "truncate table temp_Hotel;"
    cur.execute(query)

    query = "truncate table temp_Package;"
    cur.execute(query)


    df_hotel.to_sql(name="temp_Hotel", con=cnx, if_exists='append', index=False)

    df_package.to_sql(name="temp_Package", con=cnx, if_exists='append', index=False)

    cur.close()
    db.close()

    # if request_objects:
    return AetosResponse.success_api_response({
        'download_link': file_upload.download_link,
        # 'request_objects': [obj.id for obj in request_objects]
    }, 'upload successful')

@csrf_exempt
def hotel_plus_flight_index(request,request_id = None):
    if request.method == 'GET':
        if request_id:
            request.session['requestid'] = request_id
            
        else:
            if 'requestid' in request.session:
                del request.session['requestid']
            if 'batch_items' in request.session:
                del request.session['batch_items']
            if 'request_title' in request.session:
                del request.session['request_title']
            if 'request_description' in request.session:
                del request.session['request_description']

        context = {}
        if request_id:
            flag = 1
            if request_id == 'excel_upload':
                request_ids = request.session['batch_items']
                requests = RequestMaster.objects.filter(id__in=request_ids).order_by('-id')
                request_id = request_ids[0]
            else:
                requests = RequestMaster.objects.filter(id=request_id).order_by('-id')

       
            hotelflightrequestinputs = HotelFlightRequestInputDetail.objects.filter(requests__in=requests)
            data_list = []
            for hf in hotelflightrequestinputs:
                serialise_data = {}
               

                if hf.hotels_id == None and hf.flightSearchTypeID.id ==1:#or hf.fromdate == None or hf.todate == None or hri.DaysOfWeek == None:
                    

                    fromAirCode = AirportCodeMaster.objects.get(id = hf.fromAirportCodeId.id)
                    fromCityCode = fromAirCode.city.id
                    fromCountryCode = fromAirCode.country.id
                    toAirCode = AirportCodeMaster.objects.get(id = hf.toAirportCodeId.id)
                    toCityCode = toAirCode.city.id
                    toCountryCode = toAirCode.country.id
                    
                    serialise_data = lambda hr, hri: {
                        'id': hri.id,
                        'hotel_request': {
                            'request_title': hr.title,
                            'request_desc': hr.description
                        },

                        'booking': {
                            'pos' : hri.pointofsales.id,
                            'adult_count': hri.adults,
                            'children_count': hri.children,
                            'fromAirport' :hri.fromAirportCodeId.id,
                            'toAirport': hri.toAirportCodeId.id,
                            'suppliers': hri.suppliers,
                            #'week_days': hri.DaysOfWeek,
                            #'advance_dates': hri.advancedates,
                            'no_of_nights': hri.rentallength,
                            'bookingperiods' : hri.bookingperiods_id,
                            'fromcity' : fromCityCode,
                            'fromcountry' : fromCountryCode,
                            'tocity' : toCityCode,
                            'tocountry':toCountryCode,
                            'id' : hri.id,
                            'flightSearchType' : hri.flightSearchTypeID.id,
                            'HotelGroupId':hri.HotelGroupId
                            
                        },
                        'crawl': {'mode': hri.crawlmode},
                        'airport': {'to': hri.toAirportCodeId.name, 'from': hri.fromAirportCodeId.name },
                        'country': { 'pos': hri.pointofsales.posale},

                        
                    }

                    data_list.append([serialise_data(sub_req.requests, sub_req) for sub_req in hotelflightrequestinputs if sub_req.id == hf.id])
                elif  hf.hotels_id == None and hf.flightSearchTypeID.id ==2: 
                    

                    fromAirCode = AirportCodeMaster.objects.get(id = hf.fromAirportCodeId.id)
                    fromCityCode = fromAirCode.city.id
                    fromCountryCode = fromAirCode.country.id
                    toAirCode = AirportCodeMaster.objects.get(id = hf.toAirportCodeId.id)
                    toCityCode = toAirCode.city.id
                    toCountryCode = toAirCode.country.id

                    serialise_data = lambda hr, hri: {
                        'id': hri.id,
                        'hotel_request': {
                            'request_title': hr.title,
                            'request_desc': hr.description
                        },
                        'booking': {
                            'pos' : hri.pointofsales.id,
                            'adult_count': hri.adults,
                            'children_count': hri.children,
                            'fromAirport' :hri.fromAirportCodeId.id,
                            'toAirport': hri.toAirportCodeId.id,
                            'hotel': '',
                            'room_type': hri.roomtype,
                            'board_type': hri.boardtype,
                            'star_rating': hri.StarRating,
                            'suppliers': hri.suppliers,
                            'no_of_nights': hri.rentallength,
                            'bookingperiods' : hri.bookingperiods_id,
                            'fromcity' : fromCityCode,
                            'fromcountry' : fromCountryCode,
                            'tocity' : toCityCode,
                            'tocountry':toCountryCode,
                            'id' : hri.id,
                            'flightSearchType' : hri.flightSearchTypeID.id,
                            'HotelGroupId':hri.HotelGroupId

                        },
                        'crawl': {'mode': hri.crawlmode},
                        'airport': {'to': hri.toAirportCodeId.name, 'from': hri.fromAirportCodeId.name},
                        'country': { 'pos': hri.pointofsales.posale},
                        'country_id': {'hotel_name':''}

                        
                    }                                       
                    data_list.append([serialise_data(sub_req.requests, sub_req) for sub_req in hotelflightrequestinputs if sub_req.id == hf.id])
                else:
                    

                    serialise_data = lambda hr, hri: {
                        'id': hri.id,
                        'hotel_request': {
                            'request_title': hr.title,
                            'request_desc': hr.description
                        },
                        'booking': {
                            'pos' : hri.pointofsales.id,
                            'adult_count': hri.adults,
                            'children_count': hri.children,
                            'fromAirport' :hri.fromAirportCodeId.id,
                            'toAirport': hri.toAirportCodeId.id,
                            'hotel': ",".join([str(hf.hotels.id)]),
                            'room_type': hri.roomtype,
                            'board_type': hri.boardtype,
                            'star_rating': hri.StarRating,
                            'suppliers': hri.suppliers,
                            'no_of_nights': hri.rentallength,
                            'bookingperiods' : hri.bookingperiods_id,
                            'id' : hri.id,
                            'flightSearchType' : hri.flightSearchTypeID.id,
                            'HotelGroupId':hri.HotelGroupId

                        },
                        'crawl': {'mode': hri.crawlmode},
                        'airport': {'to': hri.toAirportCodeId.name, 'from': hri.fromAirportCodeId.name},
                        'country': { 'pos': hri.pointofsales.posale},
                        'country_id': {'hotel_name':hri.hotels.name}

                        
                    }                                       
                    data_list.append([serialise_data(sub_req.requests, sub_req) for sub_req in hotelflightrequestinputs if sub_req.id == hf.id])
                    
                for i in data_list:
                    for x in i :
                        if hf.bookingperiods_id == 1:
                            if x['id'] == hf.id:
                                x['booking']['week_days'] = hf.DaysOfWeek
                                x['booking']['fromdate'] = hf.fromdate.strftime('%m/%d/%Y')
                                x['booking']['todate'] = hf.todate.strftime('%m/%d/%Y')
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''

                        elif hf.bookingperiods_id == 2:

                            if x['id'] == hf.id:

                                x['booking']['advance_dates'] = hf.advancedates
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''
                                

                        elif hf.bookingperiods_id == 3:

                            if x['id'] == hf.id:

                                x['booking']['advance_dates'] = hf.advancedates
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''
                                


                        else:

                            if x['id'] == hf.id:

                                x['booking']['advance_dates'] = hf.advancedates
                                x['booking']['week_days'] = hf.DaysOfWeek
                                if x['booking']['suppliers']:
                                    comp = x['booking']['suppliers'].split(',')
                                    lis = []
                                    for sup in comp:
                                        lis.append(CompetitorMaster.objects.get(id =sup).name)

                                    x['booking']['suppliers_name'] = ', '.join(lis)
                                else:
                                    x['booking']['suppliers_name'] = ''

            hidden_data_list = data_list[:3]
            show_data_list = data_list[3:]
            context.update({
                'data_list': data_list,
                'hidden_data_list':hidden_data_list,
                'show_data_list':show_data_list,
                'data_list_count': len(data_list)
            })
            if len(context['data_list']) != 0:
                lists = reduce(lambda x,y: x+y,context['data_list'])
                context_string = json.dumps({c['id']: c for c in lists.copy()}) 
                context.update({'json_string': context_string})

            if request.session.get('batch_items'):
                context.update({
                    'batch_items': RequestMaster.objects.filter(id__in=request.session['batch_items']).order_by('-id'),
                    'selected_request_id': int(request_id),
                })

        else:
            flag = 0

        posales = HotelPOS.objects.filter(_active=True).values('id', 'posale')
        dicposales = {}
        for i in posales:
            dicposales[i['id']] = i['posale']

        countries = CountryMaster.objects.filter(_active=True).values(
            'id', 'name').order_by('name')

        diccountries = {}
        for i in countries:
            diccountries[i['id']] = i['name']

        roomtypes = RoomTypeMaster.objects.filter(
            _active=True).values('id', 'roomtype')
        dicroomtypes = {}
        for i in roomtypes:
            dicroomtypes[i['id']] = i['roomtype']

        boardtypes = BoardTypeMaster.objects.filter(
            _active=True).values('id', 'boardtypedescription')
        dicboardtypes = {}

        for i in boardtypes:
            dicboardtypes[i['id']] = i['boardtypedescription']

        starratings = StarRatingMaster.objects.filter(
            _active=True).values('id', 'starrating')
        dic_starratings = {}

        for i in starratings:
            dic_starratings[i['id']] = i['starrating']
        # Bind Countries from CountyMaster

        airportCodes = AirportCodeMaster.objects.filter(
            _active=True).values('id', 'code')
        dictairportcodes = {}
        for i in airportCodes:
            dictairportcodes[i['id']] = i['code']

        suppliers = CompetitorMaster.objects.filter(_active=True).values('id', 'name')
        dicsuppliers = {}
        for i in suppliers:
            dicsuppliers[i['id']] = i['name']

        #hotels = HotelMaster.objects.filter(_active=True).values('id', 'name')
        hotels = []
        dichotels = {}
        for i in hotels:
            dichotels[i['id']] = i['name']

        context.update({
            'pointofsales': dicposales,
            'countries': diccountries,
            'roomtypes': dicroomtypes,
            'boardtypes': dicboardtypes,
            'starratings': dic_starratings,
            'airportcodes': dictairportcodes,
            'suppliers': dicsuppliers,
            'hotels': dichotels,
            'flag' : flag
        })

        #return render_to_response('hotel/hotel_plus_flight.html', context, context_instance=RequestContext(request))
        return render(request, 'hotel/hotel_plus_flight.html', context)
    else:
        return JsonResponse({"data": "success"})


@csrf_exempt
def Hotels_Specific(request):
    if request.method == 'POST' and request.is_ajax():
    
        filename = None
        filepath = None

        countries = request.POST['countries']
        cities = request.POST['cities']

        country_name = CountryMaster.objects.get(id=countries).name
        city_name = CityMaster.objects.get(id=cities).name

        for filename, file in request.FILES.items():
            filename = request.FILES[filename].name
            file = file
        
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_UPLOAD)
        uploaded_filename = fs.save(filename, file)
        uploaded_filepath = os.path.join(settings.HOTEL_MEDIA_UPLOAD, uploaded_filename)

        if uploaded_filepath.endswith('.xlsx') or uploaded_filepath.endswith('.xls'):
            dataframe = pd.read_excel(uploaded_filepath)
        else:  # read csv
            dataframe = pd.read_csv(uploaded_filepath)

        count = len(dataframe.columns)
        rows_count = len(dataframe.index)
        message = "Excel file template are not matched !!!"
        list_hotels = []
        path = ''
        msgType = 1

        if (count == 5 and dataframe.columns[0] == 'Country' and dataframe.columns[1] == 'City'
                and dataframe.columns[2] == 'Supplier' and dataframe.columns[3] == 'WebSiteHotelId'
                and dataframe.columns[4] == 'Hotel Name'):
            list1 = []

            dataFrame = dataframe.replace(np.nan, '', regex=True)
            if rows_count > 500:
                return JsonResponse({"message": 'File size should not be more than 500.', "path": path, "hotels": list_hotels, "msgType": msgType})
            if rows_count == 1:
                return JsonResponse({"message": 'Invalid Excel file', "path": path, "hotels": list_hotels, "msgType": msgType})
            if rows_count == 0:
                return JsonResponse({"message": 'Empty file could not be processed.', "path": path, "hotels": list_hotels, "msgType": msgType})

            for item in dataFrame.values.tolist():
                if not CountryMaster.objects.filter(name=item[0]).exists():
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3], "Hotel Name": item[4],
                             "ErrorStatus": "Sorry country "+ item[0] +" does not Exist"}
                    list1.append(dict1)
                elif not CityMaster.objects.filter(name=item[1]).exists():
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3], "Hotel Name": item[4],
                             "ErrorStatus": "Sorry city "+ item[1] +" does not Exist"}
                    list1.append(dict1)
                elif not Competitor.objects.filter(name=item[2]).exists():
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3],
                             "Hotel Name": item[4],
                             "ErrorStatus": "Sorry supplier " + item[2] + " does not Exist"}
                    list1.append(dict1)
                elif item[3] == '':
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3],
                             "Hotel Name": item[4],
                             "ErrorStatus": "Sorry website hotel id cannot be empty."}
                    list1.append(dict1)
                elif item[4] == '':
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3],
                             "Hotel Name": item[4],
                             "ErrorStatus": "Sorry hotel name cannot be empty."}

                    list1.append(dict1)
                elif not (item[1].lower() == city_name.lower()):
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3],
                             "Hotel Name": item[4],
                             "ErrorStatus": "Sorry there is city mismatch."}

                    list1.append(dict1)
                elif not (item[0].lower() == country_name.lower()):
                    dict1 = {"Country": item[0], "City": item[1], "Supplier": item[2], "WebSiteHotelId": item[3],
                             "Hotel Name": item[4],
                             "ErrorStatus": "Sorry there is country mismatch."}

                    list1.append(dict1)

            if len(list1) > 0:
                df = pd.DataFrame(list1)
                time = 'create_request_error_output_excel_%s' % timezone.now() + ''
                path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Download_create_request/%s' % time + '.xlsx'
                writer = pd.ExcelWriter(path)
                df.to_excel(writer, 'Sheet1',
                            columns=['Country', 'City', 'Supplier', 'WebSiteHotelId', "Hotel Name", 'ErrorStatus'], index=False)
                writer.save()
                path = '/static/Excel_file_Download_create_request/%s' % time + '.xlsx'
                message = 'Excel file matched but Errors in file'
                msgType = 2
            else:
                message = 'File validated successfully'
                msgType = 3
                for rows in dataframe.iterrows():
                    list_hotels.append(rows[1]['Hotel Name'])

        return JsonResponse({"message": message, "path": path, "hotels": list_hotels, "msgType": msgType})



def bind_request_hotel(request, request_id=None):
    context = {
        'data_list': [
            {
                'id': request_id,
                'booking': {'adult_count': 4, 'children_count': 5, 'star_rating_list': ', '.join(['3', '4', '5']),
                            'no_of_nights': 2, 'getMySQLDBroom_type': ', '.join(['1', '3']), 'board_type': ', '.join(['1', '4']),
                            'hotel': ', '.join(['1', '3'])},
                'crawl': {'mode': 1},
                'airport': {'to': 'IN', 'from': 'BGI'},
                'country': {'to': 'India', 'from': 'Bulgaria', 'pos': 'Bulgaria'},
                'country_id': {'to': 'IN', 'from': 'BGI', 'pos': 'BGI'}
            }
        ]
    }
    context_string = json.dumps({c['id']: c for c in context['data_list'].copy()})
    context.update({'json_string': context_string})
    return render(request, 'hotel/booking_list.html', context)


@csrf_exempt
def hoteltype_download(request):
    path = os.path.join(settings.HOTEL_MEDIA_DOWNLOAD,'hotel.xls')

    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(path)
            return response


def get_update_schedular_context(request):
    

    if 'request_action' in request.session:
        # del request.session['request_action']
      


        if request.session.get('request_action') == 'update_request':
            request_id = request.session.get('requestid')
            schedule_masters = ScheduleMaster.objects.filter(request_id=request_id).values(
                'startDate', 'endDate', 'triggerDay', 'schedule_type_id', 'time', 'frequency',
                'day_of_week', 'week_of_month'
            )
            
            
            if schedule_masters.exists():
                context = {}
                time_list = []
               

                schedule_master = schedule_masters.first()
                context.update(start_date=schedule_master['startDate'])
                context.update(end_date=schedule_master['endDate'])
                context.update(frequency=schedule_master['frequency'])
                context.update(day_of_week=schedule_master['day_of_week'])
                context.update(week_of_month=schedule_master['week_of_month'])

                if schedule_master['schedule_type_id'] == 1: #Daily
                    context.update(schedule_type='Daily')

                if schedule_master['schedule_type_id'] == 2: #Monthly
                    context.update(schedule_type='Monthly')
                    context.update(days=schedule_master['triggerDay'])

                if schedule_master['schedule_type_id'] == 3: #Weekly
                    context.update(schedule_type='Weekly')
                    context.update(days=schedule_master['triggerDay'])

                if schedule_master['schedule_type_id'] == 4: #Once
                    context.update(schedule_type='Once')

                for sch_master in schedule_masters:
                        time_list.append(sch_master['time'].strftime('%H:%M'))

                # times = ','.join(map(str, time_list))
                context.update(times=time_list)
                #print('context*********************')
                #print(context)
                return context

    return None

@csrf_exempt
def Schedular(request, request_id = None):
   
    if request.method == "GET":
        # if 'request_action' in request.session:
        if request.session.get('requestid'): 
            request.session['request_action'] = 'update_request'
            context = get_update_schedular_context(request)
            return render(request, 'hotel/scheduler_hotel.html', context)
        else:
            if request_id and not ('requestid' in request.session):
                request.session['requestid'] = request_id
            context = get_update_schedular_context(request)
            return render(request, 'hotel/scheduler_hotel.html', context)
    else:        
        
        if not request_id:
            request_id = request.session.get('requestid')
        if request_id and not ('requestid' in request.session):
            request.session['requestid'] = request_id
        
        
        req = RequestMaster.objects.get(id=request_id)
        req_mode = req.requestmodeid_id

        hiddenvalue = request.POST['SchedularType']
        hiddenvalue = str(hiddenvalue).strip()

        if 'request_action' in request.session:
            if request.session['request_action'] == 'update_request' and hiddenvalue != "Now":
                ScheduleMaster.objects.filter(request_id=request.session["requestid"]).delete()
                ScheduleDate.objects.filter(sd_reqid=request.session["requestid"]).delete()
       
        if hiddenvalue == "Now":
            response = ServiceCallHandler.simple_get('schedule/', "StartCrawl?requestId=" + str(request_id) + "&requestModeId=" + str(req_mode))
           
            data = {"flag": "1", "req_id": request_id, "data": response.json()}
            return JsonResponse(data)

        model = request.POST['ScheduleData']
        model = eval(model)
        
        if hiddenvalue == "Daily":
            schedulelist = []
            starttime = None
            endtime = None
            for entity in model:
                if 'txtStartDate' in entity:
                    starttime = model[entity]
                elif 'txtEndDate' in entity:
                    endtime = model[entity]
                elif 'txtSchedulTime' in entity:
                    schedulelist = model[entity]

            fromdate = starttime
            todate = endtime
            fromdate = fromdate.split('/')
            todate = todate.split('/')
            start_dt = datetime.date(int(fromdate[2]), int(fromdate[0]), int(fromdate[1]))
            end_dt = datetime.date(int(todate[2]), int(todate[0]), int(todate[1]))

            dailySchedular(end_dt,start_dt,schedulelist,request_id)
            


        elif hiddenvalue == "Weekly":
            schedulelist = []
            starttime = None
            endtime = None
            weekdaydate = None
            week_number = ''
            for entity in model:
                if 'txtW_StartDate' in entity:
                    starttime = model[entity]
                elif 'txtW_EndDate' in entity:
                    endtime = model[entity]
                elif 'txtW_WeekDays' in entity:
                    weekdaydate = model[entity]
                elif 'txtSchedulTime' in entity:
                    schedulelist = model[entity]
                elif 'week_number' in entity:
                    week_number = model[entity]

            fromdate = starttime
            todate = endtime
            inputdays = weekdaydate

            fromdate = fromdate.split('/')
            todate = todate.split('/')
            start_dt = datetime.date(int(fromdate[2]), int(fromdate[0]), int(fromdate[1]))
            end_dt = datetime.date(int(todate[2]), int(todate[0]), int(todate[1]))
            
            weeklySchedular(end_dt,start_dt,inputdays,schedulelist,week_number,request_id)
         

        elif hiddenvalue == "Monthly":
            schedulelist = []
            starttime = None
            endtime = None
            weekdaydate = None
            week_of_month = None
            day_of_week = None
            frequency = None
            month_day = None

            for entity in model:
                if 'txtM_StartDate' in entity:
                    starttime = model[entity]
                elif 'txtM_EndDate' in entity:
                    endtime = model[entity]
                elif 'txtM_Days' in entity:
                    weekdaydate = model[entity]
                elif 'txtSchedulTime' in entity:
                    schedulelist = model[entity]
                elif 'week_of_month' in entity:
                    week_of_month = model[entity]
                elif 'day_of_week' in entity:
                    day_of_week = model[entity]
                elif 'frequency' in entity:
                    frequency = model[entity]                

            starttime = datetime.datetime.strptime(starttime, '%m/%d/%Y')
            startyear = starttime.year
            startmon = starttime.month

            endtime = datetime.datetime.strptime(endtime, '%m/%d/%Y')
            endyear = endtime.year
            endmon = endtime.month

            inputdates = weekdaydate

            start_dt = datetime.date(startyear, startmon, 1)
            ending = calendar.monthrange(endyear, endmon)
            end_dt = datetime.date(endyear, endmon, ending[-1])

            monthlySchedular(end_dt,start_dt,inputdates,schedulelist,frequency,day_of_week,week_of_month,request_id)        


        elif hiddenvalue == "Once":

            onceSchedular(model,request_id)
       

        elif hiddenvalue == '' :
            data = {"flag": "0", "req_id": request_id}
            return JsonResponse(data)
        
        schedtypeid = ScheduleTypeMaster.objects.get(schedtype=hiddenvalue)
        rquest = RequestMaster.objects.filter(id=request_id).update(statustypeid=schedtypeid.id)
        data = {"flag": "1", "req_id": request_id}
        return JsonResponse(data)


@csrf_exempt
def requestmanagement(request):

    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    cur = db.cursor()
    fromdate = None
    todate = None
    fromnextdate = None
    tonextdate = None
    fromcompletedate = None
    tocompletedate = None
    if request.method == 'POST':
        fetchall=0

        requestno = request.POST.get('reqnumber') or 0
        RequestDesc = request.POST.get('RequestDesc') or None
        RequestFromDate = request.POST.get('fromCreateDate') or  None
        RequestToDate = request.POST.get('toCreateDate') or  None
        FromNextScheduleDate = request.POST.get('FromNextScheduleDate') or  None
        TONextScheduleDate = request.POST.get('TONextScheduleDate') or  None
        FromCompletionDate = request.POST.get('FromCompletionDate') or  None
        ToCompletionDate = request.POST.get('ToCompletionDate') or  None
        ReqStatus = request.POST.get('ReqStatus') or  None
        if RequestFromDate!=None and RequestToDate!=None:
            fromdate=datetime.datetime.strptime(RequestFromDate,'%m/%d/%Y').strftime("%Y-%m-%d")
            todate =datetime.datetime.strptime(RequestToDate,'%m/%d/%Y').strftime("%Y-%m-%d")
        if FromNextScheduleDate != None and TONextScheduleDate != None:
            fromnextdate = datetime.datetime.strptime(FromNextScheduleDate, '%m/%d/%Y').strftime("%Y-%m-%d")
            tonextdate = datetime.datetime.strptime(TONextScheduleDate, '%m/%d/%Y').strftime("%Y-%m-%d")

        if FromCompletionDate != None and ToCompletionDate != None:
            fromcompletedate = datetime.datetime.strptime(FromNextScheduleDate, '%m/%d/%Y').strftime("%Y-%m-%d")
            tocompletedate = datetime.datetime.strptime(TONextScheduleDate, '%m/%d/%Y').strftime("%Y-%m-%d")

        args = [requestno, RequestDesc, fromdate , todate, fromnextdate, tonextdate,
                FromCompletionDate, ToCompletionDate, ReqStatus,fetchall]



        cur.callproc(procname="sp_SearchRequestManagement", args=args)
        result = cur.fetchall()
      
        columns = ["RequestRunId", "RequestId", "RequestTitle", "RequestDescription", "ScheduleType", "UserName",
                   "CreatedDatetime",
                   "EndDateTime", "TR", "Completed", "PNF", "Status", "Percent", "ReportDownloadLink"]
        datalist = []
        for x in result:
            datalist.append(dict(tuple(zip(columns, x))))

        return render(request, 'Add_Request/request_management.html',{'datalist':datalist})
    else:
        fetchall=1
        Dashboardstatus = request.GET.get('status')
        DashboardfromDate=request.GET.get('fromDate')
        Dashboardtodate=  request.GET.get('toDate')


        if DashboardfromDate != None and Dashboardtodate != None and Dashboardstatus!=None:
            fromdate = datetime.datetime.strptime(DashboardfromDate, '%d-%m-%Y').strftime("%Y-%m-%d")
            todate = datetime.datetime.strptime(Dashboardtodate, '%d-%m-%Y').strftime("%Y-%m-%d")
            args = [0, 'NULL', fromdate, todate, None, None,None, None, Dashboardstatus, 2]
        else:
            args = [0, 'NULL', str(datetime.datetime.now().date()), str(datetime.datetime.now().date()), None, None,
                None, None, 'NULL',fetchall]

        cur.callproc(procname="sp_SearchRequestManagement", args=args)
        result = cur.fetchall()
       
        columns = ["RequestRunId", "RequestId","RequestTitle","RequestDescription","ScheduleType","UserName","CreatedDatetime",
                    "EndDateTime","TR","Completed","PNF","Status","Percent","ReportDownloadLink"]
        datalist = []
        for x in result:
            datalist.append(dict(tuple(zip(columns,x))))



		

        return render(request, 'hotel/request_management.html', {'datalist': datalist})

def downloadhotelSpecialChar(request):
    data=HotelNameSpecialChars.objects.all()
    filename='HotelSpecialChar'+datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
    filepath=os.path.join(settings.MEDIA_ROOT,'tempfiles',filename+'.csv')
    
    with open(filepath,'w') as file:
        file.write('"SpecialChars","ReplaceChars","Status"\n')
        for rec in data:
            status = 'Active' if rec.IsActive==1 else 'Inactive'
            try:
                file.write('"'+rec.SpecialChars+'","'+rec.ReplaceChars+'","'+status+ '"\n')
            except Exception as e:
                pass

    if os.path.exists(filepath):
        with open(filepath,'rb') as fh:
            response=HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
            return response
    raise http404

        

@csrf_exempt
def keywordRule(request):
   
    msg=None
    if request.method=='POST' and 'SpecialCharFileUpld' in request.FILES:
        file2upload=request.FILES['SpecialCharFileUpld'].readlines()
        
        if len(file2upload) < 2:
             msg = "Input file has no Data"
        else:
            hotelNameSpecial=HotelNameSpecialChars()
            bulk_data=[]
            linecount=0
            for line in file2upload:
                linecount+=1
                if linecount==1:
                    continue
                try:
                    line=line.decode('utf-8').replace('\n','').split(',')
                except UnicodeDecodeError:
                    try:
                        line=line.decode('cp1252').replace('\n','').split(',')
                    except UnicodeDecodeError:
                        continue
                if linecount==1:
                    if line!=['SpecialChars', 'ReplaceChars','Status']: 
                        msg="Invalid Columns please check the template"
                        break
               
                if len(line[0])<1 or len(line[1])<1:
                    msg="Blank values are not allowed."
                    break    
                hotelNameSpecial=HotelNameSpecialChars(SpecialChars=line[0],
                                                        ReplaceChars=line[1],
                                                        IsActive=line[2],
                                                        AddedDate=datetime.datetime.now())
                bulk_data.append(hotelNameSpecial)
            if msg is None:
                db2insert=HotelNameSpecialChars.objects.bulk_create(bulk_data)
                msg='Hotel Name Special Chars Bulk Upload Done'


    if request.method=='POST' and 'txtReplaceSepChar' in request.POST and 'txtSpecialChar' in request.POST:
        db2insert=HotelNameSpecialChars()
        db2insert.SpecialChars=request.POST['txtSpecialChar']
        db2insert.ReplaceChars=request.POST['txtReplaceSepChar']
        db2insert.IsActive=request.POST['POS1']
        db2insert.AddedDate=datetime.datetime.now()
        db2insert.save()
        msg='Special Char Added'

    if request.method=='POST' and 'txtpriority' in request.POST and 'txtroomtype' in request.POST:
        txtactive = request.POST.get('txtactive', None)
        if txtactive is None:
            txtactive = 0
        else:
            txtactive = 1

        db2insert=HotelStandardization()
        db2insert.RoomType=request.POST['txtroomtype']
        db2insert.RoomTypeMatch=request.POST['txtroomtypeMatch']
        db2insert.Priority=request.POST['txtpriority']
        db2insert.RuleType=request.POST['txtruletype']
        db2insert.Active=txtactive
        db2insert.CreatedBy=UserMaster.objects.get(UserName=request.user.UserName)
        db2insert.CreatedDateTime=datetime.datetime.now()
        db2insert.ModifiedBy=UserMaster.objects.get(UserName=request.user.UserName)
        db2insert.ModifiedDatetime=datetime.datetime.now()
        db2insert.save()
        msg='Hotel Standardization Record Added'

    if request.method=='POST' and 'HotelStanFile' in request.FILES:
        file2upload=request.FILES['HotelStanFile'].read()
        file2upload=file2upload.decode('utf-8')
        data=StringIO(file2upload)
        reader=csv.reader(data,delimiter=',')

        datalist = []
        for row in reader:
            datalist.append(row)

        if len(datalist) < 1:
             msg = "Input file has no Data"
        else:

            bulk_data=[]
            linecount=0

            try:
                for row in datalist:
                    linecount+=1
                    db2insert=HotelStandardization()
                    if linecount==1:
                        if row!=['RoomType', 'RoomTypeMatch', 'Priority', 'RuleType', 'Active']:
                            msg="Invalid Columns uploaded Please check the template"
                            break;
                        else:
                            continue
                    if ''.join(row)=='':
                        continue
                    for value in row:
                        if len(value)<1:
                            raise Exception('blankvalue')
                    hotelStand=HotelStandardization(RoomType=row[0],
                                                    RoomTypeMatch=row[1],
                                                    Priority=row[2],
                                                    RuleType=row[3],
                                                    Active=row[4],
                                                    CreatedBy=UserMaster.objects.get(UserName=request.user.UserName),
                                                    CreatedDateTime=datetime.datetime.now(),
                                                    ModifiedBy=UserMaster.objects.get(UserName=request.user.UserName),
                                                    ModifiedDatetime=datetime.datetime.now())
                    bulk_data.append(hotelStand)
            except Exception as e:
                if str(e)=="blankvalue":
                    msg="Value can not be blank while upload"     
            if msg is None:
                db2insert=HotelStandardization.objects.bulk_create(bulk_data)
                msg='Hotel Standardization Bulk Upload done'

    keywordList = KeywordRule.objects.all()
    list1 = []
    for keywords in keywordList:
        act_stat=''
        if keywords.active==1 :
            act_stat='Active'
        else :
            act_stat='InActive'
        user_name = UserMaster.objects.filter(User_ID=keywords.created_by).values_list('UserName', flat=True).first()    
        dict1 = {"roomtype": keywords.roomtype, "roomtypematch": keywords.roomtypematch, "created_by": user_name, "priority": keywords.priority,
                "ruletype": keywords.ruletype, "active":act_stat}
        list1.append(dict1)

    specialCharData=[[i.SpecialChars,i.ReplaceChars,'Active' if i.IsActive==1 else 'Inactive'] for i in HotelNameSpecialChars.objects.all()]

    if msg is None:
        return render(request, 'hotel/keyword_n_rules.html', {
            'keywordList': list1,'SpecialCharData':specialCharData,
            'grid_type': '1'})
    else:
        if request.method=='POST' and 'txtpriority' in request.POST and 'txtroomtype' in request.POST: 
            return render(request, 'hotel/keyword_n_rules.html', {
            'keywordList': list1 ,'msg':msg ,'SpecialCharData':specialCharData,
            'grid_type': '1'})
        elif request.method=='POST' and 'HotelStanFile' in request.FILES :
            return render(request, 'hotel/keyword_n_rules.html', {
            'keywordList': list1 ,'msg':msg ,'SpecialCharData':specialCharData,
            'grid_type': '1'})
        else :
            return render(request, 'hotel/keyword_n_rules.html', {
            'keywordList': list1 ,'msg':msg ,'SpecialCharData':specialCharData,
            'grid_type': '2'})

    
@csrf_exempt
def updatePNFRecrawl(request):

    try:
        req_id = request.POST.get('req_id')
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                             user=settings.DATABASES['default']['USER'],
                             passwd=settings.DATABASES['default']['PASSWORD'],
                             db=settings.DATABASES['default']['NAME'])

        cur = db.cursor()
        args = [req_id]

        res=cur.execute("Update tbl_CrawlRequestDetail set FK_StatusId=9,StartDatetIme=now() where RequestId = %s and FK_StatusId=8",(req_id))
        db.commit()
    except Exception as e:
        traceback. print_exc()
  
    db.close()
    return JsonResponse({'res':''})

@csrf_exempt
def export_data_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="HotelStandardization.csv"'

    writer = csv.writer(response)
    users = HotelStandardization.objects.all().values_list('RoomType', 'RoomTypeMatch', 'Priority', 'RuleType')
    writer.writerow(['RoomType', 'RoomTypeMatch', 'Priority', 'RuleType'])
    for user in users:
        writer.writerow(user)
    return response

@csrf_exempt
def search_export_data_csv(request):
    if request.method == 'POST' or request.is_ajax():
        search_val = request.POST['txt_val']
        if search_val != '': 
            users = HotelNameSpecialChars.objects.filter(SpecialChars__icontains=search_val).values("SpecialChars","ReplaceChars","IsActive") | HotelNameSpecialChars.objects.filter(ReplaceChars__icontains=search_val).values("SpecialChars","ReplaceChars","IsActive") | HotelNameSpecialChars.objects.filter(IsActive__icontains=search_val).values("SpecialChars","ReplaceChars","IsActive")
        else:
            users = HotelNameSpecialChars.objects.filter().values("SpecialChars","ReplaceChars","IsActive")

       
        
        filename='SearchHotelSpecialChar'+datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
        # filepath=os.path.join(settings.MEDIA_ROOT,'tempfiles',filename+'.csv')
        filepath ='/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % filename + '.csv'
        with open(filepath,'w') as file:
            file.write('"SpecialChars","ReplaceChars","IsActive"\n')
            for rec in users:
                file.write('"'+str(rec['SpecialChars'])+'","'+str(rec['ReplaceChars'])+'","'+str(rec['IsActive']) + '"\n')
            

        if os.path.exists(filepath):
            with open(filepath,'rb') as fh:
                filepath = settings.MEDIA_URL + filepath.replace(settings.MEDIA_ROOT, '')
                response=HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                data = {
                    'path':'/static/Excel_file_Dowload_lead_time/%s' % filename + '.csv'
                }
                return JsonResponse(data,safe=False)
                  
        else:
            return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def search_export_data_csv_standard(request):
    if request.method == 'POST' or request.is_ajax():
        search_val = request.POST['txt_val']
        if search_val != '':
            users = HotelStandardization.objects.filter(RoomType__icontains=search_val).values("RoomType","RoomTypeMatch","Priority","RuleType","CreatedBy","Active")  | HotelStandardization.objects.filter(RoomTypeMatch__icontains=search_val).values("RoomType","RoomTypeMatch","Priority","RuleType","CreatedBy","Active") | HotelStandardization.objects.filter(Priority__icontains=search_val).values("RoomType","RoomTypeMatch","Priority","RuleType","CreatedBy","Active") |HotelStandardization.objects.filter(RuleType__icontains=search_val).values("RoomType","RoomTypeMatch","Priority","RuleType","CreatedBy","Active")
            for i in users:
                x = i['CreatedBy']
                name = UserMaster.objects.get(User_ID=x).UserName
                i['CreatedBy'] = name
        else:
            users = HotelStandardization.objects.filter().values("RoomType","RoomTypeMatch","Priority","RuleType","CreatedBy","Active")
            for i in users:
                x = i['CreatedBy']
                name = UserMaster.objects.get(User_ID=x).UserName
                i['CreatedBy'] = name
        

        filename='HotelStandardization'+datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
        # filepath=os.path.join(settings.HOTEL_MEDIA_DOWNLOAD,filename+'.csv')
        filepath='/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % filename + '.csv'
        with open(filepath,'w') as file:
            file.write('"RoomType","RoomTypeMatch","Priority","RuleType","User Name","Active"\n')
            for rec in users:
                file.write('"'+rec['RoomType']+'","'+rec['RoomTypeMatch']+'","'+str(rec['Priority'])+'","'+str(rec['RuleType'])+'","'+rec['CreatedBy']+'","'+str(rec['Active'])+'"\n')
            

        if os.path.exists(filepath):
            with open(filepath,'rb') as fh:
            #  filepath = settings.HOTEL_MEDIA_DOWNLOAD + filename+'.csv'
               
                response=HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                data = {
                    'path':'/static/Excel_file_Dowload_lead_time/%s' % filename + '.csv'
                }
                return JsonResponse(data,safe=False)
                  
        else:
            return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def insertRule(request):
    room = request.POST['roomtype']
    KeywordRule_instance = KeywordRule.objects.create(roomtype = request.POST['roomtype'],roomtypematch = request.POST['roomytypeMatch'],priority = request.POST['priority'],ruletype = request.POST['ruletype'],active = 1,created_by = request.session['UserID'],created_date = '2018-02-02',modified_by = request.session['UserID'],modified_date = '2018-02-02')
    return render(request, 'hotel/keyword_n_rules.html')




#vikash code

def map_group_domain(request):
    if request.method == 'GET':
        return render(request, 'hotel/map_group_domain.html')
    else:
        return JsonResponse({"data": "success"})


def push_to_staging(request):    
    if request.method == 'GET':
        return render(request, 'hotel/push_to_staging.html')
    else:
        return JsonResponse({"data": "success"})


@csrf_exempt
def Bind_request_and_sup_name_by_request_id(request):
    if request.method == 'GET' or request.is_ajax():
        req_id = request.POST['req_id']
        sp_res = sp_get_by_param ('sp_GetSupplierListFromBCD',[req_id])
        data = {
            'compt':sp_res,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt


@csrf_exempt
def Bind_request_and_batch_name(request):
    if request.method == 'GET' or request.is_ajax():        
        list_sp = sp_get_by_param('GetReqeustListForPushToStagingByUser',[int(request.session["UserID"]),int(request.session.get('bli_id'))])
        batch_list = []
        batch_dist = {}
        for Sp_res in list_sp:
            batch_dist = {"id": Sp_res[0], "title": Sp_res[1]}
            batch_list.append(batch_dist)
        # req_master = GetReqeustListForPushToStagingByUser(author=request.session["UserID"])
        # req_master = list(req_master.filter(Q(status_id=3) | Q(created_at__contains=timezone.now().date())).values('title', 'id'))       
        Sp_res_get_all_list=push_to_stage_get_all_data_on_page_load(request.session.get('bli_id'))
        data = {
            'country': batch_list,
             'list':Sp_res_get_all_list
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def Bind_grid_push_to_Stagging(request):
    if request.method == 'GET' or request.is_ajax():        
        Sp_res_get_all_list=push_to_stage_get_all_data_on_page_load(request.session.get('bli_id'))
        data = {
             'list':Sp_res_get_all_list
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



def lead_time_upload(request):
    if request.method == 'GET':
        return render(request, 'hotel/Lead_time_upload.html')
    else:
        return JsonResponse({"data": "success"})


def match_n_unmatch(request):
    if request.method == 'GET':
        return render(request, 'hotel/match_n_unmatch.html')
    else:
        return JsonResponse({"data": "success"})



def match_n_unmatch_download(request):
    if request.method == 'GET':
        return render(request, 'hotel/match_n_unmatch_excel_download.html')
    else:
        return JsonResponse({"data": "success"})

@csrf_exempt
def Bind_city_name_by_sup(request):
    if request.method == 'POST' or request.is_ajax():
        sup_id = request.POST['sup_id']
        country_id = request.POST['country_id']
        cont = sp_get_by_param('sp_GetCityFromHotels_by_sup',[sup_id, country_id])
        countr_list = []
        countr_dist = {}
        for Sp_res in cont:
            countr_dist = {"id": Sp_res[0], "cityname": Sp_res[1]}
            countr_list.append(countr_dist)
        data = {
            'City': countr_list,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def download_excel_match_n_match(request):
    if request.method == 'POST' or request.is_ajax():
        city_id = request.POST['city_id']
        sup_id = request.POST['secondry_sup_id']
        data = {
            'City': 'ok',
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


def group_creation(request):
    if request.method == 'GET':

        return render(request, 'hotel/group_creation.html')
    else:
        return JsonResponse({"data": "success"})

@csrf_exempt
def Bind_grid_by_search(request):
    if request.method == 'GET' or request.is_ajax():
        grp_name = request.POST['grp_name'].split(',')
        act_not = request.POST['act_not'].split(',')
       
        htl_grp_dtls = (HotelGroup.objects.all().annotate(detail_count=Count('hotelgroupdetail')).values('hotelgroup', 'id' ,'_active', 'detail_count'))
        if not grp_name == ['']:
            htl_grp_dtls = htl_grp_dtls.filter(id__in=grp_name)
      
        if act_not == ["1"]:

            htl_grp_dtls = htl_grp_dtls.filter(_active=True)
        if act_not == ["2"]:

            htl_grp_dtls = htl_grp_dtls.filter(_active=False)
        data = {
            'htl_grp_dtls':list(htl_grp_dtls),
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

		

@csrf_exempt
def f_Bind_grp_mapp_detail(request):
    if request.method == 'GET' or request.is_ajax():
        Field_master_data = list(FieldGroupMaster.objects.filter(active=True).values('id','name' ))
        Filed_master_frm_db=list(Filed_master.objects.filter(_active=True).values('id','name' ))
        bli_master= list(BliMaster.objects.filter(Active=True, DomainTypeID=2).values('id','BliName' ))
        data = {
            'Field_master' :Field_master_data,
            'Field_master_db' :Filed_master_frm_db,
            'bli_master':bli_master
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def f_get_grp_mapp_detail(request):
    if request.method == 'GET' or request.is_ajax():
        grp_id = request.POST['grp_id']
        Filed_master_frm_db=list(Filed_group_mapping_detail.objects.filter(fgmd_id=grp_id).values('id','textboxvalue' ))
        Field_master_data = list(FieldGroupMaster.objects.filter(active=True,id=grp_id).values('id','name','description','bli_id' ))
        if Field_master_data[0]['bli_id'] == None:
            bli_master =''
        else:
            bli_master= list(BliMaster.objects.filter(Active=True, DomainTypeID=2,id=Field_master_data[0]['bli_id'] ).values('id','BliName' ))
        data = {
            'Field_master_db' :Filed_master_frm_db, 
            'Field_master_data' :Field_master_data,
            'bli_master' :bli_master
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def f_delete_grp_mapp_detail(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        grp_id = request.POST['grp_id']
        field_dtls = Filed_group_mapping_detail.objects.filter(id=id).delete()
        Filed_master_frm_db=list(Filed_group_mapping_detail.objects.filter(fgmd_id=grp_id).values('id','textboxvalue' ))
        data = {
            'Field_master_db' :Filed_master_frm_db, 
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def f_Save_grp_detail(request):
    if request.method == 'GET' or request.is_ajax():
        grp_name = request.POST['grp_name']
        grp_desc = request.POST['grp_desc']
        user_id = request.session['UserID'] # value by session for user id
        bli_id = request.POST['bli_data']
        grp_id = request.POST['grp_id'].split(',')
        grp_field_name = request.POST['grp_field_name'].split(',')
        grpmapping = FieldGroupMaster.objects.create(name=grp_name, active=True, user_id_id=user_id,description=grp_desc,bli_id=bli_id)      
        for i, x in enumerate(grp_id):
            grp_mapp_dtls = Filed_group_mapping_detail.objects.create(textboxvalue=grp_field_name[i], datatype='Numeric', fgmd_id =grpmapping.id,fgmd_fieldid=x)
        data = {
            'Field_master' :"done",
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



		
@csrf_exempt
def Bind_Country_name(request):
    if request.method == 'GET' or request.is_ajax():
        cont = sp_get_by_param('sp_GetCountryCityFromHotels',[1,0])
        countr_list = []
        countr_dist = {}
        for Sp_res in cont:
            countr_dist = {"countries__id": Sp_res[0], "countries__name": Sp_res[1]}
            countr_list.append(countr_dist)
        
        htls_grp = sp_get_by_param('sp_GetCountryCityFromHotels',[2,0])
        htls_grp_list = []
        htls_grp_dist = {}
        for Sp_res in htls_grp:
            htls_grp_dist = {"id": Sp_res[0], "hotelgroup": Sp_res[1], "detail_count": Sp_res[2], "_active": Sp_res[3]}
            htls_grp_list.append(htls_grp_dist)
        
        #compt =   list(Competitor.objects.filter( ~Q(id = 1) , active=True  ).values('name', 'id'))
        competitors = sp_get('sp_GetAllCompetitors')
        compt = []
        for competitor in competitors:
            compt.append({"id":competitor[0], "name": competitor[1]})

        Field_master = list(FieldGroupMaster.objects.filter(active=True).values('id','name' ))
        htls_status = sp_get_by_param('sp_GetCountryCityFromHotels',[19,0])
        data = {
            'country': countr_list,
            'compt':compt,
            'htl_grp_dtls':htls_grp_list,
            'Field_master' :Field_master,
            'htls_status':htls_status
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Bind_city_name(request):
    if request.method == 'GET' or request.is_ajax():
        country_id = request.POST['Country_id']
        city_grp = sp_get_by_param('sp_GetCountryCityFromHotels',[3,country_id])
        city_grp_list = []
        city_grp_dist = {}
        for Sp_res in city_grp:
            city_grp_dist = {"id": Sp_res[0], "cityname": Sp_res[1]}
            city_grp_list.append(city_grp_dist)
      
        data = {
            'City': city_grp_list,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def autoComplete_hotels(request):
    if request.method == 'GET' or request.is_ajax():
        htls_id = request.POST['prefix']
        City = list(Cities.objects.filter(active=True, countries=1, cityname__icontains=htls_id).values('cityname', 'id'))
        data = {
            'City': City,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Bind_hotel_name(request):
    if request.method == 'GET' or request.is_ajax():
        city_id = request.POST['city_id']
        hotels = list(Hotels.objects.filter(active=True, cityid=city_id).values('HotelName', 'id'))
        data = {
            'hotels': hotels,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Match_unmatch_Bind_hotel_name(request):
    if request.method == 'GET' or request.is_ajax():
        city_id = request.POST['city_id']
        htls_grp = sp_get_by_param('sp_GetCountryCityFromHotels',[4,city_id])
        list1 = []
        dict1 = {}
        for Sp_res in htls_grp:
            dict1 = {"id": Sp_res[0], "HotelName": Sp_res[1]}
            list1.append(dict1)
        data = {
            'hotels': list1,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Bind_hotel_name_for_update(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        hotel_ids = HotelGroupDetail.objects.filter(hotelgroups_id=id).values_list('hotels_id', flat=True)
        result = list(Hotels.objects.filter(active=True, id__in=hotel_ids).values('cityid_id', 'HotelName',
                'cityid__cityname', 'cityid__countries__id', 'cityid__countries__name', 'id'))
        data = {
            'hotels': result,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def DBind_hotel_name_by_sup(request):
    if request.method == 'GET' or request.is_ajax():
        sup_id = request.POST['Sup_id']
        city_id = request.POST['city_id']

        htls_grp = sp_get_by_param('sp_Hotels_by_sup_city',[sup_id,city_id])
        list1 = []
        dict1 = {}
        for Sp_res in htls_grp:
            dict1 = {"id": Sp_res[0], "HotelName": Sp_res[1]}
            list1.append(dict1)

      
        data = {
            'hotels': list1,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


def push_to_stage_get_all_data_on_page_load(bli_id):
    #print('********************')
    #print(bli_id)
    Sp_res_get = sp_get_by_param('sp_get_data_push_to_staging', [int(bli_id)])
    list1 = []
    dict1 = {}
    for Sp_res in Sp_res_get:
        dict1 = {"main_id": Sp_res[0], "Batch_id": Sp_res[1], "Batch_name": Sp_res[2], "Dip_dynamic": Sp_res[3], "status": Sp_res[4],
                "Rep_time": Sp_res[5], "Priority": Sp_res[6],"Status_id":Sp_res[8], "Report_start_time" :Sp_res[19],"Reprot_end_time" :Sp_res[20],
                "Report_Type" :Sp_res[18], "client_priority" :Sp_res[21]}
        list1.append(dict1)
    return list1            
        
            


@csrf_exempt
def Db_push_stag_stopped(request):
    if request.method == 'GET' or request.is_ajax():
        csv_id = request.POST['csv_id']
        session_id = request.session['UserID']
        list_args = [csv_id,session_id]
        sp_res = Sp_res_get = aetos_SP_all_operation_genric('sp_update_data_push_to_status',list_args)
        reqIds = sp_get_by_param('sp_Get_requestId_for_stopped_batches',csv_id)
        ReqIds = []
        if reqIds:
            for i in reqIds:
                ReqIds.append(i[0])
        #print("REQUESTTIIIDDDSSS",ReqIds)
        import pyodbc
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.100.20.24;DATABASE=' + settings.PUSH_DB_NAME + ';UID=dipbag_hm;PWD=!@dipbaghm!@')
        cur = cnxn.cursor()
        # cur.execute("exec sp_StopBatch "+ ReqIds + "")
        cur.execute("{CALL sp_StopBatch (?)}", ReqIds)
        cur.commit()
        Sp_res_get_all_list = push_to_stage_get_all_data_on_page_load(request.session.get('bli_id'))
        if len(Sp_res_get_all_list) > 0:
            data = {
                'htl_grp_dtls': "1",
                'list':Sp_res_get_all_list
            }
            return JsonResponse(data, safe=False)
        else :
            data = {
                'htl_grp_dtls': "0",
            }
            return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Db_push_to_stag_prio_update(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        chk_val = request.POST['chk_val']
        bool_chk_val = 0
        if (chk_val=='true'):
           bool_chk_val=1
        session_id = request.session['UserID']
        list_args = [id,bool_chk_val,session_id]
        sp_res =  aetos_SP_all_operation_genric('sp_update_data_push_to_staging_priority',list_args)
        data = {
            'hotels': "Ok",
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def Push_tostg_db_save(request):
    if request.method == 'GET' or request.is_ajax():
        req_id = request.POST['req_id']
        req_text =request.POST['req_text']
        user_res = request.POST['user_res']


        if (user_res == '0') :
            sp_res_day_chk =  sp_get_by_param('sp_check_data_push_to_staging', req_id)
            #print("PPPPPUUUSSSSHHHHTTOOOO",sp_res_day_chk)

            if sp_res_day_chk:                 
                if sp_res_day_chk[-1][2] == "Completed":
                    error_msg = sp_res_day_chk[0][1] + " batch already send for Push to stagging in system for today. Do you want to re-upload again?"
                    return JsonResponse({"error_msg": error_msg, "error_type": "completed_batch", "htl_grp_dtls": 0}, safe=False)

                if sp_res_day_chk[-1][2] in ["Inqueue","Active"]:
                    error_msg = sp_res_day_chk[0][1] + " batch already send for Push to stagging in system for today. You are not allowed to re-upload again."
                    return JsonResponse({"error_msg": error_msg, "error_type": "active_batch", "htl_grp_dtls": 0}, safe=False)
       
        rad_id_1 = request.POST['rad_fir']
        is_pnf = 0 
        is_hotel_ = ''
        if (rad_id_1=='pnf_yes'):
            is_pnf= 1
        else :
            is_pnf= 0  
        rad_id_prior = request.POST['rad_sec']
        # if (rad_id_2=='htls_bed'):
        #     is_hotel_= 'HB'
        # else :
        #     is_hotel_= 'HBA'
        rad_id_2 = request.session.get('bli_id')
        if (rad_id_2=='1'):
            is_hotel_= settings.HOTEL_BEDS_RPT_TYPE
        else :
            is_hotel_= settings.HOTEL_BEDS_AVL_RPT_TYPE
        prim_sup_id = request.POST['Prim_sup_id']
        sec_sup_id = request.POST['Sec_sup_id']
        
        results = SP_getBatchCountryCode('sp_GetBatchCountryCode', int(req_id), prim_sup_id)        

        if results:
            CountryCode = results[0][0]
            CountryName = results[0][1]
            SupplierName = results[0][2]
        else:
            CountryCode = ''
            CountryName = ''
            SupplierName = ''
       
       
        sp_res= SP_Push_to_staging('sp_Save_data_push_to_staging',req_id,req_text,prim_sup_id,sec_sup_id,is_pnf,is_hotel_,request.session['UserID'],rad_id_prior,rad_id_2,CountryCode,CountryName,SupplierName)
        # for storing data in sql server
        import pyodbc
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.100.20.24;DATABASE='+settings.PUSH_DB_NAME+';UID=dipbag_hm;PWD=!@dipbaghm!@')
        cur = cnxn.cursor()
        cur.execute("exec Sp_Save_data_push_to_staging_229 "+req_id+",'"+req_text+"','"+prim_sup_id+"','"+sec_sup_id+"','"+str(is_pnf)+"','"+is_hotel_+"', '"+ str(request.session['UserID'])+"','"+CountryCode+"','"+CountryName+"','"+SupplierName+"','"+rad_id_prior+"'")
        cur.commit()
        Sp_res_get_all_list = push_to_stage_get_all_data_on_page_load(request.session.get('bli_id'))
        if len(Sp_res_get_all_list) > 0:
            data = {
                'htl_grp_dtls': "1",
                'list':Sp_res_get_all_list
            }
            return JsonResponse(data, safe=False)
        else :
            data = {
                'htl_grp_dtls': "0",
                "error_msg": ""
            }
            return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


def SP_Push_to_staging(sp_name, req_id,req_name,prim_sup_id,Sec_sup_id,is_pnf,is_hotel,userid,prior,bli_id,country_code,country_name,supplier_name):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        cursor = db.cursor()
        args = [req_id,req_name,prim_sup_id,Sec_sup_id,is_pnf,is_hotel,userid,prior,bli_id,country_code,country_name,supplier_name]
        cursor.callproc(procname=sp_name , args=args)
        cursor.close()
        db.commit()


def SP_getBatchCountryCode(sp_name, req_id,suppliers):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        cursor = db.cursor()
        args = [req_id,suppliers]
        cursor.callproc(procname=sp_name , args=args)
        results = list(cursor.fetchall())
        cursor.close()
        db.commit()
        return results


@csrf_exempt
def delete_grp_details(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        htls_grp_main_dtls = HotelGroupDetail.objects.filter(hotelgroups=id).delete()
        htls_dtls=HotelGroup.objects.filter(id=id).delete()
        htl_grp_dtls = list(
           HotelGroup.objects.all().annotate(detail_count=Count('hotelgroupdetail')).values('hotelgroup', 'id'
                                                                                              ,'_active',
                                                                                               'detail_count'))
        data = {
            'htl_grp_dtls': htl_grp_dtls,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Save_htls_details(request):
    if request.method == 'GET' or request.is_ajax():
        grp_name = request.POST['grp_name']
        grp_type = request.POST['grp_type']
        list_hotels = request.POST['list_hotels']
        user = UserMaster.objects.get(User_ID=request.user.User_ID)
        hotelgroup = HotelGroup.objects.create(hotelgroup=grp_name, _active=True, createdby=user,createddate=datetime.datetime.now)
        list_hotels = list_hotels.split(',')
        for i in list_hotels:
            hotel_detail = HotelGroupDetail.objects.create(hotelgroups=hotelgroup, hotels_id=i)

        htl_grp_dtls = list(
            HotelGroup.objects.all().annotate(detail_count=Count('hotelgroupdetail')).values('hotelgroup', 'id'
                                                                                              ,'_active',
                                                                                               'detail_count'))
        data = {
            'hotels': htl_grp_dtls,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def File_download_excel_lead_time(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        if (id=='lead_time'):
            sp_res_1= sp_get('sp_GetLatestLeadTimeTemplate')
        else :
            sp_res_1= sp_get('sp_GetLatestAdhocLeadTimeTemplate')
        list1 = []
        dict1 = {}

    

        for Sp_res in sp_res_1:
            

            dict1 = {"Booking date": '{:%Y-%m-%d}'.format(Sp_res[0]), "Batch Name": Sp_res[1], "Destination": Sp_res[2], "Lead time Value": Sp_res[3],
                    "Event Type Value": Sp_res[4], "Nights": Sp_res[5], "Account Name": Sp_res[6],
                    "Primary": Sp_res[7]}
            list1.append(dict1)
        if len(list1) > 0:
            df = pd.DataFrame(list1)
            if (id=='lead_time'):
               time = 'lead_time_output_excel_%s' % datetime.datetime.now() + ''
            else :
                time = 'lead_time_adhoc_output_excel_%s' % datetime.datetime.now() + ''
            path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=['Booking date', 'Batch Name', 'Destination',
                                                'Lead time Value', 'Event Type Value', 'Nights', 'Account Name','Primary'], index=False)
            writer.save()
            path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
            count=len(list1)
        else :
            count= "0"
            path=""
        data = {
            'htl_grp_dtls': list1,
            'Path':path,
            'count':count
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)



@csrf_exempt
def Fgrid_bind_lead_time(request):
    if request.method == 'GET' or request.is_ajax():
        id = request.POST['id']
        if (id=='lead_time'):
            sp_res_1= sp_get('sp_DisplayLeadTime')
        else :
            sp_res_1= sp_get('sp_DisplayLeadTimeAdhoc')
        list1 = []
        dict1 = {}
        for Sp_res in sp_res_1:
            dict1 = {"Booking_date": Sp_res[0], "Batch_name": Sp_res[1], "Destination": Sp_res[2], "Lead_time_value": Sp_res[3],
                    "Event_time_value": Sp_res[4], "Nights": abs(Sp_res[5]), "NvcrAccountName": Sp_res[6],
                    "NvcrprimarysupplierName": Sp_res[7], "smdtCheckindate": Sp_res[8]}
            list1.append(dict1)
        if len(list1) > 0:
            count=len(list1)
        else :
            count= "0"
        data = {
            'htl_grp_dtls': list1,
            'count':count
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


@csrf_exempt
def File_upload_excel_lead_time(request):
    if request.method == 'GET' or request.is_ajax():
        upload_id = request.POST['id']
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        count =len(dataFrame.columns)

        if (count == 8 and dataFrame.columns[0]=='Booking date' and dataFrame.columns[2]=='Destination'
                and dataFrame.columns[1]=='Batch Name' and dataFrame.columns[5]=='Nights' and dataFrame.columns[7]=='Primary'):

            table_name = ''
            if (upload_id=='lead_time'):
                table_name='tempLeadTime_Excel'
                teamLeadtime.objects.all().delete()
            else :
                table_name= 'tempLeadtimeAdhoc_Excel'
                teamLeadtime_adhoc.objects.all().delete()

            

            import sqlalchemy
            database_username = settings.DATABASES['default']['USER']
            database_password = settings.DATABASES['default']['PASSWORD']
            database_ip       = settings.DATABASES['default']['HOST']
            database_name     = settings.DATABASES['default']['NAME']
            database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(database_username, database_password, 
                                                        database_ip, database_name))
            dataFrame.to_sql(con=database_connection, name= table_name, if_exists='append')

            if (upload_id=='lead_time'):

                sp_res_1= sp_get_by_param('sp_UploadLeadTimeTemplate', request.session['UserID'])
                
                
                list1 = []
                dict1 = {}
                for Sp_res in sp_res_1:
                    dict1 = {"BookingDate": Sp_res[0], "BatchName": Sp_res[1], "Destination" : Sp_res[2], "LeadTime" : Sp_res[3],  "ErrorStatus" : Sp_res[4] }
                    list1.append(dict1)
                if len(list1) > 0:
                    df = pd.DataFrame(list1)
                    time = 'UploadLeadTime_excel_%s' % timezone.now() + ''
                    path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                    writer = pd.ExcelWriter(path)
                    df.to_excel(writer, 'Sheet1', columns=['BookingDate', 'BatchName','Destination', 'LeadTime','ErrorStatus'], index=False)
                    writer.save()
                    path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                    count=len(list1)
                else :
                        count= "0"
                        path=""
                
            else :
  
                sp_res_1= sp_get_by_param('sp_UploadAdhocLeadTimeTemplate', request.session['UserID'])
            
                
                list1 = []
                dict1 = {}
                for Sp_res in sp_res_1:
                    dict1 = {"BookingDate": Sp_res[0], "BatchName": Sp_res[1], "Destination" : Sp_res[2], "LeadTime" : Sp_res[3],  "ErrorStatus" : Sp_res[4] }
                    list1.append(dict1)
                if len(list1) > 0:
                    df = pd.DataFrame(list1)
                    time = 'UploadAdhocLeadTime_excel_%s' % timezone.now() + ''
                    path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                    writer = pd.ExcelWriter(path)
                    df.to_excel(writer, 'Sheet1', columns=['BookingDate', 'BatchName','Destination', 'LeadTime','ErrorStatus'], index=False)
                    writer.save()
                    path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                    count=len(list1)
                else :
                        count= "0"
                        path=""

            

            data = {
                'Path':path,
                'count':count,
                'error':'0',
                'htl_grp_dtls': "file uploaded successfully ",
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





def SP_all_operation(sp_name, userid):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        cursor = db.cursor()
        args = [userid]
        cursor.callproc(procname=sp_name , args=args)
        cursor.close()
        db.commit()



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


@csrf_exempt
def File_upload_excel(request):
    if request.method == 'GET' or request.is_ajax():
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        count=len(dataFrame.columns)
        err_msg_file =''
        dup_grp =''
        if (count>0):
            user = UserMaster.objects.get(User_ID=request.user.User_ID)
            list_unique_grp_name = list(dataFrame.Group_Name.unique())


            if (len (list_unique_grp_name))>0 :
                for lit_i in list_unique_grp_name:
                    htl_grp_name_chk = HotelGroup.objects.filter(_active=True, hotelgroup__iexact=lit_i).exists()
                    if not htl_grp_name_chk:
                        hotelgroup = HotelGroup.objects.create(hotelgroup=lit_i, _active=True, createdby=user, createddate=datetime.datetime.now)
                        df_1_index = dataFrame[dataFrame.Group_Name == lit_i].index.values

                        for index in df_1_index:
                            row = dict(dataFrame.iloc[index])
                        
                            country_id = CountryMaster.objects.get(name__iexact=row['Country'].strip())
                            city_id = Cities.objects.get(cityname__iexact=row['City'].strip(), countries=country_id)
                            hotel_id = Hotels.objects.get(HotelName__iexact=row['Hotels_Name'].strip(), cityid=city_id,comp_id =1)
                
                            HotelGroupDetails_name_chk = HotelGroupDetail.objects.filter(hotelgroups=hotelgroup, hotels_id=hotel_id.id).exists()
                            if not HotelGroupDetails_name_chk:
                                HotelGroupDetail.objects.create(hotelgroups=hotelgroup, hotels_id=hotel_id.id)
                    else :
                        dup_grp =dup_grp+' ,'+lit_i


                HotelGroup.objects.annotate(detail_count=Count('hotelgroupdetail')).filter(detail_count=0).delete()
                htl_grp_dtls = list(
                HotelGroup.objects.all().annotate(detail_count=Count('hotelgroupdetail')).values('hotelgroup', 'id'
                                                                                                ,'_active',
                                                                                               'detail_count'))
                err_msg_file =''
            else :
                htl_grp_dtls=[] 
                err_msg_file ='uploded file can not be empty  !!'  
        else :
            htl_grp_dtls=[] 
            err_msg_file ='Plese select valid upload format !!'                                                                                       
        data = {
            'htl_grp_dtls': htl_grp_dtls,
            'err_msg_file' :err_msg_file,
            'dup_grp' :dup_grp
        }
        os.remove(settings.HOTEL_MEDIA_ROOT+uploaded_filename)

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def chk_grp_name(request):
    if request.method == 'GET' or request.is_ajax():
        grp_name = request.POST['grp_name']
        htl_grp_dtls = HotelGroup.objects.filter(_active=True, hotelgroup__iexact=grp_name).exists()
        if htl_grp_dtls:
            data = {
                'data': grp_name + '  already in Hotel Group !!!!',
            }
        else:
            data = {
                'data': '',
            }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def Update_hotel_list(request):
    if request.method == 'GET' or request.is_ajax():
        grp_name = request.POST['grp_name']
        grp_Id = request.POST['grp_Id']
        list_hotels = request.POST['list_hotels']
        list_db = list(HotelGroupDetail.objects.filter(hotelgroups_id=grp_Id).values_list('hotels', flat=True))
        list_hotels = list_hotels.split(',')
        list_hotels = list(map(int, list_hotels))
        to_be_delete = list(set(list_db) - set(list_hotels))
        to_be_insert = list(set(list_hotels) - set(list_db))
        HotelGroupDetail.objects.filter(hotelgroups_id=grp_Id, hotels_id__in=to_be_delete).delete()
        for i in to_be_insert:
             hotel_detail = HotelGroupDetail.objects.create(hotelgroups_id=grp_Id, hotels_id=i)

        htl_grp_dtls = list(
             HotelGroup.objects.all().annotate(detail_count=Count('hotelgroupdetail')).values('hotelgroup', 'id'
                                                                                              ,'_active',
                                                                                               'detail_count'))
        data = {
            'hotels': htl_grp_dtls,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)


  
@csrf_exempt
def matach_unmatch_upload_excel(request):
    if request.method == 'GET' or request.is_ajax():
        filepath = None
        for k, v in request.FILES.items():
            filepath = v
        fs = FileSystemStorage(location=settings.HOTEL_MEDIA_ROOT)
        uploaded_filename = fs.save(str(filepath), filepath)
        dataFrame = pd.read_excel(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
        rowcount =len(dataFrame)
        count =len(dataFrame.columns)
        if (count ==8 and dataFrame.columns[0]=='Secondary Supplier Company' and dataFrame.columns[1]=='Secondary Supplier Hotel ID'):
            if (rowcount >0):
                    table_name = 'TempExcelMatch_UI'
                    teammatchunmatched.objects.all().delete()
                    
                    import sqlalchemy
                    database_username = settings.DATABASES['default']['USER']
                    database_password = settings.DATABASES['default']['PASSWORD']
                    database_ip       = settings.DATABASES['default']['HOST']
                    database_name     = settings.DATABASES['default']['NAME']
                    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                        format(database_username, database_password, 
                                                                database_ip, database_name))
                    dataFrame.to_sql(con=database_connection, name= table_name, if_exists='append')
                    lst = ['123',request.session['UserID']]
                    sp_res_1 = sp_get_by_param('OfflineMatching_UploadMatch',lst)
                    list1 = []
                    dict1 = {}
                    for Sp_res in sp_res_1:
                        dict1 = {"Secondary Supplier Company": Sp_res[0], "Secondary Supplier Hotel ID": Sp_res[1], "Secondary Supplier Hotel Name" : Sp_res[2], "Primary Supplier Hotel ID" : Sp_res[3],  "Primary Supplier Hotel Code" : Sp_res[4],"Primary Supplier Hotel Name" : Sp_res[5], "City" : Sp_res[6], "Country" : Sp_res[7], "ErrorStatus": Sp_res[8] }
                        list1.append(dict1)
                    if len(list1) > 0:
                        df = pd.DataFrame(list1)
                        time = 'Match_excel_error_output_%s' % timezone.now() + ''
                        path = '/var/www/eCube_Hotel_2/eCube_UI_2/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                        writer = pd.ExcelWriter(path)
                        df.to_excel(writer, 'Sheet1', columns=['Secondary Supplier Company', 'Secondary Supplier Hotel ID','Secondary Supplier Hotel Name', 'Primary Supplier Hotel ID','Primary Supplier Hotel Code', 'Primary Supplier Hotel Name','City',  'Country', 'ErrorStatus'], index=False)
                        writer.save()
                        path = '/static/Excel_file_Dowload_lead_time/%s' % time + '.xlsx'
                        count=len(list1)
                    else :
                            count= "0"
                            path=""
                    data = {
                            'htl_grp_dtls': "file uploded successfully",
                            "path":path,
                            "count":count
                    }
                    os.remove(settings.HOTEL_MEDIA_ROOT+uploaded_filename)
                    return JsonResponse(data, safe=False)
            else : 
                 data = {
                        'error':'1',
                        'htl_grp_dtls': "Excel file can not be empty  !!!",
                        }
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
def f_get_email_by_req_id(request):
    if request.method == 'POST' or request.is_ajax():
        req_ID = request.POST['req_ID']
        req_master_email = RequestMaster.objects.filter(id=req_ID).values('email', 'email_cc').first()
        data = {
            'req_master_email': req_master_email,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)
  

# vikash code end
def getUrlRequest(request):
    req_id = int(request.GET['req_id'])

    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])

    cur = db.cursor()
    query = "select RequestUrl,StartDatetime,EndDatetime,RequestId from tbl_CrawlRequestDetail where RequestId=%d" % req_id
    cur.execute(query)
    dataObj = cur.fetchall()
    dataObjlist = []
    datadict = {}
    for row in dataObj:
        datadict['RequestUrl'] = row[0]
        datadict['StartDatetime'] = row[1]
        datadict['EndDatetime'] = row[2]
        datadict['RequestId'] = row[3]
        dataObjlist.append(datadict)

    dataObjlist = {'dataObjlist': dataObjlist}

    return JsonResponse(dataObjlist)


def aetosGetUrlRequest(request):
    from django.template.loader import get_template
    field_value_template = get_template('Add_Request/field_value.html')
    req_id = int(request.GET['req_id'])
    req = RequestMaster.objects.get(id=req_id)
    if not req.field_group:
        mappings = list()
    else:
        mappings = FieldGroupMapping.objects.filter(
            field_group=req.field_group)
    data = field_value_template.render(
        {'data': {map.field.name: 'value' for map in mappings}})

    return JsonResponse({
        'dataObjlist': [{
            'RequestUrl': obj.request_url,
            'StartDatetime': obj.start_date,
            'EndDatetime': obj.end_date,
            'Data': data,
        } for obj in CrawlRequestDetail.objects.filter(request_id=req_id)]
    })
