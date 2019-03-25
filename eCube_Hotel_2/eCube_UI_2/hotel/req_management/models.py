from django.db import models

from eCube_UI_2.core.UserManagement.models import (UserMasterBase, RoleMasterBase, BliMasterBase, BliUserMapBase,
                                                   MenuMasterBase, AccessItemMasterBase, RoleAccessItemDetailsBase,
                                                   UserMenuAccessMappingBase, RoleAccessMappingBase,
                                                   UserAttributeConsumptionBase, DomainTypeMasterBase)

from eCube_UI_2.core.domain_management.models import (PointOfSaleBase, CompetitorBase, CompetitorMarketMappingBase)

from eCube_UI_2.core.Add_Request.models import (DomainMasterBase, RequestModeBase, CountryMasterBase, FieldGroupMasterBase)


class RoleMaster(RoleMasterBase):
    pass


class UserMaster(UserMasterBase):

    # DomainTypeID = models.ForeignKey(DomainTypeMaster, models.DO_NOTHING, db_column='DomainTypeId', blank=True, null=True)  # Field name made lowercase.
    RoleID = models.OneToOneField(RoleMaster, db_column='UM_RoleId', on_delete=models.CASCADE)

    @property
    def verbose_name(self):
        return '%s "%s" %s' % (self.FirstName, self.UserName, self.LastName)


class DomainTypeMaster(DomainTypeMasterBase):
    pass


class CountryMaster(CountryMasterBase):
    code = models.CharField(db_column='CountryCode', max_length=100)
    # created_by = models.PositiveIntegerField(db_column='CreatedBy', default=69)
    # created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    # modified_by = models.PositiveIntegerField(db_column='ModifiedBy', default=69)
    # modified_date = models.DateTimeField(db_column='ModifiedDatetime', auto_now=True)
    timezone = models.CharField(db_column='TimeZone', max_length=35)

    class Meta:
        managed = False
        db_table = 'tbl_CountryMaster'

    def __str__(self):
        return '%s: %s' % (self.code, self.name)

    @property
    def active(self):
        return bool(self._active)


class DomainMaster(DomainMasterBase):
    country_id = models.ForeignKey(CountryMaster, db_column='FK_CountryId', on_delete=models.CASCADE)


class BliMaster(BliMasterBase):
    DomainTypeID = models.ForeignKey(DomainTypeMaster, on_delete=models.DO_NOTHING, db_column='DomainTypeId', blank=True, null=True)  # Field name made lowercase.


class BliUserMap(BliUserMapBase):
    pass


class MenuMaster(MenuMasterBase):
    pass


class AccessItemMaster(AccessItemMasterBase):
    menu_id = models.ForeignKey(MenuMaster,db_column='MenuId', on_delete=models.CASCADE)


class RoleAccessItemDetails(RoleAccessItemDetailsBase):
    role_id = models.ForeignKey(RoleMaster,db_column='Role_Id', on_delete=models.CASCADE)
    accessitem_id = models.ForeignKey(AccessItemMaster, db_column='AccessItem_Id', on_delete=models.CASCADE)


class UserMenuAccessMapping(UserMenuAccessMappingBase):
    menu_id = models.ForeignKey(MenuMaster,db_column='Menu_Id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserMaster,db_column='User_Id', on_delete=models.CASCADE)
    accessitem_id = models.ForeignKey(AccessItemMaster,db_column='AccessItem_Id', on_delete=models.CASCADE)


class RoleAccessMapping(RoleAccessMappingBase):
    roleaccessid = models.OneToOneField(RoleMaster, db_column="Roles_Access_Id", on_delete=models.CASCADE, related_name='main_roles_access')
    role_id = models.ForeignKey(RoleMaster, db_column="Roles_Id", on_delete=models.CASCADE, related_name='main_roles')


class UserAttributeConsumption(UserAttributeConsumptionBase):
    user_menu = models.ForeignKey(UserMenuAccessMapping, on_delete=models.DO_NOTHING, related_name='consumption_logs')


class PointOfSale(PointOfSaleBase):
    domain = models.ForeignKey(DomainMaster, on_delete=models.CASCADE, related_name='point_of_sales')
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, related_name='point_of_sales')


class Competitor(CompetitorBase):
    id = models.AutoField(db_column='Id', primary_key=True)
    # countries = models.ForeignKey(CountryMaster, db_column='Fk_CountryId', on_delete=models.DO_NOTHING)


class CompetitorMarketMapping(CompetitorMarketMappingBase):
    competitor_id = models.ForeignKey(Competitor, db_column='competitor_id', on_delete=models.CASCADE)
    country_id = models.ForeignKey(CountryMaster, db_column='country_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserMaster, db_column='user_id', on_delete=models.CASCADE)

