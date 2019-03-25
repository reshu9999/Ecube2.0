from django.db import models

# Create your models here.

class Notifications(models.Model):
    id = models.AutoField(db_column="id",primary_key=True)
    title = models.CharField(db_column='title',max_length=200,blank=True)
    descriptions = models.CharField(db_column='descriptions',max_length=1000,blank=True)
    created_by = models.IntegerField(db_column='created_by',default=10,blank=True)
    created_date = models.DateTimeField(db_column='created_date',blank=True)
    active = models.BooleanField(db_column='active',default=True,max_length=2)
    delete= models.BooleanField(db_column='delete',default=False,max_length=2)
    deleted_by = models.IntegerField(db_column='delete_by',blank=True)
    delete_date =  models.DateTimeField(db_column='delete_date',blank=True)

    class Meta:
        db_table='tbl_notifications'
        managed = False