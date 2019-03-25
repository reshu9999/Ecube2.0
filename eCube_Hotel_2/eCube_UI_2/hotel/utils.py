# Package Imports
import datetime
import pendulum
import requests
import pandas as pd
from sqlalchemy import create_engine
from .master.models import RequestModeMaster, AirportCodeMaster
from .models import (RequestMaster, FieldGroupMaster, ScheduleMaster, HotelPOS, HotelMaster, HotelGroup,
                     HotelRequestInputDetail, CityMaster, CountryMaster, HotelFlightRequestInputDetail,
                     BookingPeriodMaster, Children, FlightSearchType, ScheduleDate)

# App Imports
from eCube_UI_2.core.resources.responses import AetosResponseBase
from eCube_UI_2.core.resources.db_connectors import MySQLBaseHandler
from eCube_UI_2.core.resources.file_upload import AjaxFileUploaderBase, FileUploadBase

# Django Imports
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from pdb import set_trace as st


class FileUpload(FileUploadBase):
    UPLOAD_TO = settings.HOTEL_UPLOAD_ROOT
    DOWNLOAD_BASE = settings.HOTEL_UPLOAD_URL
    STORAGE = FileSystemStorage


class AjaxFileUploader(AjaxFileUploaderBase):
    FILE_UPLOAD = FileUpload


def dates_between(start, end):
    while start <= end:
        yield start
        start += datetime.timedelta(1)


class AetosResponse(AetosResponseBase):
    RESPONSE = JsonResponse


class PandasSQLUpload(object):
    ENGINE_STRING = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
        settings.DATABASES['default']['USER'],
        settings.DATABASES['default']['PASSWORD'],
        settings.DATABASES['default']['HOST'],
        settings.DATABASES['default']['PORT'],
        settings.DATABASES['default']['NAME']
    )

    @classmethod
    def get_engine(cls):
        return create_engine(cls.ENGINE_STRING, echo=False)


class UploadRequestCreation(MySQLBaseHandler):
    QUERIES = [
        '''
            Select D.`Batch Name` RequestName, D.`Batch Name` RequestDescription, 
            null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
            null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
            Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
            null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
            From temp_Hotel D Left Join tbl_RequestMaster RM
            On D.`Batch Name` = RM.RequestName Where RM.RequestID is NULL;
        ''',
        '''
            Select D.`Batch Name` RequestName, D.`Batch Name` RequestDescription, 
            null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
            null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
            Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
            null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
            From temp_Package D Left Join tbl_RequestMaster RM
            On D.`Batch Name` = RM.RequestName Where RM.RequestID is NULL;
        ''',
    ]

    def process_hotel(self, request):
        hotel_objects = self.fetch_from_query(self.QUERIES[0])
        all_objects = set(hotel_objects)
        self.REQUEST_MODE_ID = 2

        bulk_entry_list = [RequestMaster(
            title=obj[0],
            description=obj[1],
            _csv_filenames=RequestMaster.get_csv_filenames(obj[2]),
            status_id=1,
            field_group=FieldGroupMaster.objects.get(id=obj[7]) if obj[7] else None,
            author=request.user.User_ID,
            modifedby=obj[10],
            scheduled_next=obj[12],
            statustypeid=obj[13],
            requestmodeid=RequestModeMaster.objects.get(id=self.REQUEST_MODE_ID),
            is_pnf_stopper=obj[15],
            BLI_id=request.session.get('bli_id')
        ) for obj in all_objects]

        request_objects = list()
        for obj in bulk_entry_list:
            existing_requests = RequestMaster.objects.filter(title=obj.title)
            if existing_requests:
                obj = existing_requests.last()
            obj.save()
            request_objects.append(obj)

        self.clean_connections()
        print('requests objects***************')
        print(request_objects)
        return request_objects

    def process_flight(self, request):
        package_objects = self.fetch_from_query(self.QUERIES[1])
        all_objects = set(package_objects)
        self.REQUEST_MODE_ID = 3

        bulk_entry_list = [RequestMaster(
            title=obj[0],
            description=obj[1],
            _csv_filenames=RequestMaster.get_csv_filenames(obj[2]),
            status_id=1,
            field_group=FieldGroupMaster.objects.get(id=obj[7]) if obj[7] else None,
            author=request.user.User_ID,
            modifedby=obj[10],
            scheduled_next=obj[12],
            statustypeid=obj[13],
            requestmodeid=RequestModeMaster.objects.get(id=self.REQUEST_MODE_ID),
            is_pnf_stopper=obj[15],
        ) for obj in all_objects]

        request_objects = list()
        for obj in bulk_entry_list:
            obj.save()
            request_objects.append(obj)

        self.clean_connections()
        return request_objects


