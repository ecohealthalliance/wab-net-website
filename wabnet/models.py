from django.db import models
from django.contrib.auth.models import User
from .ec5_models import *
import datetime

class SecondaryData(models.Model):
    name = "Secondary Data Attachments"
    parent = models.ForeignKey(BatData, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='secondary/', verbose_name='File Attachment')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

class EpiCollectImport(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    success = models.BooleanField(default=False)
    import_type = models.CharField(max_length=50)
