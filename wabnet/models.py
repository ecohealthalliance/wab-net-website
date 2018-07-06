from django.db import models
from .ec5_models import *

class SecondaryData(models.Model):
    name = "Secondary Data Attachments"
    parent = models.ForeignKey(SiteData, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='secondary/', verbose_name='File Attachment')