class UploadScheduleCreation(MySQLBaseHandler):
    QUERIES = [
        '''
            Select 
            CONCAT(SPLIT_STR(StartDate,'-',3),'-',SPLIT_STR(StartDate,'-',2),'-',SPLIT_STR(StartDate,'-',1))  StartDate, 
            CONCAT(SPLIT_STR(EndDate,'-',3),'-',SPLIT_STR(EndDate,'-',2),'-',SPLIT_STR(EndDate,'-',1))  EndDate, 
            TriggerDayDate, Time, Active, SM_ScheduleTypeId, SM_RequestId, CreatedDate, ModifiedDate, Split, 0 frequency
            From 
            (
                Select Distinct Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',1))) StartDate, 
                    Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',2))) EndDate,
                    null TriggerDayDate, 
                    D.`Schedule Time`  `Time`,
                    1 Active, 1 SM_ScheduleTypeId, RM.requestID SM_RequestId,
                    now() CreatedDate, null ModifiedDate, 1 Split 
                From temp_Hotel D Inner Join tbl_RequestMaster RM
                    On D.`Batch Name` = RM.RequestName
                    Where D.`Schedule Frequency` = 'Daily'
                union All
                Select Distinct Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',1))) StartDate, 
                    Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',2))) EndDate,
                    null TriggerDayDate, D.`Schedule Time`  `Time`,
                    1 Active, 1 SM_ScheduleTypeId, RM.requestID SM_RequestId,
                    now() CreatedDate, null ModifiedDate, 1 Split 
                 From temp_Package D Inner Join tbl_RequestMaster RM
                    On D.`Batch Name` = RM.RequestName
                 Where D.`Schedule Frequency` = 'Daily'
                 
             ) A;
        ''',
        '''
            Select 
            CONCAT(SPLIT_STR(StartDate,'-',3),'-',SPLIT_STR(StartDate,'-',2),'-',SPLIT_STR(StartDate,'-',1))  StartDate, 
            CONCAT(SPLIT_STR(EndDate,'-',3),'-',SPLIT_STR(EndDate,'-',2),'-',SPLIT_STR(EndDate,'-',1))  EndDate, 
            TriggerDayDate, Time, Active, SM_ScheduleTypeId, SM_RequestId, CreatedDate, ModifiedDate, Split  
            , frequency
            From 
            (
                Select Distinct Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',1))) StartDate, 
                    Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',2))) EndDate,
                    D.`Which Day of week/month?` TriggerDayDate, 
                    D.`Schedule Time`  `Time`,
                    1 Active, 3 SM_ScheduleTypeId, RM.requestID SM_RequestId,
                    now() CreatedDate, null ModifiedDate, 1 Split
                    , D.`Which Week?` frequency 
                From temp_Hotel D Inner Join tbl_RequestMaster RM
                    On D.`Batch Name` = RM.RequestName
                    Where D.`Schedule Frequency` = 'Weekly'
                union All
                Select Distinct Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',1))) StartDate, 
                    Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',2))) EndDate,
                    D.`Which Day of week/month?` TriggerDayDate, 
                    D.`Schedule Time`  `Time`,
                    1 Active, 3 SM_ScheduleTypeId, RM.requestID SM_RequestId,
                    now() CreatedDate, null ModifiedDate, 1 Split
                    , D.`Which Week?` frequency 
                From temp_Package D Inner Join tbl_RequestMaster RM
                    On D.`Batch Name` = RM.RequestName
                    Where D.`Schedule Frequency` = 'Weekly'
                 
             ) A;
        ''',
        '''
            Select 
            CONCAT(SPLIT_STR(StartDate,'-',3),'-',SPLIT_STR(StartDate,'-',2),'-',SPLIT_STR(StartDate,'-',1))  StartDate, 
            CONCAT(SPLIT_STR(EndDate,'-',3),'-',SPLIT_STR(EndDate,'-',2),'-',SPLIT_STR(EndDate,'-',1))  EndDate, 
            TriggerDayDate, Time, Active, SM_ScheduleTypeId, SM_RequestId, CreatedDate, ModifiedDate, Split  
            ,  frequency, day_of_week, week_of_month
            From 
            (
                Select Distinct Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',1))) StartDate, 
                    Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',2))) EndDate,
                    D.`Which date of month?` TriggerDayDate, 
                    D.`Schedule Time`  `Time`,
                    1 Active, 2 SM_ScheduleTypeId, RM.requestID SM_RequestId,
                    now() CreatedDate, null ModifiedDate, 1 Split
                    , D.`Which Month?` frequency, D.`Which Day of week/month?` day_of_week
                    , D.`Which Week?` week_of_month
                From temp_Hotel D Inner Join tbl_RequestMaster RM
                    On D.`Batch Name` = RM.RequestName
                    Where D.`Schedule Frequency` = 'Monthly'
                union All
                Select Distinct Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',1))) StartDate, 
                    Ltrim(Rtrim(SPLIT_STR(D.`Schedule Duration`,'to',2))) EndDate,
                    D.`Which date of month?` TriggerDayDate, 
                    D.`Schedule Time`  `Time`,
                    1 Active, 1 SM_ScheduleTypeId, RM.requestID SM_RequestId,
                    now() CreatedDate, null ModifiedDate, 1 Split
                    , D.`Which Month?` frequency, D.`Which Day of week/month?` day_of_week
                    , D.`Which Week?` week_of_month
                From temp_Package D Inner Join tbl_RequestMaster RM
                    On D.`Batch Name` = RM.RequestName
                    Where D.`Schedule Frequency` = 'Monthly'
                 
             ) A;
        '''
    ]

    def process(self):
        daily_objects = self.fetch_from_query(self.QUERIES[0])
        weekly_objects = self.fetch_from_query(self.QUERIES[1])
        monthly_objects = self.fetch_from_query(self.QUERIES[2])
        all_objects = daily_objects + weekly_objects + monthly_objects

        schedule_objects = []

        for obj in all_objects:
            if obj[5] == 1:
                end_dt = datetime.datetime.strptime(obj[1], '%Y-%m-%d')
                start_dt = datetime.datetime.strptime(obj[0], '%Y-%m-%d')
                schedulelist = obj[3].split()
                request_id = obj[6]
                list_of_objects = dailySchedular(end_dt, start_dt, schedulelist, request_id)
                if list_of_objects:
                    schedule_objects.extend(list_of_objects)
                    RequestMaster.objects.filter(id=request_id).update(statustypeid=obj[5])
                else:
                    request_object = RequestMaster.objects.get(id=request_id)
                    title = request_object.title
                    print(title)
                    self.update_temp_hotel(title=title)
                    request_object.delete()

            elif obj[5] == 3:
                end_dt = datetime.datetime.strptime(obj[1], '%Y-%m-%d')
                start_dt = datetime.datetime.strptime(obj[0], '%Y-%m-%d')
                inputdays = obj[2]
                schedulelist = obj[3].split()
                request_id = obj[6]
                frequency = obj[10] if obj[10] else None
                list_of_objects = weeklySchedular(end_dt, start_dt, inputdays, schedulelist, frequency, request_id)
                if list_of_objects:
                    schedule_objects.extend(list_of_objects)
                    RequestMaster.objects.filter(id=request_id).update(statustypeid=obj[5])
                else:
                    request_object = RequestMaster.objects.get(id=request_id)
                    title = request_object.title
                    print(title)
                    self.update_temp_hotel(title=title)
                    request_object.delete()

            elif obj[5] == 2:
                end_dt = datetime.datetime.strptime(obj[1], '%Y-%m-%d')
                start_dt = datetime.datetime.strptime(obj[0], '%Y-%m-%d')
                schedulelist = obj[3].split()
                inputdates = obj[2]
                request_id = obj[6]
                frequency = obj[10] if obj[10] else None
                day_of_week = obj[11] if obj[11] else None
                week_of_month = obj[12] if obj[12] else None
                list_of_objects = monthlySchedular(end_dt, start_dt, inputdates, schedulelist, frequency, day_of_week, week_of_month,
                                 request_id)
                if list_of_objects:
                    schedule_objects.extend(list_of_objects)
                    RequestMaster.objects.filter(id=request_id).update(statustypeid=obj[5])
                else:
                    request_object = RequestMaster.objects.get(id=request_id)
                    title = request_object.title
                    print(title)
                    self.update_temp_hotel(title=title)
                    request_object.delete()

        # self.clean_connections()
        return schedule_objects

    def update_temp_hotel(self, title):
        query = 'UPDATE temp_Hotel SET `is_valid`=0 where `Batch Name`="{title}"'.format(title=title)
        self.update_query(query)

