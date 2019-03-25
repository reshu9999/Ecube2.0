from django.contrib import admin

from . import models

admin.site.register(models.DomainTypeMaster)
admin.site.register(models.BliMaster)
admin.site.register(models.RoleMaster)
admin.site.register(models.UserMaster)

