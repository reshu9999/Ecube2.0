from django.db import models
from eCube_UI_2.core.Add_Request.models import (DomainMasterBase, RequestModeBase, CountryMasterBase,
                                                FieldGroupMasterBase)
from hotel.user_management.models import UserMaster, DomainMaster, CountryMaster


class RequestModeMaster(RequestModeBase):
    pass


class FieldGroupMaster(FieldGroupMasterBase):
    id = models.AutoField(db_column='GroupID', primary_key=True)
    name = models.CharField(db_column='GroupName', max_length=50)
    description = models.CharField(db_column='GroupDesc', max_length=50)
    active = models.BooleanField(db_column='Active')
    user_id = models.ForeignKey(UserMaster, db_column="FGM_UserId", on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now=True, db_column='CreatedDate')
    bli_id = models.IntegerField(db_column='Bli_ID', default=0)

class temphotelmaster(models.Model):
    id = models.AutoField(db_column='index', primary_key=True)
    class Meta:
        managed = False
        db_table = 'temphotelmaster_excel'



class CityMaster(models.Model):
    id = models.AutoField(db_column='CityId', primary_key=True)
    code = models.CharField(db_column='CityCode', max_length=10)
    name = models.CharField(db_column='CityName',max_length=100)
    country = models.ForeignKey(CountryMaster, db_column="CountryId", on_delete=models.CASCADE)
    _active = models.PositiveSmallIntegerField(db_column='Active', default=0)
    created_by = models.ForeignKey(UserMaster,db_column='CreatedBy', related_name='citymaster_createdby',on_delete = models.DO_NOTHING)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified_by = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='citymaster_modifiedby' ,on_delete = models.DO_NOTHING)
    modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'Cities'

    @property
    def active(self):
        return bool(self._active)


class AirportCodeMaster(models.Model):
    id = models.AutoField(db_column='AirportCodeId', primary_key=True)
    code = models.CharField(db_column='AirportCode', max_length=10)
    name = models.CharField(db_column='AirportName', max_length=100)
    country = models.ForeignKey(CountryMaster, db_column="CountryId", on_delete=models.CASCADE)
    city = models.ForeignKey(CityMaster, db_column="CityId", on_delete=models.CASCADE)
    _active = models.PositiveSmallIntegerField(db_column='Active', default=0)
    created_by = models.ForeignKey(UserMaster,db_column='CreatedBy', related_name='airportcodemaster_created_by' ,on_delete = models.DO_NOTHING)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified_by = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='airportmaster_modified_by' , on_delete = models.DO_NOTHING)
    modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'AirportCodes'

    @property
    def active(self):
        return bool(self._active)


class HotelGroupMaster(models.Model):
    id = models.AutoField(db_column='HotelGroupId', primary_key=True)
    group = models.CharField(db_column='HotelGroup', max_length=200)
    _active = models.PositiveSmallIntegerField(db_column='Active', default=0)
    created_by = models.ForeignKey(UserMaster,db_column='CreatedBy', related_name='hotelgroupmaster_createdby' ,on_delete = models.DO_NOTHING)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified_by = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='hotelgroupmaster_modifiedby', on_delete = models.DO_NOTHING)
    modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'HotelGroups'

    @property
    def active(self):
        return bool(self._active)


class PointOfSaleMaster(models.Model):
    id = models.AutoField(db_column='PointOfSaleId', primary_key=True)
    point_of_sale = models.CharField(db_column='PointOfSale', max_length=100)
    code = models.CharField(db_column='PointOfSaleCode', max_length=10)
    #country = models.ForeignKey(CountryMaster, db_column="CountryId", on_delete=models.CASCADE)
    _active = models.PositiveSmallIntegerField(db_column='Active', default=0)
    created_by = models.ForeignKey(UserMaster,db_column='CreatedBy', related_name='pos_createdby', on_delete = models.DO_NOTHING)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified_by = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='pos_modifiedby', on_delete = models.DO_NOTHING)
    modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'HotelPOS'

    @property
    def active(self):
        return bool(self._active)


class CompetitorMaster(models.Model):
    id = models.AutoField(db_column='CompetitorId', primary_key=True)
    name = models.CharField(db_column='CompetitorName',max_length=256)
    _active = models.BooleanField(db_column='Active',default=True)
    createdDate = models.DateTimeField(db_column='CreatedDate',auto_now=True)
    updatedDate = models.DateTimeField(db_column='ModifiedDate', auto_now_add=True)
    #countries = models.ForeignKey(CountryMaster, db_column='Fk_CountryId', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vw_competitor'