class UploadSubRequestCreation(MySQLBaseHandler):
    QUERIES = [
        '''
            Select Distinct
            RequestId,RequestURL,RequestTypeId,
            CONCAT(SPLIT_STR(FromDate,'-',3),'-',SPLIT_STR(FromDate,'-',2),'-',SPLIT_STR(FromDate,'-',1))  FromDate, 
            CONCAT(SPLIT_STR(ToDate,'-',3),'-',SPLIT_STR(ToDate,'-',2),'-',SPLIT_STR(ToDate,'-',1))  ToDate, 
            BookingPeriodID,
            DaysOfWeek,PointOfSaleId,RentalLength,AdvanceDates,AdultId,ChildID,
            CrawlMode,HotelId,CityId,CountryId,StarRating,BoardType,RoomType,
            HotelGroupId,CompetitorIds,CreatedDatetime
            From (
                Select Distinct RM.RequestId, TH.`Check-in & Check-out date Dates` RequestURL, null RequestTypeId,
                    Ltrim(Rtrim(SPLIT_STR(TH.`Start & End Check-in date`,'to',1))) FromDate, 
                    Ltrim(Rtrim(SPLIT_STR(TH.`Start & End Check-in date`,'to',2))) ToDate,
                    Case When TH.`Start & End Check-in date` != '' Then 1 
                         When TH.`Advance Dates` != '' Then 2
                         When TH.`Check-in & Check-out date Dates` != '' Then 3
                    End BookingPeriodID,
                    TH.Days DaysOfWeek, POS.PointOfSaleId, TH.Nights RentalLength,  
                    TH.`Advance Dates` AdvanceDates, TH.Adults AdultId,	TH.Children ChildID,
                    Case When ifnull(TH.Hotel ,'') = '' Then 1 else 2 End CrawlMode,
                    H.HotelId HotelId, C.CityID CityId, CM.CountryID CountryId,
                    Null StarRating, Null BoardType, Null RoomType,
                    Null HotelGroupId, 
                    fn_GetSupplierID(TH.`Supplier 1`,    TH.`Supplier 2`,    TH.`Supplier 3`,    TH.`Supplier 4`,
                    TH.`Supplier 5`,    TH.`Supplier 6`,    TH.`Supplier 7`,    TH.`Supplier 8`,
                    TH.`Supplier 9`,    TH.`Supplier 10`,    TH.`Supplier 11`,    TH.`Supplier 12`,
                    TH.`Supplier 13`,    TH.`Supplier 14`,    TH.`Supplier 15`,    TH.`Supplier 16`,
                    TH.`Supplier 17`,    TH.`Supplier 18`,    TH.`Supplier 19`,    TH.`Supplier 20`) 
                    CompetitorIds,
                    now() CreatedDatetime
    
                From temp_Hotel TH
                    Inner Join tbl_RequestMaster RM On TH.`Batch Name` = RM.requestname
                    Inner Join HotelPOS POS On TH.`Source Market` = POS.PointOfSaleCode
                    Inner Join tbl_CountryMaster CM On TH.Country = CM.CountryName
                    Inner Join Cities C On TH.destination = C.Cityname 
                    Left Join Adults A On TH.Adults = A.adult	
                    Left Join Children CL On TH.Children = CL.Child
                    Left Join Hotels H On TH.Hotel = H.HotelName
                        And C.CityId = H.CityId
                        And H.competitorId = 1
             ) A;
        ''',
        '''
            Select Distinct
            RequestId,RequestURL,RequestTypeId,CreatedDatetime,
            UpdatedDatetime,
            CONCAT(SPLIT_STR(FromDate,'-',3),'-',SPLIT_STR(FromDate,'-',2),'-',SPLIT_STR(FromDate,'-',1))  FromDate, 
            CONCAT(SPLIT_STR(ToDate,'-',3),'-',SPLIT_STR(ToDate,'-',2),'-',SPLIT_STR(ToDate,'-',1))  ToDate, 
            BookingPeriodId,DaysOfWeek,PointOfSaleId,
            RentalLength,AdvanceDates,AdultId,
            ChildID,CrawlMode,HotelId,StarRating,BoardType,RoomType,
            CompetitorIds,FlightSearchTypeID,
            FromAirportCodeId,ToAirportCodeId
            From (
                Select  RM.RequestId, TH.`Check-in & Check-out date Dates` RequestURL,
                    null RequestTypeId, now() CreatedDatetime, null UpdatedDatetime,
                    Ltrim(Rtrim(SPLIT_STR(TH.`Start & End Check-in date`,'to',1))) FromDate, 
                    Ltrim(Rtrim(SPLIT_STR(TH.`Start & End Check-in date`,'to',2))) ToDate,
                    Case When TH.`Start & End Check-in date` != '' Then 1 
                         When TH.`Advance Dates` != '' Then 2
                         When TH.`Check-in & Check-out date Dates` != '' Then 3
                    End BookingPeriodID,
                    TH.Days DaysOfWeek, POS.PointOfSaleId, TH.`Nights` RentalLength,  
                    TH.`Advance Dates` AdvanceDates, A.AdultId AdultId,	CL.ChildID ChildID,
                    Case When ifnull(TH.Hotel ,'') = '' Then 1 else 2 End CrawlMode,
                    H.HotelId HotelId, 
                    Null StarRating, Null BoardType, Null RoomType,
                    fn_GetSupplierID(TH.`Supplier 1`,    TH.`Supplier 2`,    TH.`Supplier 3`,    TH.`Supplier 4`,
                    TH.`Supplier 5`,    TH.`Supplier 6`,    TH.`Supplier 7`,    TH.`Supplier 8`,
                    TH.`Supplier 9`,    TH.`Supplier 10`,    TH.`Supplier 11`,    TH.`Supplier 12`,
                    TH.`Supplier 13`,    TH.`Supplier 14`,    TH.`Supplier 15`,    TH.`Supplier 16`,
                    TH.`Supplier 17`,    TH.`Supplier 18`,    TH.`Supplier 19`,    TH.`Supplier 20`) 
                    CompetitorIds, 1 FlightSearchTypeID,
                    DAC.AirportCodeId FromAirportCodeId, 
                    AAC.AirportCodeId ToAirportCodeId
                
                From temp_Package TH
                    Inner Join tbl_RequestMaster RM On TH.`Batch Name` = RM.requestname
                    Inner Join HotelPOS POS On TH.`source market` = POS.PointOfSaleCode
                    Inner Join tbl_CountryMaster CM On TH.country = CM.countryname
                    Inner Join Cities C On TH.destination = C.Cityname
                    Left Join AirportCodes DAC On TH.`Departure Airport Code` = DAC.AirportCode
                    Left Join AirportCodes AAC On TH.`Arrival Airport Code` = AAC.AirportCode
                    Left Join Adults A On TH.Adults = A.adult	
                    Left Join Children CL On TH.Children = CL.Child
                    Left Join Hotels H On TH.Hotel = H.HotelName
                        And C.CityId = H.CityId
                        And H.competitorId = 1
            ) A; 
    
        '''
    ]

    @classmethod
    def yyyy_dd_mm_to_yyyy_mm_dd(cls, date_string):
        if date_string:
            date_parts = date_string.split('-')
            return "-".join([date_parts[0], date_parts[2], date_parts[1]])
        else:
            return None

    def dd_mm_yyyy_to_mm_dd_yyyy(self, date_list):
        if date_list:
            date_format = "%d-%m-%Y"
            date_list = [datetime.datetime.strptime(val, date_format) for val in date_list]
            date_format = "%m-%d-%Y"
            date_list = [datetime.datetime.strftime(val, date_format) for val in date_list]
            return ','.join(date_list)
        else:
            return None

    def multipleCheckIn(self, date_string):
        if date_string:
            all_dates = date_string.replace('to', '').split(' ')
            all_dates = [i for i in all_dates if i != '']
            all_dates = [i.strip(';') for i in all_dates]
            multipleCheckInDates = [j for i, j in enumerate(all_dates) if i % 2 == 0]

            return self.dd_mm_yyyy_to_mm_dd_yyyy(multipleCheckInDates)
        else:
            return None

    def convert_checkin_to_advance_dates(self, date_string):
        if date_string:
            all_dates = date_string.replace('to', '').split(' ')
            all_dates = [i for i in all_dates if i != '']
            all_dates = [i.strip(';') for i in all_dates]
            multipleCheckInDates = [j for i, j in enumerate(all_dates) if i % 2 == 0]

            date_format = "%d-%m-%Y"
            date_list = [datetime.datetime.strptime(val, date_format) for val in multipleCheckInDates]
            advance_days = []
            for checkin_date in date_list:
                advance_days.append(str((checkin_date.date() - datetime.datetime.now().date()).days))
            return ','.join(advance_days)
        else:
            return None

    def NoOfNights(self, date_string, nights):
        if date_string:
            all_dates = date_string.replace('to', '').split(' ')
            all_dates = [i for i in all_dates if i != '']
            all_dates = [i.strip(';') for i in all_dates]
            multipleCheckInDates = [j for i, j in enumerate(all_dates) if i % 2 == 0]
            date_format = "%d-%m-%Y"
            dt_0 = [datetime.datetime.strptime(j, date_format) for i, j in enumerate(all_dates) if i % 2 == 0][0]
            dt_1 = [datetime.datetime.strptime(j, date_format) for i, j in enumerate(all_dates) if i % 2 != 0][0]
            NoOfNights = dt_1 - dt_0
            NoOfNights = int(NoOfNights.days)

            return NoOfNights

        return nights.replace(";", ",")


    def process(self):
        hotel_objects = self.fetch_from_query(self.QUERIES[0])

        package_objects = self.fetch_from_query(self.QUERIES[1])

        hotel_bulk_entry_list = [HotelRequestInputDetail(

            requests=RequestMaster.objects.get(id=obj[0]),
            requesturl=obj[1],
            requesttypeid=obj[2],
            fromdate=self.yyyy_dd_mm_to_yyyy_mm_dd(obj[3]),
            todate=self.yyyy_dd_mm_to_yyyy_mm_dd(obj[4]),
            bookingperiods=BookingPeriodMaster.objects.get(id=obj[5]),
            DaysOfWeek=obj[6],
            pointofsales=HotelPOS.objects.get(id=obj[7]),
            rentallength=obj[8].replace(";", ",") if obj[8] and obj[9] else self.NoOfNights(obj[1], obj[8]),
            advancedates=obj[9].replace(";", ',') if obj[9] else self.multipleCheckIn(obj[1]),
            adults=obj[10] if obj[10] else 0,
            #children=Children.objects.get(child=obj[11]).id if obj[11] else Children.objects.get(child=0).id,
            children=obj[11] if obj[11] else 0,
            crawlmode=obj[12],
            hotels=HotelMaster.objects.get(id=obj[13]) if obj[13] else None,
            cities=CityMaster.objects.get(id=obj[14]),
            countries=CountryMaster.objects.get(id=obj[15]),
            starrating=obj[16],
            boardtype=obj[17],
            roomtype=obj[18],
            hotelgroups=HotelGroup.objects.get(id=obj[19]) if obj[19] else None,
            suppliers=obj[20],
            createddatetime=obj[21],
        ) for obj in hotel_objects]

        for obj in hotel_objects:
            if obj[1] and obj[9]:
                hotel_bulk_entry_list.append(HotelRequestInputDetail(
                    requests=RequestMaster.objects.get(id=obj[0]),
                    requesturl=obj[1],
                    requesttypeid=obj[2],
                    fromdate=self.yyyy_dd_mm_to_yyyy_mm_dd(obj[3]),
                    todate=self.yyyy_dd_mm_to_yyyy_mm_dd(obj[4]),
                    bookingperiods=BookingPeriodMaster.objects.get(id=obj[5]),
                    DaysOfWeek=obj[6],
                    pointofsales=HotelPOS.objects.get(id=obj[7]),
                    rentallength=self.NoOfNights(obj[1], obj[8]),
                    advancedates=self.convert_checkin_to_advance_dates(obj[1]),
                    adults=obj[10] if obj[10] else 0,
                    # children=Children.objects.get(child=obj[11]).id if obj[11] else Children.objects.get(child=0).id,
                    children=obj[11] if obj[11] else 0,
                    crawlmode=obj[12],
                    hotels=HotelMaster.objects.get(id=obj[13]) if obj[13] else None,
                    cities=CityMaster.objects.get(id=obj[14]),
                    countries=CountryMaster.objects.get(id=obj[15]),
                    starrating=obj[16],
                    boardtype=obj[17],
                    roomtype=obj[18],
                    hotelgroups=HotelGroup.objects.get(id=obj[19]) if obj[19] else None,
                    suppliers=obj[20],
                    createddatetime=obj[21],
                ))

        hf_bulk_entry_list = [HotelFlightRequestInputDetail(
            requests=RequestMaster.objects.get(id=obj[0]),
            requesturl=obj[1],
            requesttypeid=obj[2],
            createddatetime=obj[3],
            updatedatetime=obj[4],
            fromdate=self.yyyy_dd_mm_to_yyyy_mm_dd(obj[5]),
            todate=self.yyyy_dd_mm_to_yyyy_mm_dd(obj[6]),
            bookingperiods=BookingPeriodMaster.objects.get(id=obj[7]),
            DaysOfWeek=obj[8],
            pointofsales=HotelPOS.objects.get(id=obj[9]),
            rentallength=obj[10] if obj[10] else self.NoOfNights(obj[1]),
            advancedates=obj[11].replace(";", ',') if obj[11] else self.multipleCheckIn(obj[1]),
            adults=obj[12] if obj[12] else 0,
            #children=Children.objects.get(child=obj[13]).id if obj[13] else Children.objects.get(child=0).id,
            children=obj[13] if obj[13] else 0,
            crawlmode=obj[14],
            hotels=HotelMaster.objects.get(id=obj[15]),
            StarRating=obj[16],
            boardtype=obj[17],
            roomtype=obj[18],
            suppliers=obj[19],
            flightSearchTypeID=FlightSearchType.objects.get(id=obj[20]),
            fromAirportCodeId=AirportCodeMaster.objects.get(id=obj[21]),
            toAirportCodeId=AirportCodeMaster.objects.get(id=obj[22]),
        ) for obj in package_objects]

        hotel_sub_request_objects = list()
        for obj in hotel_bulk_entry_list:
            obj.save()
            hotel_sub_request_objects.append(obj)

        hf_sub_request_objects = list()
        for obj in hf_bulk_entry_list:
            obj.save()
            hf_sub_request_objects.append(obj)

        self.clean_connections()
        return hotel_sub_request_objects, hf_sub_request_objects
        # return list(), list()


