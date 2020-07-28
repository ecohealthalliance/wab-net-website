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
from django.core.exceptions import ObjectDoesNotExist
#from .entity_keywords_model import EntityKeywords
import inspect
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.backends.signals import connection_created
import time
import requests
import json

import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('./log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


#SECONDS_PER_REQUEST = 1
SECONDS_PER_REQUEST = 2

logger.info('*** import_from_airtable ***')

last_request_time = datetime.datetime.now()
def throttled_request_get(*args, **kwargs):
    global last_request_time
    seconds_since_last_request = (datetime.datetime.now() - last_request_time).total_seconds()
    if seconds_since_last_request < SECONDS_PER_REQUEST:
        time.sleep(SECONDS_PER_REQUEST - seconds_since_last_request)
    last_request_time = datetime.datetime.now()
    return requests.get(*args, **kwargs)

def import_from_airtable(airtable_models, only_new_data=False):
    # Rolling back the database does not restore the EC5 media directory,
    # so exception handling is used here to handle the restoration.
    airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable')
    airtable_media_backup_path = os.path.join(settings.MEDIA_ROOT, 'airtable_backup')
    try:
        import_from_airtable_transaction(airtable_models, only_new_data)
    except:
        if not only_new_data and os.path.exists(airtable_media_backup_path):
            shutil.move(airtable_media_backup_path, airtable_media_path)
        raise
    if not only_new_data:
        if os.path.exists(airtable_media_backup_path):
            shutil.rmtree(airtable_media_backup_path)

def refresh_ec5_token(ec5_client_id, ec5_secret_key, current_token = None):
    # If we have no token, gives us a new token.
    # If we have a token that's near expiration, give us a new one.
    # Otherwise, keep the same token.
    if current_token is not None and current_token["expiration_time"] > datetime.datetime.now():
            return current_token
    response = requests.post('https://five.epicollect.net/api/oauth/token', data={
      'grant_type': 'client_credentials',
      'client_id': ec5_client_id,
      'client_secret': ec5_secret_key
    })
    response.raise_for_status()
    token = response.json()
    token["expiration_time"] = datetime.datetime.now() + datetime.timedelta(seconds = token["expires_in"] - 100)
    return(token)

@transaction.atomic
def import_from_airtable_transaction(airtable_models, only_new_data):
    # read models into directory(key=name, value=object)
    airtable_model_dict = {}
    root_model = None
    for name, obj in inspect.getmembers(airtable_models):
        if inspect.isclass(obj) and issubclass(obj, models.Model):
            airtable_model_dict[name] = obj
            if not hasattr(obj, 'cov_screening_data'):
                root_model = obj

    # collapse directory into list and sort with root at index 0
    sorted_model_items = []
    unresolved_models = list(airtable_model_dict.items())
    for model_item in unresolved_models:
        if model_item[1] == root_model:
            sorted_model_items.insert(0, model_item)
        else:
            sorted_model_items.append(model_item)

    token = settings.AIRTABLE_API_KEY


    ###  FIX: backup procedure will have to be changed to either work for
    ###       each database
    '''
    if not only_new_data:
        # Disable foreign key constraint checking because deleting the old data
        # will temporarily break referential integrity until it is re-imported.
        def disable_foreign_keys(sender, connection, **kwargs):
            if connection.vendor == 'sqlite':
                cursor = connection.cursor()
                cursor.execute('PRAGMA foreign_keys = OFF;')
        connection_created.connect(disable_foreign_keys)

        # Move EC5 media to backup in preparation for deletion
        # when the transaction succeeds.
        ec5_media_path = os.path.join(settings.MEDIA_ROOT, 'ec5')
        if os.path.exists(ec5_media_path):
            shutil.move(ec5_media_path, os.path.join(settings.MEDIA_ROOT, 'ec5backup'))
        # Delete all previously imported data
        root_model.objects.all().delete()
    '''

    #url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/CoV%20Screening%20Data?maxRecords=1&view=Grid%20view'
    url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/Host%20DNA%20Barcoding%20Data?maxRecords=1&view=Grid%20view'
    logger.info(url)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(url, headers=headers)
    logger.info(r)
    json_response = r.json()
    logger.info(json_response)
    animal_id = json_response['records'][0]['fields']['Unique ANIMAL ID']
    logger.info(animal_id)
    cov_screening_data_id = json_response['records'][0]['fields']['CoV Screening Data']
    logger.info(cov_screening_data_id)
    # get associated CoV Screening Data record
    url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/CoV%20Screening%20Data/{}'.format(cov_screening_data_id)
    r_screening = requests.get(url, headers=headers)
    json_response_screening = r.json()
    logger.info(json_response_screening)

    '''
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
        page = 1
        total_pages = 1
        all_entries = []
        while page <= total_pages:
            params['page'] = page
            token = refresh_ec5_token(settings.EC5_CLIENT_ID, settings.EC5_SECRET_KEY, token)
            response = throttled_request_get('https://five.epicollect.net/api/export/entries/' + settings.EC5_PROJECT_NAME,
                params=params,
                headers={
                    'Authorization': 'Bearer ' + token['access_token']
                })
            response.raise_for_status()
            response_json = response.json()
            all_entries += response_json['data']['entries']
            total_pages = response_json['meta']['last_page']
            page += 1
        for entry in all_entries:
            values = {}
            file_values = {}
            for key, value in entry.items():
                if not value:
                    continue
                if re.match(r"\d+_.*", key) and format_name(key) not in ec5_model_dict:
                    if isinstance(model._meta.get_field(format_name(key)), models.FileField):
                        if value.endswith('.jpg'):
                            params = {
                                'type': 'photo',
                                'format': 'entry_original',
                                'name': value
                            }
                        else:
                            params = {
                                'type': 'audio',
                                'format': 'audio',
                                'name': value
                            }
                        token = refresh_ec5_token(settings.EC5_CLIENT_ID, settings.EC5_SECRET_KEY, token)
                        response = throttled_request_get('https://five.epicollect.net/api/export/media/' + settings.EC5_PROJECT_NAME,
                            params=params,
                            headers={
                                'Authorization': 'Bearer ' + token['access_token']
                            })
                        response.raise_for_status()
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
            parent_id = entry.get('ec5_branch_owner_uuid', entry.get('ec5_parent_uuid'))
            if parent_id:
                values['parent'] = model.parent.field.related_model.objects.get(pk=parent_id)
            model_instance = model(**values)
            for field_name, file_data in file_values.items():
                getattr(model_instance, field_name).save(*file_data, save=False)
            try:
                model_instance.save()
            except:
                print(values)
                raise
            objects_created += 1
            EntityKeywords(content_object=model_instance, keywords=keywords).save()

    # Create group for each Country
    for site in ec5_models.SiteData.objects.all():
        if site.country:
            new_group, created = Group.objects.get_or_create(name="View " + site.country)
    Group.objects.get_or_create(name="View all countries")
    return objects_created
    '''
