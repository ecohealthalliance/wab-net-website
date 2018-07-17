import hashlib
import requests
import sys
import os
import shutil
import django
import datetime
from django.core.files.base import ContentFile
from django.db import models
import re
from .utils import format_name
from django.conf import settings

def import_from_epicollect(ec5_models, only_new_data=False):
    from .entity_keywords_model import EntityKeywords
    import inspect
    ec5_model_dict = {}
    root_model = None
    for name, obj in inspect.getmembers(ec5_models):
        if inspect.isclass(obj) and issubclass(obj, models.Model):
            ec5_model_dict[name] = obj
            if not hasattr(obj, 'parent'):
                root_model = obj

    sorted_model_items = []
    unresolved_models = list(ec5_model_dict.items())
    while len(unresolved_models) > 0:
        for model_item in unresolved_models:
            if model_item[1] == root_model:
                sorted_model_items.insert(0, model_item)
                unresolved_models.remove(model_item)
            elif model_item[1].parent.field.related_model in [model for name, model in sorted_model_items]:
                sorted_model_items.append(model_item)
                unresolved_models.remove(model_item)

    if not only_new_data:
        # Disable foreign key constraint checking because deleting the old data
        # will temporarily break referential integrity until  it is re-imported.
        from django.db.backends.signals import connection_created
        def disable_foreign_keys(sender, connection, **kwargs):
            """Enable integrity constraint with sqlite."""
            if connection.vendor == 'sqlite':
                cursor = connection.cursor()
                cursor.execute('PRAGMA foreign_keys = OFF;')
        connection_created.connect(disable_foreign_keys)
        
        # Delete ec5 media
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'ec5')):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'ec5'))
        # Delete all previously imported data
        root_model.objects.all().delete()

    response = requests.post('https://five.epicollect.net/api/oauth/token', data={
      'grant_type': 'client_credentials',
      'client_id': settings.EC5_CLIENT_ID,
      'client_secret': settings.EC5_SECRET_KEY
    })
    response.raise_for_status()
    token = response.json()
    objects_created = 0
    for model_name, model in sorted_model_items:
        params  = {}
        if model.ec5_is_branch:
            params['branch_ref'] = model.ec5_ref
            params['form_ref'] = model.parent.field.related_model.ec5_ref
        else:
            params['form_ref'] = model.ec5_ref
        if only_new_data:
            if model.objects.count() > 0:
                latest_created_at = model.objects.latest('created_at').created_at
                params['filter_by'] = 'created_at'
                params['filter_from'] = (
                    latest_created_at + datetime.timedelta(seconds=1)
                ).strftime('%Y-%m-%dT%H:%M:%S')
        response = requests.get('https://five.epicollect.net/api/export/entries/' + settings.EC5_PROJECT_NAME,
            params=params,
            headers={
                'Authorization': 'Bearer ' + token['access_token']
            })
        response.raise_for_status()
        for entry in response.json()['data']['entries']:
            values = {}
            file_values = {}
            for key, value in entry.items():
                if not value:
                    continue
                if re.match(r"\d+_.*", key) and format_name(key) not in ec5_model_dict:
                    if isinstance(model._meta.get_field(format_name(key)), models.FileField):
                        response = requests.get('https://five.epicollect.net/api/export/media/' + settings.EC5_PROJECT_NAME,
                            params={
                                'type': 'photo',
                                'format': 'entry_original',
                                'name': value
                            },
                            headers={
                                'Authorization': 'Bearer ' + token['access_token']
                            })
                        file_values[format_name(key)] = (value, ContentFile(response.content),)
                    else:
                        values[format_name(key)] = value
            values['created_at'] = datetime.datetime.strptime(
                entry['created_at'].replace('Z', '-0000'),
                '%Y-%m-%dT%H:%M:%S.%f%z')
            values['created_by'] = entry['created_by']
            values['title'] = entry['title']
            keywords = ' '.join(str(v) for v in values.values())
            if 'ec5_uuid' in entry:
                values['uuid'] = entry['ec5_uuid']
            else:
                idhash = hashlib.sha256()
                if 'ec5_branch_owner_uuid' in entry:
                    idhash.update(entry['ec5_branch_owner_uuid'].encode('ascii', 'replace'))
                idhash.update(entry['title'].encode('ascii', 'replace'))
                idhash.update(entry['created_at'].encode('ascii', 'replace'))
                idhash.update(entry['created_by'].encode('ascii', 'replace'))
                values['id'] = idhash.hexdigest()
            if 'ec5_branch_owner_uuid' in entry:
                values['parent'] = model.parent.field.related_model(entry['ec5_branch_owner_uuid'])
            elif 'ec5_parent_uuid' in entry:
                values['parent'] = model.parent.field.related_model(entry['ec5_parent_uuid'])
            model_instance = model(**values)
            for field_name, file_data in file_values.items():
                getattr(model_instance, field_name).save(*file_data, save=False)
            model_instance.save()
            objects_created += 1
            EntityKeywords(content_object=model_instance, keywords=keywords).save()

    # Create group for each Country
    from django.contrib.auth.models import Group
    for site in ec5_models.SiteData.objects.all():
        if site.country:
            new_group, created = Group.objects.get_or_create(name="View " + site.country)
    Group.objects.get_or_create(name="View all countries")
    return objects_created
