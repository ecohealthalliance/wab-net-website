import hashlib
import requests
import sys
import os
import shutil
import django
import datetime
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.db import models
import re
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

def is_list_json_files(test_obj):
    # test_obj must be list of json objects and must have key 'filename' to pass
    if isinstance(test_obj, list):
        for el in test_obj:
            if not isinstance(el, dict):
                return False
            try:
                json_obj = json.loads(json.dumps(el))
                if 'filename' not in json_obj.keys():
                    return False
            except ValueError as e:
                return False
            except TypeError as te:
                return False
    else:
        return False

    return True

def clear_all_airtable(airtable_models):
    # remove all airtable records and associated media files
    all_screening_records = airtable_models.Screening.objects.all()
    all_screening_records.delete()
    all_barcoding_records = airtable_models.Barcoding.objects.all()
    all_barcoding_records.delete()
    all_RawCovSequenceAb1_records = airtable_models.RawCovSequenceAb1.objects.all()
    all_RawCovSequenceAb1_records.delete()

    airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable')
    for filename in os.listdir(airtable_media_path):
        full_path = os.path.join(airtable_media_path, filename)
        os.unlink(full_path)

    return

def import_from_airtable(airtable_models, only_new_data=False):
    # Rolling back the database does not restore the airtable media directory,
    # so exception handling is used here to handle the restoration.
    airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable')
    airtable_media_backup_path = os.path.join(settings.MEDIA_ROOT, 'airtable_backup')
    # move media files to backup dir
    if not only_new_data and os.path.exists(airtable_media_backup_path):
        for mv_fn in os.listdir(airtable_media_path):
            path_from = os.path.join(airtable_media_path, mv_fn)
            path_to = os.path.join(airtable_media_backup_path, mv_fn)
            shutil.move(path_from, path_to)
    # try importing
    try:
        import_from_airtable_transaction(airtable_models, only_new_data)

    except Exception as e:
        # import failed so move backed-up media back
        if not only_new_data and os.path.exists(airtable_media_backup_path):
            for mv_fn in os.listdir(airtable_media_backup_path):
                path_to = os.path.join(airtable_media_path, mv_fn)
                path_from = os.path.join(airtable_media_backup_path, mv_fn)
                shutil.move(path_from, path_to)
        # send email notification of failure
        send_mail('WAB-NET-Website Airtable data import failed',
                  str(e),
                  'young@ecohealthalliance.org',
                  ['young@ecohealthalliance.org'],
                  fail_silently=False)
        raise
    if not only_new_data:
        if os.path.exists(airtable_media_backup_path):
            # import succeeded, so remove backup files
            for rm_fn in os.listdir(airtable_media_backup_path):
                full_rm_path = os.path.join(airtable_media_backup_path, rm_fn)
                os.unlink(full_rm_path)

def get_airtable_batch(json_response_barcode, at_id, page_size, token):
    url = 'https://api.airtable.com/v0/{0}/Host%20DNA%20Barcoding%20Data?view=Grid%20view&pageSize={1}'.format(at_id, page_size)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'Bearer {}'.format(token)}
    if 'offset' in json_response_barcode.keys():
        params = {'offset': '{}'.format(json_response_barcode['offset'])}
        r_barcode = requests.get(url, headers=headers, params=params)
    else:
        r_barcode = requests.get(url, headers=headers)
    if r_barcode.status_code != 200:
        raise ValueError('Error: got return code {0} for AirTable barcoding read'.format(r_barcode.status_code))
    json_response_barcode = r_barcode.json()
    record_batch_size = len(json_response_barcode['records'])

    return (json_response_barcode, record_batch_size, headers)

