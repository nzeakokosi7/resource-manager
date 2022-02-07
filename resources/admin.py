from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Resource)
admin.site.register(models.ResourceLog)
