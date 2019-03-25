from django.db import models
from django.utils.crypto import salted_hmac
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    pass


class DomainTypeMasterBase(models.Model):

    id = models.AutoField(db_column='BliId', primary_key=True)
    BliName = models.CharField(db_column='DomainType', max_length=100, blank=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_DomainTypeMaster'


class UserMasterBase(models.Model):
    User_ID = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    FirstName = models.CharField(db_column='FirstName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    LastName = models.CharField(db_column='LastName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    UserName = models.CharField(db_column='UserName', max_length=30, blank=True, null=True, unique=True)  # Field name made lowercase.
    Password = models.CharField(db_column='password', max_length=30, blank=True, null=True)  # Field name made lowercase.
    EmailID = models.CharField(db_column='EmailID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    Active = models.BooleanField(db_column='Active', blank=True)  # Field name made lowercase.
    #DomainTypeID = models.ForeignKey(DomainTypeMaster, models.DO_NOTHING, db_column='DomainTypeId', blank=True,
    #                                 null=True)  # Field name made lowercase.
    # RoleID = models.OneToOneField(RoleMaster,db_column='UM_RoleId' , on_delete=models.CASCADE)
    Role = models.CharField(db_column='Role', max_length=15)  # Field name made lowercase.
    BliID = models.CharField(db_column='UM_BliId', blank=True, max_length=30)  # Field name made lowercase.
    CreatedDate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    last_login = models.DateTimeField(db_column='LastLogin', auto_now_add=True)

    REQUIRED_FIELDS = ['EmailID']
    USERNAME_FIELD = 'UserName'
    EMAIL_FIELD = 'EmailID'

    objects = UserManager()

    class Meta:
        abstract = True
        db_table = 'tbl_UserMaster'

    @property
    def full_name(self):
        return '%s "%s" %s' % (self.FirstName, self.UserName, self.LastName)
    
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.Password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["Password"])
        return check_password(raw_password, self.Password, setter)
    
    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.Password = make_password(None)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.Password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'


class RoleMasterBase(models.Model):
    roleid = models.AutoField(db_column='RoleId', primary_key=True)  # Field name made lowercase.
    rolename = models.CharField(db_column='RoleName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    Active = models.BooleanField(db_column='Active', blank=True)  # Field name made lowercase.
    CreatedDate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    ModifiedDate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_RoleMaster'


class BliMasterBase(models.Model):
    id = models.AutoField(db_column='BliId', primary_key=True)  # Field name made lowercase.
    BliName = models.CharField(db_column='BliName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    business = models.CharField(db_column='businessType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    Active = models.BooleanField(db_column='Active', blank=True)  # Field name made lowercase.
    CreatedDate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    ModifiedDate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    # DomainTypeID = models.ForeignKey(DomainTypeMaster, models.DO_NOTHING, db_column='DomainTypeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_BliMaster'


class BliUserMapBase(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    userid = models.IntegerField(db_column='userID', null=False)
    bliid = models.IntegerField(db_column='bliID', null=False)
    createDt = models.DateTimeField(db_column='createDT', auto_now_add=True, auto_now=False)
    lastupdDt = models.DateTimeField(db_column='lastupdateDT', auto_now_add=True, auto_now=False)
    delflg = models.CharField(db_column='delflg', max_length=1, null=False)

    class Meta:
        abstract = True
        db_table = 'tbl_bliuser_mapping'


class MenuMasterBase(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)
    menuname = models.CharField(db_column='MenuName', max_length=30)
    active = models.BooleanField(db_column="Active")

    class Meta:
        abstract = True
        managed = False
        db_table = "tbl_MenuMaster"


class AccessItemMasterBase(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)
    # menu_id =models.ForeignKey(MenuMaster,db_column='MenuId', on_delete=models.CASCADE)
    accessitems = models.CharField(db_column='AccessItems', max_length =30)
    active = models.BooleanField(db_column='Active', blank=True)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_AccessItemsMaster'


class RoleAccessItemDetailsBase(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    # role_id = models.ForeignKey(RoleMaster,db_column='Role_Id', on_delete=models.CASCADE)
    # accessitem_id = models.ForeignKey(AccessItemsMaster, db_column='AccessItem_Id', on_delete=models.CASCADE)
    # is_access = models.BooleanField(db_column='IsAccess', blank=True)
    defaultvalue = models.CharField(db_column='DefaultValue', max_length=30)
    display = models.BooleanField(db_column='IsDisplay', blank=True)
    active = models.BooleanField(db_column='Active', blank=True)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_RoleAccessItemsDetails'


class UserMenuAccessMappingBase(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)
    # menu_id = models.ForeignKey(MenuMaster,db_column='Menu_Id', on_delete=models.CASCADE)
    # user_id = models.ForeignKey(UserMaster,db_column='User_Id', on_delete=models.CASCADE)
    # accessitem_id = models.ForeignKey(AccessItemsMaster,db_column='AccessItem_Id', on_delete=models.CASCADE)
    accessitems = models.CharField(db_column='accessitems', max_length=30)
    limits = models.IntegerField(db_column='limits')
    permission_type = models.CharField(db_column='permission_type', max_length=30)
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'UserMenuMappings'

    def add_consumption(self, consumption):
        new_consumption_log = self._meta.model(
            user_menu=self,
            consumption=consumption
        )
        new_consumption_log.save()

    @classmethod
    def _consumption(cls, logs):
        return sum(logs.values_list('consumption', flat=True))

    @classmethod
    def _percentage_consumption(cls, logs, limit):
        return int((float(cls._consumption(logs)) / float(limit)) * 100)

    @property
    def _all_logs(self):
        return self.consumption_logs.all()

    @property
    def total_consumption(self):
        return self._consumption(self._all_logs)

    @property
    def total_percentage(self):
        if self.content:
            return self._percentage_consumption(self.total_consumption, self.content)

    @property
    def count_remaining(self):
        if self.content:
            return int(self.content) - int(self.total_consumption)

    @property
    def percentage_remaining(self):
        return float(100) - float(self.total_percentage)

    def reset_consumption(self):
        self._all_logs.delete()


class RoleAccessMappingBase(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)
    # roleaccessid = models.OneToOneField(RoleMaster,db_column="Roles_Access_Id",on_delete=models.CASCADE,related_name='main_roles_access')
    # role_id = models.ForeignKey(RoleMaster, db_column="Roles_Id", on_delete=models.CASCADE, related_name='main_roles')
    active = models.NullBooleanField(db_column="Active",blank=True, null=True)
    createddate = models.DateTimeField(db_column="CreatedDate", auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = "tbl_RolesAccessMapping"


class UserAttributeConsumptionBase(models.Model):
    # user_menu = models.ForeignKey(UserMenuAccessMappings, on_delete=models.CASCADE, related_name='consumption_logs')
    consumption = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_UserMenuConsumptionLog'
