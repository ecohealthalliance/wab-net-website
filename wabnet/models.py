from django.db import models
from .ec5_models import *

class SecondaryData(models.Model):
    parent = models.ForeignKey(x_field_data_forms_x, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='secondary/', verbose_name='File Attachment')
