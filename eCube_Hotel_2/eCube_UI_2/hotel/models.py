from django.db import models
from eCube_UI_2.core.Add_Request.models import RequestMasterBase, ScheduleMasterBase, CrawlRequestDetailBase
from hotel.user_management.models import Competitor
from hotel.master.models import (CountryMaster, CityMaster, AirportCodeMaster, HotelMaster, UserMaster, DomainMaster,
                                 RequestModeMaster, BookingPeriodMaster, FieldGroupMaster, BoardTypeMaster,
                                 RoomTypeMaster, StarRatingMaster)


class RequestMaster(RequestMasterBase):
    requestmodeid = models.ForeignKey(RequestModeMaster, db_column='RequestModeId', on_delete=models.DO_NOTHING)
    field_group = models.ForeignKey(FieldGroupMaster, db_column='FK_GroupId', on_delete=models.CASCADE)
    statustypeid = models.IntegerField(db_column='FK_ScheduleTypeId')


class ScheduleMaster(ScheduleMasterBase):
    schedule_type_id = models.IntegerField(db_column='SM_ScheduleTypeId')
    request_id = models.ForeignKey(RequestMaster, db_column='SM_RequestId', on_delete=models.DO_NOTHING)


class Adult(models.Model):
    id = models.AutoField(db_column='AdultId', primary_key=True)
    adult = models.IntegerField(db_column='Adult')
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='adult_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='adult_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'Adults'


class AdvanceDay(models.Model):
    id = models.AutoField(db_column='AdvanceDayId', primary_key=True)
    advanceday = models.IntegerField(db_column='AdvanceDay')
    advancedaytext = models.CharField(db_column='AdvanceDayText', max_length=50)
    specifictype = models.IntegerField(db_column='SpecificType')
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='advancedays_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='advancedays_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'AdvanceDays'


class Children(models.Model):
    id = models.AutoField(db_column='ChildID', primary_key=True)
    child = models.CharField(db_column='Child', max_length=100)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='children_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='children_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'Children'


# vikash code

class teamLeadtime(models.Model):
    id = models.AutoField(db_column='index', primary_key=True)
    class Meta:
        managed = False
        db_table = 'tempLeadTime_Excel'


class temp_hotel_only(models.Model):
    id = models.AutoField(db_column='index', primary_key=True)
    class Meta:
        managed = False
        db_table = 'temp_Hotel_UI'

class temp_hotel_Flight(models.Model):
    id = models.AutoField(db_column='index', primary_key=True)
    class Meta:
        managed = False
        db_table = 'temp_Hotel_Flight_UI'


class teammatchunmatched(models.Model):
    id = models.AutoField(db_column='index', primary_key=True)
    class Meta:
        managed = False
        db_table = 'TempExcelMatch_UI'



class teamLeadtime_adhoc(models.Model):
    id = models.AutoField(db_column='index', primary_key=True)
    class Meta:
        managed = False
        db_table = 'tempLeadtimeAdhoc_Excel'

class Filed_master(models.Model):
    id = models.AutoField(db_column='Fmid', primary_key=True)
    name = models.CharField(db_column='FieldName', max_length=100)
    _active = models.BooleanField(db_column='Active')
    Domainid =models.IntegerField(db_column='DomainTypeid')
    class Meta:
        managed = False
        db_table = 'tbl_FieldMaster'

class Filed_group_mapping_detail(models.Model):
    id = models.AutoField(db_column='GrMapID', primary_key=True)
    textboxvalue = models.CharField(db_column='TextBoxValue', max_length=100)
    datatype = models.CharField(db_column='DataType', max_length=100)
    fgmd_id =models.IntegerField(db_column='FGMD_GroupID')
    fgmd_fieldid =models.IntegerField(db_column='FGMD_FieldID')
    created_date = models.DateTimeField(auto_now=True, db_column='CreatedDate')
    class Meta:
        managed = False
        db_table = 'tbl_FieldGroupMappingDetails'



# class request_master(models.Model):
#     Req_id = models.AutoField(db_column='RequestId', primary_key=True)
#     Req_Name = models.CharField(db_column='RequestName', max_length=100)
#     class Meta:
#         managed = False
#         db_table = 'tbl_Request_Master'


