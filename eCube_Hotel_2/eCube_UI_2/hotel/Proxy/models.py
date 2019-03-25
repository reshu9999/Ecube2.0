from django.db import models
from .utils import CSVReader
from hotel.master.models import CountryMaster


class ProxyTypeMaster(models.Model):
    id = models.AutoField(db_column='ProxyTypeId', primary_key=True)
    name = models.CharField(db_column='ProxyTypeName', max_length=200)

    class Meta:
        managed = False
        db_table = 'tbl_ProxyTypeMaster'


class ProxyMaster(models.Model):
    id = models.AutoField(db_column='ProxyMasterId', primary_key=True)
    name = models.CharField(db_column='ProxyName', max_length=200)
    port = models.PositiveIntegerField(db_column='ProxyPort')
    username = models.CharField(db_column='ProxyUserName', max_length=200, null=True)
    password = models.CharField(db_column='ProxyPassword', max_length=200, null=True)
    proxy_type = models.ForeignKey(ProxyTypeMaster, db_column="PRM_ProxyTypeId", on_delete=models.CASCADE)
    created_date = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    modified_date = models.DateTimeField(db_column='ModifiedDate', auto_now=True)
    country_id = models.ForeignKey(CountryMaster, db_column="CountryId", related_name='proxy_country', on_delete=models.CASCADE, null=True)
    region_id = models.PositiveIntegerField(db_column='RegionId')
    vendor_name = models.CharField(db_column='Vendor_Name', max_length=500)
    pos_id = models.ForeignKey(CountryMaster, db_column="POS", related_name='proxy_pos', on_delete=models.CASCADE, null=True)
    page_type = models.CharField(db_column='PageType', max_length=200, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_ProxyMaster'

    @classmethod
    def upload_csv(cls, file_path):
        csv_file = CSVReader(file_path)

        csv_db_key_map = lambda x: {
            'country_id': CountryMaster.objects.get(name=csv_file.get_value('CountryName', x)) if csv_file.get_value('CountryName', x) else None,
            'name': csv_file.get_value('ProxyName', x),
            'password': csv_file.get_value('ProxyPassword', x),
            'port': csv_file.get_value('ProxyPort', x),
            'proxy_type': ProxyTypeMaster.objects.get(name=csv_file.get_value('ProxyType', x)),
            'region_id': csv_file.get_value('RegionId', x),
            'username': csv_file.get_value('ProxyUserName', x),
            'vendor_name': csv_file.get_value('VendorName', x),
            'pos_id': CountryMaster.objects.get(name=csv_file.get_value('POS', x)) if csv_file.get_value('POS', x) else None,
            'page_type': csv_file.get_value('PageType', x),
        }

        data_kwargs = list()
        unique_vendors = list()
        proxyName = list()
        if len(csv_file.csv_data) == 0:
            return list()
        else:
            for data in csv_file.csv_data:
                # cls(**{db_key: csv_file.get_value(header, data) for db_key, header in csv_db_key_map.items()}).save()
                print("csv_db_key_map(data)")
                print(data)
                print(csv_db_key_map(data))
                if cls.objects.filter(name=csv_db_key_map(data)['name'],vendor_name=csv_db_key_map(data)['vendor_name'], port=csv_db_key_map(data)['port'], pos_id=csv_db_key_map(data)['pos_id']).exists():
                    cls.objects.filter(name=csv_db_key_map(data)['name'],vendor_name=csv_db_key_map(data)['vendor_name'], port=csv_db_key_map(data)['port'], pos_id=csv_db_key_map(data)['pos_id']).update(**csv_db_key_map(data))
                    #pass
                else:
                    data_kwargs.append(csv_db_key_map(data))

                if not csv_db_key_map(data)['vendor_name'] in unique_vendors:
                    unique_vendors.append(csv_db_key_map(data)['vendor_name'])

                if not csv_db_key_map(data)['name'] in proxyName:
                    proxyName.append(csv_db_key_map(data)['name'])

            cls.objects.bulk_create([cls(**kwargs) for kwargs in data_kwargs])
        return unique_vendors , proxyName
# Create your models here.