class ExcelBatchUploadHandler(MySQLBaseHandler):

    def __init__(self, file_upload):
        self.host = settings.DATABASES['default']['HOST']
        self.user = settings.DATABASES['default']['USER']
        self.password = settings.DATABASES['default']['PASSWORD']
        self.db_name = settings.DATABASES['default']['NAME']
        super(ExcelBatchUploadHandler, self).__init__(self.host, self.user, self.password, self.db_name)
        self._upload = file_upload

    @property
    def _get_hotel_batchnames(self):
        return [o[0] for o in self.fetch_from_query('SELECT * FROM eCube_Centralized_DB.temp_Hotel')]

    @property
    def _get_package_batchnames(self):
        return [o[0] for o in self.fetch_from_query('SELECT * FROM eCube_Centralized_DB.temp_Package')]

    def update_db_hotel(self, request):
        self.create_temp_tables()
        self.clean_temp_tables()

        h_new_batches = None
        invalid_batches_path = None
        # try:
        if True:
            print('inside try')
            self.upload_excel_into_temp_tables_hotel()
            hotel_titles = self._get_hotel_batchnames
            old_batches = RequestMaster.objects.filter(title__in=hotel_titles)
            old_batches.delete()
            req_objs = self.add_request_entries_hotel(request)

            if req_objs:
                sch_objs = self.add_schedule_entries()
                if sch_objs:
                    h_sub_req_objs, hf_sub_req_objs = self.add_sub_request_entries()
                    self.update_procedure('sp_HotelDateDetails', 1)
                    self.update_procedure('sp_HotelDateDetails', 2)
                    h_new_batches = RequestMaster.objects.filter(id__in=[sr.requests.id for sr in h_sub_req_objs])

                    invalid_batches_path = self.export_invalid_batches_to_csv()  # write non scheduled batches to csv

        # self.clean_temp_tables()
        self.clean_connections()
        return h_new_batches, invalid_batches_path

    def export_invalid_batches_to_csv(self):
        conn = PandasSQLUpload.get_engine()
        file_path = 'InvalidBatches/' + str(datetime.datetime.now()) + '.csv'
        query = 'SELECT `Batch Name`,`Country`,`Destination`,`Hotel`,`Adults`,`Children`,' \
                '`Check-in & Check-out date Dates`,`Advance Dates`,`Start & End Check-in date`,' \
                '`Days`,`Nights`,`Supplier 1`,`Supplier 2`,`Supplier 3`,`Supplier 4`,`Supplier 5`,' \
                '`Supplier 6`,`Supplier 7`,`Supplier 8`,`Supplier 9`,`Supplier 10`,`Supplier 11`,`Supplier 12`,' \
                '`Supplier 13`,`Supplier 14`,`Supplier 15`,`Supplier 16`,`Supplier 17`,`Supplier 18`,' \
                '`Supplier 19`,`Supplier 20`,`Schedule Duration`,`Schedule Frequency`,`Which Week?`,' \
                '`Which Day of week/month?`,`Which Month?`,`Which date of month?`,`Schedule Time` from' \
                ' temp_Hotel where `is_valid`=0'

        df = pd.read_sql(sql=query, con=conn)

        if df.empty:
            return None

        df['ErrorMessage'] = "No Schedule date exists within given parameters. Please update the specified parameters."
        df.to_csv(settings.STATIC_ROOT + file_path, index=False)
        return file_path


    def update_db_flight(self, request):
        self.create_temp_tables()
        self.clean_temp_tables()
        hf_new_batches = None
        # try:
        if True:
            print('inside try')
            self.upload_excel_into_temp_tables_flight()
            package_titles = self._get_package_batchnames

            old_batches = RequestMaster.objects.filter(title__in=package_titles)
            old_batches.delete()

            req_objs = self.add_request_entries_flight(request)
            if req_objs:
                sch_objs = self.add_schedule_entries()
                h_sub_req_objs, hf_sub_req_objs = self.add_sub_request_entries()

                self.update_procedure('sp_HotelDateDetails', 1)
                self.update_procedure('sp_HotelDateDetails', 2)
                hf_new_batches = RequestMaster.objects.filter(id__in=[sr.requests.id for sr in hf_sub_req_objs])

        self.clean_temp_tables()
        self.clean_connections()
        return hf_new_batches

    def add_request_entries_hotel(self, request):
        return UploadRequestCreation(self.host, self.user, self.password, self.db_name).process_hotel(request)

    def add_request_entries_flight(self, request):
        return UploadRequestCreation(self.host, self.user, self.password, self.db_name).process_flight(request)

    def add_schedule_entries(self):
        return UploadScheduleCreation(self.host, self.user, self.password, self.db_name).process()

    def add_sub_request_entries(self):
        x = UploadSubRequestCreation(self.host, self.user, self.password, self.db_name).process()
        return x

    def upload_excel_into_temp_tables_hotel(self):
        print('upload_excel_into_temp_tables_hotel.................. start')
        xls = pd.ExcelFile(self._upload.uploaded_path)
        df_hotel = pd.read_excel(xls, 'Hotel')
        conn = PandasSQLUpload.get_engine()
        df_hotel.to_sql(name="temp_Hotel", con=conn, if_exists='append', index=False)
        print('upload_excel_into_temp_tables_hotel.................. end')

    def upload_excel_into_temp_tables_flight(self):
        xls = pd.ExcelFile(self._upload.uploaded_path)
        df_package = pd.read_excel(xls, 'Package')
        conn = PandasSQLUpload.get_engine()
        df_package.to_sql(name="temp_Package", con=conn, if_exists='append', index=False)

    def create_temp_tables(self):
        cur = self._cursor()

        query = "create table if not exists temp_Hotel (`Batch Name` varchar(1000),Country varchar(1000),Destination varchar(1000),Hotel varchar(1000),`Source Market` varchar(1000),Adults varchar(1000),Children varchar(1000),`Check-in & Check-out date Dates` varchar(1000),`Advance Dates` varchar(1000), `Start & End Check-in date` varchar(1000), Days varchar(1000), `Nights` varchar(1000),`Supplier 1` varchar(1000),`Supplier 2` varchar(1000),`Supplier 3` varchar(1000),`Supplier 4` varchar(1000),`Supplier 5` varchar(1000),`Supplier 6` varchar(1000),`Supplier 7` varchar(1000),`Supplier 8` varchar(1000),`Supplier 9` varchar(1000),`Supplier 10` varchar(1000),`Supplier 11` varchar(1000),`Supplier 12` varchar(1000),`Supplier 13` varchar(1000),`Supplier 14` varchar(1000),`Supplier 15` varchar(1000),`Supplier 16` varchar(1000),`Supplier 17` varchar(1000),`Supplier 18` varchar(1000),`Supplier 19` varchar(1000), `Supplier 20` varchar(1000),`Schedule Duration` varchar(1000),`Schedule Frequency` varchar(1000),`Which Week?` varchar(1000),`Which Day of week/month?` varchar(1000), `Which Month?` varchar(1000),`Which date of month?` varchar(1000),`Schedule Time` varchar(1000))"
        cur.execute(query)

        query = "create table if not exists temp_Package (`Batch Name` varchar(1000),Country varchar(1000),Destination varchar(1000),Hotel varchar(1000),`Source Market` varchar(1000),Adults varchar(1000),Children varchar(1000),`Check-in & Check-out date Dates` varchar(1000),`Advance Dates` varchar(1000), `Start & End Check-in date` varchar(1000), Days varchar(1000), `Nights` varchar(1000), `Departure Airport Code` varchar(100), `Arrival Airport Code` varchar(100), `Supplier 1` varchar(1000),`Supplier 2` varchar(1000),`Supplier 3` varchar(1000),`Supplier 4` varchar(1000),`Supplier 5` varchar(1000),`Supplier 6` varchar(1000),`Supplier 7` varchar(1000),`Supplier 8` varchar(1000),`Supplier 9` varchar(1000),`Supplier 10` varchar(1000),`Supplier 11` varchar(1000),`Supplier 12` varchar(1000),`Supplier 13` varchar(1000),`Supplier 14` varchar(1000),`Supplier 15` varchar(1000),`Supplier 16` varchar(1000),`Supplier 17` varchar(1000),`Supplier 18` varchar(1000),`Supplier 19` varchar(1000), `Supplier 20` varchar(1000), `Schedule Duration` varchar(1000),`Schedule Frequency` varchar(1000),`Which Week?` varchar(1000),`Which Day of week/month?` varchar(1000), `Which Month?` varchar(1000),`Which date of month?` varchar(1000),`Schedule Time` varchar(1000))"
        cur.execute(query)

        cur.close()

    def clean_temp_tables(self):
        cur = self._cursor()

        query = "truncate temp_Hotel;"
        cur.execute(query)

        query = "truncate temp_Package;"
        cur.execute(query)

        cur.close()