class StarRatingMaster(models.Model):
    id = models.AutoField(db_column='StarRatingId', primary_key=True)
    starrating = models.CharField(db_column='StarRating', max_length=50)
    starratingcode = models.CharField(db_column='StarRatingCode', max_length=50)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='starrratings_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='starratings_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'StarRatings'


class HotelMaster(models.Model):
    id = models.AutoField(db_column='HotelId', primary_key=True)
    website_hotel_id = models.CharField(db_column='WebSiteHotelId', max_length=255)
    name = models.CharField(db_column='HotelName', max_length=512)
    address1 = models.CharField(db_column='HotelAddress1', max_length=255)
    address2 = models.CharField(db_column='HotelAddress2', max_length=255)
    city = models.ForeignKey(CityMaster, db_column='CityId', on_delete=models.CASCADE)
    brand = models.CharField(db_column='HotelBrandName', max_length=50)
    competitorId = models.IntegerField(db_column='CompetitorId')
    star_rating = models.ForeignKey(StarRatingMaster, db_column='StarRatingId', on_delete=models.DO_NOTHING)  #to do foriegn key
    post_code = models.CharField(db_column='HotelPostCode', max_length=255)
    match_status = models.PositiveSmallIntegerField(db_column='HotelMatchStatus')
    description = models.CharField(db_column='HotelDescription', max_length=100)
    is_processed = models.PositiveSmallIntegerField(db_column='isProceesed')
    match_hotel_name = models.CharField(db_column='matchhotelname', max_length=100)
    dipbag_sync_id = models.PositiveIntegerField(db_column='DipBagSyncId')   #to do foriegn key
    is_mailed = models.PositiveSmallIntegerField(db_column='IsMailed')
    is_mailed1 = models.PositiveSmallIntegerField(db_column='IsMailed1')
    _active = models.PositiveSmallIntegerField(db_column='Active', default=0)
    created_by = models.ForeignKey(UserMaster,db_column='CreatedBy', related_name='hotelmaster_created_by' ,on_delete = models.DO_NOTHING)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified_by = models.ForeignKey(UserMaster, db_column='ModifiedBy',related_name='hotelmaster_modified_by', on_delete = models.DO_NOTHING)
    modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    Longitude = models.CharField(db_column='Longitude', max_length=255)
    Latitude = models.CharField(db_column='Latitude', max_length=255)
    ContractManager = models.CharField(db_column='ContractManager', max_length=255)
    DemandGroup = models.CharField(db_column='DemandGroup', max_length=255)
    YieldManager = models.CharField(db_column='YieldManager', max_length=255)
    HotelStatusId = models.IntegerField(db_column='HotelStatusId')

    class Meta:
        managed = False
        db_table = 'Hotels'

    @property
    def active(self):
        return bool(self._active)


class BoardTypeMaster(models.Model):
    id = models.AutoField(db_column='BoardTypeId', primary_key=True)
    boardtypecode = models.CharField(db_column='BoardTypeCode', max_length=50)
    boardtypedescription = models.CharField(db_column='BoardTypeDescription', max_length=50)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='boardtypes_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='boardtypes_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'BoardTypes'

    @property
    def active(self):
        return bool(self._active)


class RoomTypeMaster(models.Model):
    id = models.AutoField(db_column='RoomTypeId', primary_key=True)
    roomtype = models.CharField(db_column='RoomType', max_length=50)
    roomtypecode = models.CharField(db_column='RoomTypeCode', max_length=50)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='roomtypes_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='roomtypes_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'RoomTypes'


class BookingPeriodMaster(models.Model):
    id = models.AutoField(db_column='BookingPeriodID', primary_key=True)
    bookingperiod = models.CharField(db_column='BookingPeriod', max_length=256)
    _active = models.BooleanField(db_column='Active')
    createdby = models.ForeignKey(UserMaster, db_column='CreatedBy', related_name='bookingperiod_created_user',
                                  on_delete=models.DO_NOTHING)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedby = models.ForeignKey(UserMaster, db_column='ModifiedBy', related_name='bookingperiod_modified_user',
                                   on_delete=models.DO_NOTHING)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        managed = False
        db_table = 'BookingPeriod'