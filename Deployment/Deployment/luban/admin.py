from django.contrib import admin
from luban import models


# Register your models here.

admin.site.register(models.AdminInfo)
admin.site.register(models.Business)
admin.site.register(models.Server)
admin.site.register(models.UserProfile)
admin.site.register(models.ServType)
admin.site.register(models.Tools)
admin.site.register(models.CodesDB)
admin.site.register(models.SqlDB)