class ServiceCallHandler(object):
    SERVICE_BASE_URL = 'http://localhost'
    VERSION_PATH = 'api/v1/'

    SERVICE_PORT = {
        'SCHEDULE': '8001',
        'MONGO_API': '8002',
        'PROXY_API': '8003',
        'MAIL': '8004',
    }

    @classmethod
    def simple_get(cls, service_name, end_point):
        port = cls.SERVICE_PORT[service_name.replace('/','').upper()]
        url = "%s:%s/%s%s" % (cls.SERVICE_BASE_URL, port, cls.VERSION_PATH, end_point)
        print("NOW Service Call URL")
        print(url)
        return requests.get(url)


def dailySchedular(end_dt, start_dt, schedulelist, request_id):
    schedule_master = None

    for schtime in schedulelist:
        schedule_master = ScheduleMaster.objects.create(
            startDate=start_dt, endDate=end_dt, time=schtime,
            schedule_type_id=1, request_id=RequestMaster.objects.get(id=request_id),
            createDt=datetime.datetime.now()
        )

    listofdates = []
    for n in range(int((end_dt - start_dt).days) + 1):
        thisdate = start_dt + datetime.timedelta(n)
        listofdates.append(thisdate.strftime('%Y-%m-%d'))

    for sch in listofdates:
        for schtime in schedulelist:
            schedule = ScheduleDate()
            schedule.ScheduleMasterId = 1
            schedule.ScheduleDate = sch
            schedule.ScheduleTime = schtime
            schedule.Status = "Pending"  # schedular has not yet started
            schedule.sd_reqid = RequestMaster.objects.get(id=request_id)
            schedule.save()

    if not listofdates:
        if schedule_master:
            ScheduleMaster.objects.filter(request_id_id=request_id).delete()

    return listofdates


