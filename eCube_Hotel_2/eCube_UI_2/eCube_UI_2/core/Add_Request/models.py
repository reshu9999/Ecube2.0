from django.db import models


class CountryMasterBase(models.Model):
    id = models.AutoField(db_column="CountryID", primary_key=True)
    name = models.CharField(db_column="CountryName", max_length=30)
    _active = models.PositiveSmallIntegerField(db_column="Active")

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_CountryMaster'


class DomainMasterBase(models.Model):
    id = models.IntegerField(db_column='DomainId', primary_key=True)
    domainname = models.CharField(db_column='DomainName', max_length=50, null=False)
    active = models.BooleanField(db_column='Active')
    competitorid = models.PositiveIntegerField(null=True)
    scrapingscriptname =models.CharField(db_column='ScrapingScriptName', max_length=500, null=True)
    parsingscriptname =models.CharField(db_column='ParsingScriptName', max_length=500, null=True)
    scrapingconfigscriptname =models.CharField(db_column='scrapingconfigscriptname', max_length=500, null=True)
    parsingconfigscriptname =models.CharField(db_column='parsingconfigscriptname', max_length=500, null=True)
    updated_datetime = models.DateTimeField(auto_now=True, db_column='CreatedDatetime')
    created_datetime = models.DateTimeField(auto_now_add=True, db_column='UpdatedDatetime')
    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_DomainMaster'


class RequestModeBase(models.Model):
    id = models.AutoField(db_column='RequestModeId', primary_key=True)
    requestmode = models.CharField(db_column='RequestMode', max_length=50)
    active = models.BooleanField(db_column='Active')
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifieddate = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'RequestMode'


class RequestMasterBase(models.Model):
    id = models.AutoField(db_column='RequestId', primary_key=True)
    title = models.CharField(db_column='RequestName', max_length=50)
    _csv_filenames = models.CharField(db_column='RequestFile', max_length=500)
    description = models.TextField(db_column='RequestDescription')
    BLI_id = models.IntegerField(db_column='FK_BliId')
    scheduled_next = models.DateTimeField(db_column='NextScheduleDateTime')
    statustypeid = models.IntegerField(db_column='FK_ScheduleTypeId')
    status_id = models.IntegerField(db_column='FK_StatusId')
    is_pnf_stopper = models.SmallIntegerField(db_column='IsPNFStopper')
    author = models.IntegerField(db_column='CreatedBy')
    modifedby = models.IntegerField(db_column='UpdatedBy')
    created_at = models.DateTimeField(db_column='CreatedDatetime', auto_now_add=True)
    email = models.CharField(db_column='Email',max_length=1000)
    email_cc = models.CharField(db_column='EmailCC',max_length=1000)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_RequestMaster'

    @property
    def filenames(self):
        return self._csv_filenames.split(',')

    @classmethod
    def get_csv_filenames(cls, filenames):
        if filenames and not isinstance(filenames, list):
            filenames = [filenames]
        elif not filenames:
            return ''
        return ','.join(filenames)


class RequestRunDetailBase(models.Model):
    id = models.AutoField(db_column='RequestRunId', primary_key=True)
    request_obj = models.ForeignKey(RequestMasterBase, db_column='FK_RequestId', on_delete=models.CASCADE)
    download_link = models.CharField(db_column='ReportDownloadLink', max_length=1000)
    started_at = models.DateTimeField(db_column='StartDatetIme')
    ended_at = models.DateTimeField(db_column='EndDateTime')

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_RequestRunDetail'


