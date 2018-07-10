from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class EntityKeywords(models.Model):
    keywords = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.TextField()
    content_object = GenericForeignKey('content_type', 'object_id')