def weeklySchedular(end_dt, start_dt, inputdays, schedulelist, week_number, request_id):
    week_number = week_number if week_number else None
    schedule_master = None

    for schtime in schedulelist:
        schedule_master = ScheduleMaster.objects.create(
            startDate=start_dt, endDate=end_dt, time=schtime,
            schedule_type_id=3, request_id=RequestMaster.objects.get(id=request_id),
            createDt=datetime.datetime.now(), triggerDay=inputdays,
            frequency=week_number
        )
    listofdates = []
    for n in range(int((end_dt - start_dt).days) + 1):
        thisdate = start_dt + datetime.timedelta(n)
        pend = pendulum.parse(thisdate.strftime('%Y-%m-%d'))

        if week_number:
            if thisdate.strftime('%a') in inputdays and pend.week_of_month == int(week_number):
                listofdates.append(thisdate.strftime('%Y-%m-%d'))
        elif thisdate.strftime('%a') in inputdays:
            listofdates.append(thisdate.strftime('%Y-%m-%d'))

    for sch in listofdates:
        for schtime in schedulelist:
            schedule = ScheduleDate()
            schedule.ScheduleDate = sch
            schedule.ScheduleTime = schtime
            schedule.Status = "Pending"
            schedule.sd_reqid = RequestMaster.objects.get(id=request_id)
            schedule.save()

    if not listofdates:
        if schedule_master:
            ScheduleMaster.objects.filter(request_id_id=request_id).delete()

    return listofdates



