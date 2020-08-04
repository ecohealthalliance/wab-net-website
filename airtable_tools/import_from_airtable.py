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
import urllib.request

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

    token = settings.AIRTABLE_API_KEY

#    all_screening_records = airtable_models.Georgia_screening.objects.all()
#    all_screening_records.delete()
#    all_barcoding_records = airtable_models.Georgia_barcoding.objects.all()
#    all_barcoding_records.delete()
#    return

    ###  FIX: backup procedure will have to be changed
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

    ###  Process:
    ###  1) get barcoding data from airtable
    ###  2) get all associated screening data (could be a list of tables)
    ###  3) create screening record in django for each screening record from airtable
    ###  4) create barcoding record in django for barcoding record from airtable
    ###  5) repeat with next barcoding record from airtable

    N_records = 100
    url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/Host%20DNA%20Barcoding%20Data?maxRecords={0}&view=Grid%20view'.format(N_records)
    logger.info(url)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'Bearer {}'.format(token)}
    r_barcode = requests.get(url, headers=headers)
    logger.info(r_barcode)
    if r_barcode.status_code != 200:
        raise ValueError('Error: got return code {0} for AirTable barcoding read'.format(r_barcode.status_code))
    json_response_barcode = r_barcode.json()
    logger.info(json_response_barcode)

    for idx_records in range(N_records):
        logger.info('****  {}  ****'.format(idx_records))
        logger.info('')

        logger.info('****  reading in barcoding data   ****')
        animal_id = json_response_barcode['records'][idx_records]['fields']['Unique ANIMAL ID']
        logger.info(animal_id)
        cov_screening_data_id = json_response_barcode['records'][idx_records]['fields']['CoV Screening Data']
        logger.info(cov_screening_data_id)

        barcoding_field_dict = {}
        for field in json_response_barcode['records'][idx_records]['fields']:
            short_var_name = airtable_models.Georgia_barcoding.get_name_from_verbose(field)
            barcoding_field_dict[short_var_name] = json_response_barcode['records'][idx_records]['fields'][field]


        #airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable')
        logger.info('****  reading in screening data   ****')
        # FIX: screening id is a list!! must be able associate many screening tables with barcode table
        url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/CoV%20Screening%20Data/{}'.format(cov_screening_data_id[0])
        r_screening = requests.get(url, headers=headers)
        logger.info(r_screening)
        if r_screening.status_code != 200:
            raise ValueError('Error: got return code {0} for AirTable read of {1}'.format(r_screening.status_code, cov_screening_data_id[0]))

        json_response_screening = r_screening.json()
        logger.info(json_response_screening)
        screening_field_dict = {}
        for field in json_response_screening['fields']:
            short_var_name = airtable_models.Georgia_screening.get_name_from_verbose(field)
            # FIX: validation: we want to check the two inputs of animal name to make sure
            #      they're the same
            if short_var_name == 'None':
                logger.info('*** Error: got \'None\' for short_var_name = {0}  {1}'.format(short_var_name, field))
            else:
                screening_field_dict[short_var_name] = json_response_screening['fields'][field]
        for key,val in screening_field_dict.items():
            logger.info('{0}: {1}'.format(key, val))


        screening_keys = screening_field_dict.keys()
        logger.info('creating screening record with animal_id = {}'.format(screening_field_dict['animal_id']))
        airtable_models.Georgia_screening.objects.create(
            animal_id = '{}'.format(screening_field_dict['animal_id'])
        )

        logger.info('** curr screening animal_id = {}'.format(screening_field_dict['animal_id']))
        curr_record = airtable_models.Georgia_screening.objects.get(animal_id='{}'.format(screening_field_dict['animal_id']))
        logger.info(dir(curr_record))

        airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable_georgia/')
        for curr_key in screening_keys:
            array_field_list = ['gel_photo_labeled', 'raw_cov_sequence_txt',
                                'aligned_cov_seuqence_submitted_to_blast',
                                'screenshot_top_5_BLAST_matches',
                                'raw_cov_sequence_ab1', 'raw_cov_sequence_pdf']
            if curr_key in array_field_list:
                # FIX: this is a list of dictionaries!!!
                # FIX: should append timestamp to filename
                # FIX: need to get thumbnails for images if available
                for idx_file_list in range(len(screening_field_dict[curr_key])):
                    targ_url = screening_field_dict[curr_key][idx_file_list]['url']
                    targ_filename = screening_field_dict[curr_key][idx_file_list]['filename']
                    logger.info('*** aligned cov blast url: {} ***'.format(targ_url))
                    urllib.request.urlretrieve(targ_url, airtable_media_path + targ_filename)
                    setattr(curr_record, curr_key, screening_field_dict[curr_key][idx_file_list])
            elif curr_key != 'animal_id':
                logger.info('updating screening key {}'.format(curr_key))
                setattr(curr_record, curr_key, screening_field_dict[curr_key])

        for field in screening_keys:
            logger.info('screening field {0}: {1}'.format(field, getattr(curr_record, field)))

        instance = airtable_models.Georgia_screening.objects.all()
        logger.info(dir(instance))

        # Now create the barcoding table
        current_animal_id = barcoding_field_dict['animal_id']
        airtable_models.Georgia_barcoding.objects.create(
            animal_id='{}'.format(current_animal_id),
            cov_screening_data=airtable_models.Georgia_screening.objects.get(animal_id='{}'.format(current_animal_id))
        )

        curr_record = airtable_models.Georgia_barcoding.objects.get(animal_id='{}'.format(barcoding_field_dict['animal_id']))

        barcoding_keys = barcoding_field_dict.keys()

        for curr_key in barcoding_keys:
            if curr_key != 'animal_id' and curr_key != 'cov_screening_data':
                logger.info('updating screening key {}'.format(curr_key))
                setattr(curr_record, curr_key, barcoding_field_dict[curr_key])

        for field in barcoding_keys:
            if field == 'gel_photo_labeled':
                logger.info('******  we got a gel photo file!  ******')
            logger.info('barcoding field {0}: {1}'.format(field, getattr(curr_record, field)))

        instance = airtable_models.Georgia_barcoding.objects.all()
        logger.info(dir(instance))

        # test saving and deleting a record
        logger.info('*** test save/delete ***')

        logger.info('*** end test save/delete ***')