class FieldMasterBase(models.Model):
    id = models.AutoField(db_column='FMId', primary_key=True)
    name = models.CharField(db_column='FieldName', max_length=30)
    active = models.BooleanField(db_column='Active')
    # domain = models.ForeignKey(DomainMaster, db_column='DomainTypeId', on_delete=models.CASCADE)
    createdDt = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedDt = models.DateTimeField(db_column='ModifiedDate', auto_now=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_FieldMaster'


class FieldGroupMasterBase(models.Model):
    id = models.AutoField(db_column='GroupID', primary_key=True)
    name = models.CharField(db_column='GroupName', max_length=50)
    description = models.CharField(db_column='GroupDesc', max_length=50)
    active = models.BooleanField(db_column='Active')
    # user_id = models.ForeignKey(UserMaster, db_column="FGM_UserId", on_delete=False)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_Field_Group_Master'


class FieldGroupMappingBase(models.Model):
    id = models.AutoField(db_column='GrMapID', primary_key=True)
    text_box = models.CharField(db_column='TextBoxValue', max_length=100)
    data_type = models.CharField(db_column='DataType', max_length=50)
    # field_group = models.ForeignKey(Field_Group_Master, db_column='FGMD_GroupID', on_delete=models.CASCADE)
    # field = models.ForeignKey(FieldMaster, db_column='FGMD_FieldId', max_length=50, on_delete=models.CASCADE)
    createdDt = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modifiedDt = models.DateTimeField(db_column='ModifiedDate', auto_now=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_FieldGroupMappingDetails'


class StatusBase(models.Model):
    id = models.AutoField(db_column='StatusId', primary_key=True)
    name = models.CharField(db_column='StatusTitle', max_length=100)
    created = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified = models.DateTimeField(db_column='ModifiedDate', auto_now=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_StatusMaster'


class RequestInputDetailsBase(models.Model):
    id = models.AutoField(db_column="ReqInputDetailId", primary_key=True)
    # request_id = models.ForeignKey(RequestMaster, db_column="Fk_RequestId", on_delete=models.CASCADE)
    url = models.CharField(db_column="RequestURL", max_length=500)
    # domain_id = models.ForeignKey(DomainMaster, db_column="FK_DomainId", on_delete=models.CASCADE)
    request_type_id = models.IntegerField(db_column="RequestTypeId")
    created_at = models.DateTimeField(db_column='CreatedDatetime', auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = "tbl_RequestInputDetails"


class ScheduleTypeMasterBase(models.Model):
    id = models.IntegerField(db_column='ShedulId', primary_key=True)
    schedtype = models.CharField(db_column='ScheduleType', max_length=20)
    active = models.BooleanField(db_column='Active', default=1)
    createdDt = models.DateTimeField(db_column='CreatedDate')
    modifiedDt = models.DateTimeField(db_column='ModifiedDate')

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_ScheduleTypeMaster'


class ScheduleMasterBase(models.Model):
    id = models.IntegerField(db_column='ScheduleMasterId', primary_key=True)
    startDate = models.DateField(db_column='StartDate', null=False)
    endDate = models.DateField(db_column='EndDate', null=False)
    triggerDay = models.CharField(db_column='TriggerDayDate', null=True, max_length=200)
    time = models.TimeField(db_column='Time', null=False)
    active = models.BooleanField(db_column='Active', null=False, default=1)
    # sm_scheduleType = models.ForeignKey(ScheduleTypeMaster, db_column='SM_ScheduleTypeId', on_delete=False)
    # sm_reqid = models.ForeignKey(RequestMaster, db_column='SM_RequestId', on_delete=False)
    createDt = models.DateTimeField(db_column='CreatedDate', null=False, auto_now_add=True)
    modifiedDt = models.DateTimeField(db_column='ModifiedDate', null=True)
    split = models.IntegerField(db_column='Split', null=True)
    frequency = models.IntegerField(db_column='frequency', null=True)
    day_of_week = models.CharField(db_column='day_of_week', null=True, max_length=200)
    week_of_month = models.IntegerField(db_column='week_of_month', null=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_ScheduleMaster'


class ScheduleDateBase(models.Model):
    scheduleid = models.IntegerField(db_column='ScheduleDatesId', primary_key=True)
    # sd_reqid = models.ForeignKey(RequestMaster, db_column='SD_RequestId', on_delete=models.CASCADE)
    ScheduleDate = models.DateTimeField(db_column='ScheduleDate', null=False)
    ScheduleTime = models.TimeField(db_column='ScheduleTime', null=False)
    Status = models.CharField(db_column='Status', max_length=10)
    CreatedDatetime = models.DateTimeField(db_column='CreatedDatetime', null=False, auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_ScheduleDate'


class CrawlRequestDetailBase(models.Model):
    id = models.PositiveIntegerField(db_column='SubRequestId', primary_key=True)
    # request_id = models.PositiveIntegerField(RequestMaster, db_column='RequestId')
    request_run_id = models.PositiveIntegerField(db_column='RequestRunId')
    request_input_id = models.PositiveIntegerField(db_column='RequestinputdetailId')
    request_url = models.PositiveIntegerField(db_column='RequestUrl')
    start_date = models.DateTimeField(db_column='StartDatetime')
    end_date = models.DateTimeField(db_column='EndDatetime')

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_CrawlRequestDetail'