def monthlySchedular(end_dt, start_dt, inputdates, schedulelist, frequency, day_of_week, week_of_month, request_id):
    DAY_OF_WEEK = {
        "0": "Sunday",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday",
    }
    msg = ""
    schedule_master = None
    print('inputdates = ',inputdates)
    print('frequency = ',frequency)
    print('day of week = ',day_of_week)
    print('week of month = ',week_of_month)
    week_of_month = int(week_of_month) if week_of_month else None
    frequency = int(frequency) if frequency else None
    for schtime in schedulelist:
        print('sch time = ', schtime)
        schedule_master = ScheduleMaster.objects.create(
            startDate=start_dt, endDate=end_dt, time=schtime,
            schedule_type_id=2, request_id=RequestMaster.objects.get(id=request_id),
            createDt=datetime.datetime.now(), triggerDay=inputdates,
            frequency=frequency, day_of_week=day_of_week,
            week_of_month=week_of_month
        )

    listofdates = []
    for n in range(int((end_dt - start_dt).days) + 1):
        thisdate = start_dt + datetime.timedelta(n)

        pend = pendulum.parse(thisdate.strftime('%Y-%m-%d'))
        this_month = pend.month
        this_week = pend.week_of_month
        this_day = pend.day_of_week

        if frequency:
            if day_of_week and week_of_month:
                if (str(frequency) == str(this_month)) and (
                        str(this_week) == str(week_of_month) and (DAY_OF_WEEK[str(this_day)] == str(day_of_week))):
                    listofdates.append(thisdate.strftime('%Y-%m-%d'))
        elif (str(frequency) == str(this_month)) and str(thisdate.day) in [i.replace(' ', '') for i in
                                                                           inputdates.split(',')]:
            listofdates.append(thisdate.strftime('%Y-%m-%d'))

        elif str(thisdate.day) in [i.replace(' ', '') for i in inputdates.split(',')]:
            listofdates.append(thisdate.strftime('%Y-%m-%d'))
        elif 'Last' in inputdates and thisdate.day == 28:
            nextmonth = thisdate + datetime.timedelta(4)
            lastday = nextmonth - datetime.timedelta(nextmonth.day)
            listofdates.append(lastday.strftime('%Y-%m-%d'))

    for sch in listofdates:
        for schtime in schedulelist:
            schedule = ScheduleDate()
            schedule.ScheduleMasterId = 1
            schedule.ScheduleDate = sch
            schedule.ScheduleTime = schtime
            schedule.Status = "Pending"
            schedule.sd_reqid = RequestMaster.objects.get(id=request_id)
            schedule.save()

    if not listofdates:
        if schedule_master:
            ScheduleMaster.objects.filter(request_id_id=request_id).delete()

    return listofdates


def onceSchedular(model, request_id):
    schedule = ScheduleDate()
    schedule.ScheduleDate = datetime.datetime.strptime(model['txtDate'], "%m/%d/%Y")
    schedule.ScheduleTime = model['txtTime']
    schedule.Status = "Pending"
    schedule.sd_reqid = RequestMaster.objects.get(id=request_id)
    schedule.save()

    start_dt = datetime.datetime.strptime(model['txtDate'], "%m/%d/%Y")

    ScheduleMaster.objects.create(
        startDate=start_dt, time=model['txtTime'],
        schedule_type_id=4, request_id=RequestMaster.objects.get(id=request_id),
        createDt=datetime.datetime.now()
    )
