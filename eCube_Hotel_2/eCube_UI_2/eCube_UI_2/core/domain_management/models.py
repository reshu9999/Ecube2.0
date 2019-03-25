from django.db import models


class PointOfSaleBase(models.Model):
    # domain = models.ForeignKey(DomainMaster, on_delete=models.CASCADE, related_name='point_of_sales')
    # country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, related_name='point_of_sales')
    bli_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s - %s" % (self.domain.domainname, self.country.countryname)


class CompetitorBase(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    createdDate = models.DateTimeField(auto_now=True)
    updatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{name}".format(name=self.name)
    
    class Meta:
        abstract = True
        managed = False
        db_table = 'tbl_Competitor'


class CompetitorMarketMappingBase(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    # competitor_id = models.ForeignKey(Competitor, db_column='competitor_id', on_delete=models.CASCADE)
    # country_id = models.ForeignKey(CountryMaster, db_column='country_id', on_delete=models.CASCADE)
    active = models.NullBooleanField(db_column="Active",blank=True, null=True)
    createddate = models.DateTimeField(db_column="CreatedDate", auto_now_add=True)
    # user_id = models.ForeignKey(UserMaster, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        abstract = True
        managed = False
        db_table = "tbl_Competitor_Market_Mapping"