class batchcrawldata(models.Model):
    id = models.AutoField(db_column='intBatchCrawlID', primary_key=True)
    sup_id = models.IntegerField(db_column='intSupplierId')
    class Meta:
        managed = False
        db_table = 'BatchCrawlData'



class Cities(models.Model):
    id = models.AutoField(db_column='CityId', primary_key=True)
    citycode = models.CharField(db_column='CityCode', max_length=10)
    cityname = models.CharField(db_column='CityName', max_length=100)
    countries = models.ForeignKey(CountryMaster, db_column='CountryId', on_delete=models.DO_NOTHING)
    active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='cities_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='cities_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'Cities'


# class RoomTypes(models.Model):
#     id = models.AutoField(db_column='RoomTypeId', primary_key=True)
#     roomtype = models.CharField(db_column='RoomType', max_length=50)
#     roomtypecode = models.CharField(db_column='RoomTypeCode', max_length=50)
#     active = models.BooleanField(db_column='Active')
#     createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='roomtypes_created_user',
#                                   on_delete=models.DO_NOTHING)
#     createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
#     modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='roomtypes_modified_user',
#                                    on_delete=models.DO_NOTHING)
#     modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'RoomTypes'   


class HotelPOS(models.Model):
    id = models.AutoField(db_column='PointOfSaleId', primary_key=True)
    posale = models.CharField(db_column='PointOfSale', max_length=100)
    poscode = models.CharField(db_column='PointOfSaleCode', max_length=10)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='pos_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='pos_related_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'HotelPOS'


class HotelGroup(models.Model):
    id = models.AutoField(db_column='HotelGroupId', primary_key=True)
    hotelgroup = models.CharField(db_column='HotelGroup', max_length=200)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='hotelgroups_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='hotelgroups_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'HotelGroups'

  
class Hotels(models.Model):
    id = models.AutoField(db_column='HotelId', primary_key=True)
    WebSiteHotelId = models.IntegerField(db_column='WebSiteHotelId')
    HotelName = models.CharField(db_column='HotelName', max_length=512)
    HotelAddress1 = models.CharField(db_column='HotelAddress1', max_length=255)
    HotelAddress2 = models.CharField(db_column='HotelAddress2', max_length=255)
    cityid = models.ForeignKey(Cities, db_column='CityId', on_delete=models.DO_NOTHING)
    comp_id = models.ForeignKey(Competitor,db_column='CompetitorId',on_delete=models.DO_NOTHING)
    hotelbrandname = models.CharField(db_column='HotelBrandName', max_length=50)
    # roomtypes = models.ForeignKey(RoomTypeMaster, db_column='RoomTypeId', on_delete=models.DO_NOTHING)
    # boardtypes = models.ForeignKey(BoardTypeMaster, db_column='BoardTypeId', on_delete=models.DO_NOTHING)
    starratings = models.ForeignKey(StarRatingMaster, db_column='StarRatingId', on_delete=models.DO_NOTHING)
    hotelpostcode = models.CharField(db_column='HotelPostCode', max_length=255)
    # domains = models.ForeignKey(DomainMaster, db_column='DomainId', on_delete=models.DO_NOTHING)
    hotelmatchstatus = models.BooleanField(db_column='HotelMatchStatus', default=True)
    hoteldescription = models.CharField(db_column='HotelDescription', max_length=100)
    isproceesed = models.BooleanField(db_column='isProceesed', default=True)
    matchhotelname = models.CharField(db_column='matchhotelname', max_length=100)
    dipbagsyncid = models.IntegerField(db_column='DipBagSyncId')
    ismailed = models.BooleanField(db_column='IsMailed', default=True)
    requests = models.ForeignKey(RequestMaster, db_column='RequestId', on_delete=models.DO_NOTHING)
    ismailed1 = models.BooleanField(db_column='ismailed1', default=True)
    active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='hotels_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='hotels_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'Hotels'


