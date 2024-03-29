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
from .entity_keywords_model import EntityKeywords
import inspect
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.backends.signals import connection_created
import time
from django.core.mail import send_mail

#SECONDS_PER_REQUEST = 1
SECONDS_PER_REQUEST = 2

error_email_list = []

last_request_time = datetime.datetime.now()
def throttled_request_get(*args, **kwargs):
    global last_request_time
    global error_email_list
    seconds_since_last_request = (datetime.datetime.now() - last_request_time).total_seconds()
    if seconds_since_last_request < SECONDS_PER_REQUEST:
        time.sleep(SECONDS_PER_REQUEST - seconds_since_last_request)
    last_request_time = datetime.datetime.now()
    #try:
    r = requests.get(*args, **kwargs, timeout=None)
    #except requests.exceptions.RequestException as e:
    #    error_email_list.append((str(e), args, kwargs))
    #    r = False
    return r

def error_list_to_str(error_list):
    str_out = ''
    for curr_error in error_list:
        str_tmp = curr_error[0] + '\n' + curr_error[1] + '\n' + curr_error[2] + '\n\n'
        str_out += str_tmp
    return str_out

def import_from_epicollect(ec5_models, only_new_data=False):
    # Rolling back the database does not restore the EC5 media directory,
    # so exception handling is used here to handle the restoration.
    ec5_media_path = os.path.join(settings.MEDIA_ROOT, 'ec5')
    ec5_media_backup_path = os.path.join(settings.MEDIA_ROOT, 'ec5backup')
    try:
        import_from_epicollect_transaction(ec5_models, only_new_data)
    except:
        if not only_new_data:
            if not os.path.exists(ec5_media_backup_path):
                os.mkdir(ec5_media_backup_path)
            all_files = os.listdir(ec5_media_backup_path)
            for curr_file in all_files:
                shutil.move(os.path.join(ec5_media_backup_path,curr_file), os.path.join(ec5_media_path,curr_file))
        raise

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
def import_from_epicollect_transaction(ec5_models, only_new_data):
    global error_email_list
    get_failed = False
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

    token = refresh_ec5_token(settings.EC5_CLIENT_ID, settings.EC5_SECRET_KEY)

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
        ec5_media_backup_path = os.path.join(settings.MEDIA_ROOT, 'ec5backup')
        if os.path.exists(ec5_media_path):
            if not os.path.exists(ec5_media_backup_path):
                os.mkdir(ec5_media_backup_path)
            all_files = os.listdir(ec5_media_path)
            for curr_file in all_files:
                shutil.move(os.path.join(ec5_media_path,curr_file), os.path.join(ec5_media_backup_path,curr_file))
        # Delete all previously imported data
        root_model.objects.all().delete()

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
            #if not response:
            #    get_failed = True
            #    continue
            response.raise_for_status()
            response_json = response.json()
            all_entries += response_json['data']['entries']
            total_pages = response_json['meta']['last_page']
            page += 1
        for entry in all_entries:
            values = {}
            file_values = {}
            for key, value in entry.items():
                if re.match(r"\d+_.*", key) and format_name(key) not in ec5_model_dict:
                    if isinstance(model._meta.get_field(format_name(key)), models.FileField):
                        if value == '':
                            # skip missing values
                            continue
                        elif value.lower().endswith('.jpg'):
                            params = {
                                'type': 'photo',
                                'format': 'entry_original',
                                'name': value
                            }
                        elif value.lower().endswith('.mp4'):
                            params = {
                                'type': 'video',
                                'format': 'video',
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

                        #if not response:
                        #    get_failed = True
                        #    continue
                        # temp logging for files
                        #with open('/tmp/import_file.log','w') as import_file_out:
                        #    for file_key,file_value in file_values.items():
                        #        import_file_out.write('{0}: {1}\n'.format(file_key, file_value))
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

    # email errors if any throttled_request_get failed
    #if get_failed:
    #    send_mail('WAB-NET-Website sync failed',
    #              error_list_to_str(error_email_list),
    #              'young@ecohealthalliance.org',
    #              ['young@ecohealthalliance.org'],
    #              fail_silently=False)

    # Create group for each Country
    for site in ec5_models.SiteData.objects.all():
        if site.country:
            new_group, created = Group.objects.get_or_create(name="View " + site.country)
    Group.objects.get_or_create(name="View all countries")
    return objects_created
