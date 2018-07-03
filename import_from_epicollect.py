import requests
import sys
import os
import django
from django.core.files.base import ContentFile
from django.db import models
import re
from wabnet.utils import format_name

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wabnet.settings'
django.setup()

import inspect
import wabnet.ec5_models as ec5_models
ec5_model_dict = {}
root_model = None
for name, obj in inspect.getmembers(ec5_models):
    if inspect.isclass(obj):
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
        

# Delete all previously imported data
obj.objects.all().delete()

def import_from_epicollect():
    response = requests.post('https://five.epicollect.net/api/oauth/token', data={
      'grant_type': 'client_credentials',
      'client_id': 364,
      'client_secret': '3dJRqIwr9t8l9wlrbR3MENKEtlCO2c7WeJIy3K6A'
    })
    
    token = response.json()
    for name, model in sorted_model_items:
        params  = {}
        if model.ec5_is_branch:
            params['branch_ref'] = model.ec5_ref
        else:
            params['form_ref'] = model.ec5_ref
        response = requests.get('https://five.epicollect.net/api/export/entries/' + ec5_models.project_name,
            params=params,
            headers={
                'Authorization': 'Bearer ' + token['access_token']
            })
        # if model.ec5_is_branch:
        #     print(str(response.json()).encode('ascii', 'replace'))
        for entry in response.json()['data']['entries']:
            values = {}
            file_values = {}
            for key, value in entry.items():
                if not value:
                    continue
                if re.match(r"\d+_.*", key) and format_name(key) not in ec5_model_dict:
                    if isinstance(model._meta.get_field(format_name(key)), models.FileField):
                        response = requests.get('https://five.epicollect.net/api/export/media/' + ec5_models.project_name,
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
            values['created_at'] = entry['created_at']
            values['created_by'] = entry['created_by']
            values['title'] = entry['title']
            if 'ec5_uuid' in entry:
                values['uuid'] = entry['ec5_uuid']
            if 'ec5_branch_owner_uuid' in entry:
                values['parent'] = model.parent.field.related_model(entry['ec5_branch_owner_uuid'])
            model_instance = model(**values)
            for field_name, file_data in file_values.items():
                getattr(model_instance, field_name).save(*file_data, save=False)
            model_instance.save()

import_from_epicollect()