class KeywordRule(models.Model):
    id = models.IntegerField(db_column='HotelStandId', primary_key=True)
    roomtype = models.CharField(db_column='RoomType', max_length=500)
    roomtypematch = models.CharField(db_column='RoomTypeMatch', max_length=50)
    priority = models.IntegerField(db_column='Priority')
    ruletype = models.CharField(db_column='RuleType', max_length=50)
    active = models.IntegerField(db_column='Active')
    # created_by = models.ForeignKey(UserMaster,db_column='CreatedBy', related_name='hotelstand_createdby' ,on_delete = models.DO_NOTHING)
    # created_date = models.DateTimeField(db_column='CreatedDateTime', auto_now_add=True)
    # modified_by = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='hotelstand_modifiedby', on_delete = models.DO_NOTHING)
    # modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)
    created_by = models.IntegerField(db_column='CreatedBy')
    created_date = models.DateTimeField(db_column='CreatedDateTime')
    modified_by = models.IntegerField(db_column='ModifiedBy')
    modified_date = models.DateTimeField(db_column='ModifiedDatetime')

    class Meta:
        managed = False
        db_table = 'HotelStandardization'


class HotelGroupDetail(models.Model):
    id = models.AutoField(db_column='hotelgroupdetailsid', primary_key=True)
    hotelgroups = models.ForeignKey(HotelGroup, db_column="HotelGroupId", on_delete=models.DO_NOTHING)
    hotels = models.ForeignKey(HotelMaster, db_column='HotelId', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'HotelGroupDetails'


class ScheduleDate(models.Model):
    scheduleid = models.IntegerField(db_column='ScheduleDatesId', primary_key=True)
    sd_reqid = models.ForeignKey(RequestMaster, db_column='SD_RequestId', on_delete=models.CASCADE)
    ScheduleDate = models.DateTimeField(db_column='ScheduleDate', null=False)
    ScheduleTime = models.TimeField(db_column='ScheduleTime', null=False)
    Status = models.CharField(db_column='Status', max_length=10)
    CreatedDatetime = models.DateTimeField(db_column='CreatedDatetime', null=False, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_ScheduleDate'


class ScheduleTypeMaster(models.Model):
    id = models.IntegerField(db_column='ShedulId', primary_key=True)
    schedtype = models.CharField(db_column='ScheduleType', max_length=20)
    active = models.BooleanField(db_column='Active', default=1)
    createdDt = models.DateTimeField(db_column='CreatedDate')
    modifiedDt = models.DateTimeField(db_column='ModifiedDate')

    class Meta:
        managed = False
        db_table = 'tbl_ScheduleTypeMaster'
#
#
# class ScheduleMaster(models.Model):
#     scheduleid = models.IntegerField(db_column='ScheduleMasterId', primary_key=True)
#     startDate = models.DateField(db_column='StartDate', null=False)
#     endDate = models.DateField(db_column='EndDate', null=False)
#     triggerDay = models.CharField(db_column='TriggerDayDate', null=True, max_length=200)
#     time = models.TimeField(db_column='Time', null=False)
#     active = models.BooleanField(db_column='Active', null=False, default=1)
# TODO: fix this on_delete=False
#     sm_scheduleType = models.ForeignKey(ScheduleTypeMaster, db_column='SM_ScheduleTypeId', on_delete=False)
#     sm_reqid = models.ForeignKey(RequestMaster, db_column='SM_RequestId', on_delete=False)
#     createDt = models.DateTimeField(db_column='CreatedDate', null=False, auto_now_add=True)
#     modifiedDt = models.DateTimeField(db_column='ModifiedDate', null=True)
#     split = models.IntegerField(db_column='Split', null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'tbl_ScheduleMaster'
#

class HotelRequestInputDetail(models.Model):
    id = models.AutoField(db_column='HotelReqestInputDetailsId', primary_key=True)
    requests = models.ForeignKey(RequestMaster, db_column='RequestId', on_delete=models.DO_NOTHING)
    requesturl = models.CharField(db_column='RequestURL', max_length=500, blank=True, null=True)
    requesttypeid = models.IntegerField(db_column='RequestTypeId', blank=True, null=True)
    fromdate = models.DateTimeField(db_column='FromDate')
    todate = models.DateTimeField(db_column='ToDate')
    bookingperiods = models.ForeignKey(BookingPeriodMaster, db_column='BookingPeriodId', on_delete=models.DO_NOTHING)
    DaysOfWeek = models.CharField(db_column='DaysOfWeek', max_length=100)
    pointofsales = models.ForeignKey(HotelPOS, db_column='PointOfSaleId', on_delete=models.DO_NOTHING)
    rentallength = models.CharField(db_column='RentalLength', max_length=1000)
    advancedates = models.CharField(db_column='AdvanceDates', max_length=1000)
    adults = models.IntegerField(db_column='AdultId')
    children = models.IntegerField(db_column='ChildID')
    crawlmode = models.IntegerField(db_column='CrawlMode')
    hotels = models.ForeignKey(HotelMaster, db_column='HotelId', on_delete=models.DO_NOTHING, null=True)
    cities = models.ForeignKey(CityMaster, db_column='CityId', on_delete=models.DO_NOTHING)
    countries = models.ForeignKey(CountryMaster, db_column='CountryId', on_delete=models.DO_NOTHING)
    starrating = models.CharField(db_column='StarRating', max_length=500)
    boardtype = models.CharField(db_column='BoardType', max_length=512)
    roomtype = models.CharField(db_column='RoomType', max_length=512)
    hotelgroups = models.ForeignKey(HotelGroup, db_column='HotelGroupId', on_delete=models.DO_NOTHING)
    suppliers = models.CharField(db_column='CompetitorIds', max_length=512)
    createddatetime = models.DateTimeField(db_column='CreatedDatetime', auto_now_add=True)
    # TODO: who ever is using this add required columns in Staging DB
    reporttype = models.CharField(db_column='ReportType', max_length=45)


    class Meta:
        managed = False
        db_table = 'tbl_hotelrequestinputdetails'


class HotelRequestsDateDetail(models.Model):
    id = models.AutoField(db_column='HotelRequestsDateDetailId', primary_key=True)
    hotelrequestinputdetailsid = models.ForeignKey(HotelRequestInputDetail, db_column='HotelRequestInputDetailsId', on_delete=models.DO_NOTHING)
    checkindate = models.DateField(db_column='CheckInDate')
    checkoutdate = models.DateField(db_column='CheckOutDate')
    createddatetime = models.DateTimeField(db_column='CreatedDatetime', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_HotelRequestsDateDetails'


class FlightSearchType(models.Model):
    id = models.AutoField(db_column='FlightSearchTypeID',primary_key=True)
    flightsearchTypeID = models.CharField(db_column='FlightSearchType',max_length=100)
    _active = models.SmallIntegerField(db_column='Active',default=1)
    createdby = models.ForeignKey(UserMaster,db_column='CreatedBy',related_name = 'Flight_Createdby',max_length=11,on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate',auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster,db_column='ModifiedBy',max_length=11,on_delete=models.DO_NOTHING)
    modifieddatetime = models.DateTimeField(db_column='ModifiedDatetime',default=None)

    class Meta:
        managed = False
        db_table = 'FlightSearchType'


class HotelFlightRequestInputDetail(models.Model):
    id = models.AutoField(db_column='hotelflightrequestinputdetailsId', primary_key=True)
    requests = models.ForeignKey(RequestMaster, db_column='RequestId', on_delete=models.DO_NOTHING)
    requesturl = models.CharField(db_column='RequestURL', max_length=500, blank=True, null=True)
    requesttypeid = models.IntegerField(db_column='RequestTypeId', blank=True, null=True)
    createddatetime = models.DateTimeField(db_column='CreatedDatetime', auto_now_add=True)
    updatedatetime = models.DateTimeField(db_column='UpdatedDatetime', default=None)
    fromdate = models.DateTimeField(db_column='FromDate')
    todate = models.DateTimeField(db_column='ToDate')
    bookingperiods = models.ForeignKey(BookingPeriodMaster, db_column='BookingPeriodId', on_delete=models.DO_NOTHING)
    DaysOfWeek = models.CharField(db_column='DaysOfWeek', max_length=100)
    pointofsales = models.ForeignKey(HotelPOS, db_column='PointOfSaleId', on_delete=models.DO_NOTHING)
    rentallength = models.CharField(db_column='RentalLength', max_length=1000)
    advancedates = models.CharField(db_column='AdvanceDates', max_length=1000)
    fromAirportCodeId = models.ForeignKey(AirportCodeMaster, db_column='FromAirportCodeId', related_name='From_Airport',
                                          on_delete=models.DO_NOTHING)
    toAirportCodeId = models.ForeignKey(AirportCodeMaster, db_column='ToAirportCodeId', related_name='To_Airport',
                                        on_delete=models.DO_NOTHING)
    adults = models.IntegerField(db_column='AdultId')
    children = models.IntegerField(db_column='ChildID')
    crawlmode = models.IntegerField(db_column='CrawlMode')
    hotels = models.ForeignKey(HotelMaster, db_column='HotelId', on_delete=models.DO_NOTHING)
    StarRating = models.CharField(db_column='StarRating', max_length=500)
    boardtype = models.CharField(db_column='BoardType', max_length=512)
    roomtype = models.CharField(db_column='RoomType', max_length=512)
    suppliers = models.CharField(db_column='CompetitorIds', max_length=512)
    flightSearchTypeID = models.ForeignKey(FlightSearchType, db_column='FlightSearchTypeID',
                                           on_delete=models.DO_NOTHING)
    reporttype = models.CharField(db_column ='ReportType',max_length=45)
    HotelGroupId = models.IntegerField(db_column='HotelGroupId')
    # email = models.CharField(db_column='Email',max_length=1000)
    # email_cc = models.CharField(db_column='EmailCC',max_length=1000)

    class Meta:
        managed = False
        db_table = 'tbl_hotelflightrequestinputdetails'


class HotelFlightRequestsDateDetail(models.Model):
    id = models.AutoField(db_column='hotelflightRequestsDateDetailId', primary_key=True)
    hotelflightrequestinputdetailsId = models.ForeignKey(HotelFlightRequestInputDetail,
                                                         db_column='hotelflightrequestinputdetailsId',
                                                         on_delete=models.DO_NOTHING)
    checkindate = models.DateField(db_column='CheckInDate')
    checkoutdate = models.DateField(db_column='CheckOutDate')
    createddatetime = models.DateTimeField(db_column='CreatedDatetime', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_hotelflightRequestsDateDetail'


class HotelStandardization(models.Model):
    id=models.AutoField(db_column='HotelStandID', primary_key=True)
    RoomType=models.CharField(db_column='RoomType',max_length=500)
    RoomTypeMatch=models.CharField(db_column='RoomTypeMatch', max_length=50)
    Priority=models.IntegerField(db_column='Priority')
    RuleType=models.CharField(db_column='RuleType',max_length=50)
    Active=models.IntegerField(db_column='Active')
    CreatedBy=models.ForeignKey(UserMaster,db_column='CreatedBy',on_delete=models.DO_NOTHING,related_name='CreatedBy_usr')
    CreatedDateTime=models.DateField(db_column='CreatedDateTime')
    ModifiedBy=models.ForeignKey(UserMaster,db_column='ModifiedBy',on_delete=models.DO_NOTHING,related_name='ModifiedBy_usr')
    ModifiedDatetime=models.DateField(db_column='ModifiedDatetime')

    class Meta:
        managed= False
        db_table = 'HotelStandardization'


class HotelNameSpecialChars(models.Model):
    id=models.AutoField(db_column='HotelNameSpecialCharsId', primary_key=True)
    SpecialChars=models.CharField(db_column='SpecialChars',max_length=500)
    ReplaceChars=models.CharField(db_column='ReplaceChars',max_length=500)
    IsActive=models.IntegerField(db_column='IsActive')
    AddedDate=models.DateField(db_column='AddedDate')

    class Meta:
        managed=False
        db_table='HotelNameSpecialChars'


class HotelCrawlRequestDetail(CrawlRequestDetailBase):
    request_id = models.PositiveIntegerField(RequestMaster, db_column='RequestId')

    # class Meta:
    #     managed = False
    #     db_table = 'tbl_HotelCrawlRequestDetail'
