import pytz
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta


# Create your models here.
class Resource(models.Model):
    file = models.FileField(blank=True, null=True, upload_to=".")
    link = models.URLField(max_length=128, blank=True, null=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=128, blank=True, default="0")
    time_stamp = models.CharField(max_length=128, default="0")
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        now = datetime.now()
        now = pytz.utc.localize(now)
        return self.date_created < now - timedelta(days=1)


class ResourceLog(models.Model):
    datetime = models.CharField(max_length=20)
    files = models.IntegerField(default=0)
    links = models.IntegerField(default=0)