@transaction.atomic
def import_from_airtable_transaction(airtable_models, only_new_data):

    token = settings.AIRTABLE_API_KEY

    ###  Process:
    ###  1) get barcoding data from airtable
    ###  2) get all associated screening data (could be a list of tables)
    ###  3) create barcoding record in django for barcoding record from airtable
    ###  4) create screening record in django for screening record from airtable
    ###  5) repeat with next barcoding record from airtable

    airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable/')

    page_size = 100   # number of records to be taken in a batch (separated by
                      #   offset) (max = 100)
    airtable_tups = [('appAEhvMc4tSS32ll','Georgia'), ('appVb5vInUwnVTQKQ', 'Jordan')]
    json_response_barcode = {}
    for at_tup in airtable_tups:
        (json_response_barcode, record_batch_size, headers) = get_airtable_batch(json_response_barcode, at_tup[0], page_size, token)

        animal_id_barcoding_list = []
        animal_id_screening_list = []
        no_screening_data_list = []
        done = False
        while not done:

            for idx_records in range(record_batch_size):
                # read in barcoding data
                animal_id = json_response_barcode['records'][idx_records]['fields']['ANIMAL ID']
                # make sure animal_id doesn't appear twice in collection of records
                if animal_id in animal_id_barcoding_list:
                    raise ValueError('Error: duplicate animal_id {0} in barcoding import'.format(animal_id))
                else:
                    animal_id_barcoding_list.append(animal_id)

                # save record if animal_id not in collection, skip otherwise
                test_record = airtable_models.Barcoding.objects.filter(animal_id='{}'.format(animal_id)).first()
                if test_record != None:
                    continue

                cov_screening_data_id = json_response_barcode['records'][idx_records]['fields']['CoV Screening Data']

                # collect field names in a dictionary
                barcoding_field_dict = {}
                for field in json_response_barcode['records'][idx_records]['fields']:
                    short_var_name = airtable_models.Barcoding.get_name_from_verbose(field)
                    barcoding_field_dict[short_var_name] = json_response_barcode['records'][idx_records]['fields'][field]

                # create the barcoding entry
                create_return_val = airtable_models.Barcoding.objects.create(
                    animal_id='{}'.format(barcoding_field_dict['animal_id']),
                    cov_screening_data='{}'.format(barcoding_field_dict['cov_screening_data'])
                    country = at_tup[1]
                )

                # get record created above and fill in other available data
                curr_record = airtable_models.Barcoding.objects.get(animal_id='{}'.format(barcoding_field_dict['animal_id']))

                barcode_cov_screening_data = ''
                for curr_key in barcoding_field_dict.keys():
                    if is_list_json_files(barcoding_field_dict[curr_key]):
                        curr_list = []
                        for idx_file_list in range(len(barcoding_field_dict[curr_key])):
                            targ_url = barcoding_field_dict[curr_key][idx_file_list]['url']
                            targ_filename = barcoding_field_dict[curr_key][idx_file_list]['filename']
                            urllib.request.urlretrieve(targ_url, airtable_media_path + targ_filename)
                            if 'thumbnails' in barcoding_field_dict[curr_key][idx_file_list].keys():
                                thumb_url = barcoding_field_dict[curr_key][idx_file_list]['thumbnails']['large']['url']
                                filename_list = targ_filename.split('.')
                                thumb_filename = '.'.join(filename_list[:-1]) + '_thumb.' + filename_list[-1]
                                urllib.request.urlretrieve(thumb_url, airtable_media_path + thumb_filename)
                            curr_list.append(barcoding_field_dict[curr_key][idx_file_list])
                        setattr(curr_record, curr_key, curr_list)
                    elif curr_key != 'animal_id':
                        setattr(curr_record, curr_key, barcoding_field_dict[curr_key])
                    if curr_key == 'cov_screening_data':
                        barcode_cov_screening_data = barcoding_field_dict[curr_key]
                if barcode_cov_screening_data == '':
                    no_screening_data_list.append(barcoding_field_dict['animal_id'])
                    raise ValueError('Error: No associated CoV Screening Data for read of {}'.format(barcoding_field_dict['animal_id']))

                # record won't be created if you don't save
                curr_record.save()

                instance = airtable_models.Barcoding.objects.all()

                # read in screening data
                # screening id is a list, but should never be more than one, so error on multiple
                if len(cov_screening_data_id) > 1:
                    raise ValueError('Error: got multiple screeing records for AirTable read of {}'.format(cov_screening_data_id[0]))

                url = 'https://api.airtable.com/v0/{0}/CoV%20Screening%20Data/{1}'.format(at_tup[0], cov_screening_data_id[0])
                r_screening = requests.get(url, headers=headers)
                if r_screening.status_code != 200:
                    raise ValueError('Error: got return code {0} for AirTable read of {1}'.format(r_screening.status_code, cov_screening_data_id[0]))

                json_response_screening = r_screening.json()
                # make sure screening record ID is the same as that from barcoding record
                if json_response_screening['id'] != barcode_cov_screening_data[0]:
                    raise ValueError('Error: Screening ID does not match Barcoding ID for screening data for read of {}'.format(barcoding_field_dict['animal_id']))

                screening_field_dict = {}
                for field in json_response_screening['fields']:
                    short_var_name = airtable_models.Screening.get_name_from_verbose(field)
                    if short_var_name == 'None':
                        raise ValueError('*** Error: got \'None\' for short_var_name = {0}  {1}'.format(short_var_name, field))
                    else:
                        screening_field_dict[short_var_name] = json_response_screening['fields'][field]
                        if short_var_name == 'animal_id':
                            if screening_field_dict['animal_id'] in animal_id_screening_list:
                                raise ValueError('Error: duplicate animal_id {0} in screening import!'.format(screeing_field_dict['animal_id']))
                            else:
                                animal_id_screening_list.append(screening_field_dict['animal_id'])

                ## check screening record before trying to make record in django database
                if airtable_models.Barcoding.objects.filter(animal_id='{}'.format(screening_field_dict['animal_id'])).count() == 0:
                    raise ValueError("Error: didn't find associated screening record for animal_id = {}".format(screening_field_dict['animal_id']))
                elif airtable_models.Barcoding.objects.filter(animal_id='{}'.format(screening_field_dict['animal_id'])).count() > 1:
                    raise ValueError("*** Error: got multiple records back for animal_id = {}".format(screening_field_dict['animal_id']))

                # create screening table(s)
                airtable_models.Screening.objects.create(
                    animal_id = '{}'.format(screening_field_dict['animal_id']),
                    barcoding_record=airtable_models.Barcoding.objects.get(animal_id='{}'.format(screening_field_dict['animal_id']))
                )

                curr_record = airtable_models.Screening.objects.get(animal_id='{}'.format(screening_field_dict['animal_id']))

                for curr_key in screening_field_dict.keys():
                    if is_list_json_files(screening_field_dict[curr_key]):
                        curr_list = []
                        for idx_file_list in range(len(screening_field_dict[curr_key])):
                            targ_url = screening_field_dict[curr_key][idx_file_list]['url']
                            targ_filename = screening_field_dict[curr_key][idx_file_list]['filename']
                            urllib.request.urlretrieve(targ_url, airtable_media_path + targ_filename)
                            if 'thumbnails' in screening_field_dict[curr_key][idx_file_list].keys():
                                thumb_url = screening_field_dict[curr_key][idx_file_list]['thumbnails']['large']['url']
                                filename_list = targ_filename.split('.')
                                thumb_filename = '.'.join(filename_list[:-1]) + '_thumb.' + filename_list[-1]
                                urllib.request.urlretrieve(thumb_url, airtable_media_path + thumb_filename)
                            curr_list.append(screening_field_dict[curr_key][idx_file_list])
                            ## create data objects for each file
                            ## Note: abandoned this in the interest of time.
                            ##       left this code as example (open ticket)
                            if curr_key == 'raw_cov_sequence_ab1':
                                airtable_models.RawCovSequenceAb1.objects.create(
                                    airtable_id = '{}'.format(screening_field_dict[curr_key][idx_file_list]['id']),
                                    url = '{}'.format(screening_field_dict[curr_key][idx_file_list]['url']),
                                    filename = '{}'.format(screening_field_dict[curr_key][idx_file_list]['filename']),
                                    size = screening_field_dict[curr_key][idx_file_list]['size'],
                                    type = '{}'.format(screening_field_dict[curr_key][idx_file_list]['type']),
                                    screening_parent=airtable_models.Screening.objects.get(animal_id='{}'.format(screening_field_dict['animal_id'])),
                                    screening_key='{}'.format(curr_key)
                                )
                        setattr(curr_record, curr_key, curr_list)
                    elif curr_key != 'animal_id':
                        setattr(curr_record, curr_key, screening_field_dict[curr_key])
                # record won't be created if you don't save
                curr_record.save()

                instance = airtable_models.Screening.objects.all()

            if 'offset' in json_response_barcode:
                (json_response_barcode, record_batch_size, headers) = get_airtable_batch(json_response_barcode, at_tup[0], page_size, token)
            else:
                done = True

        if len(no_screening_data_list) > 0:
            logger.info('*** list no matching screening records ***')
        for bad_val in no_screening_data_list:
            logger.info('__{}__'.format(bad_val))
