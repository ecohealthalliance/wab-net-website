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

def clear_all_airtable(airtable_models):
    all_screening_records = airtable_models.Screening.objects.all()
    all_screening_records.delete()
    all_barcoding_records = airtable_models.Barcoding.objects.all()
    all_barcoding_records.delete()
    all_RawCovSequenceAb1_records = airtable_models.RawCovSequenceAb1.objects.all()
    all_RawCovSequenceAb1_records.delete()

    #airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable_georgia')
    #for filename in os.listdir(airtable_media_path):
    #    full_path = os.path.join(airtable_media_path, filename)
    #    os.unlink(full_path)

    return

def import_from_airtable(airtable_models, only_new_data=False):
    # Rolling back the database does not restore the EC5 media directory,
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
    except:
        # import failed so move backed-up media back
        if not only_new_data and os.path.exists(airtable_media_backup_path):
            #shutil.move(airtable_media_backup_path, airtable_media_path)
            for mv_fn in os.listdir(airtable_media_backup_path):
                path_to = os.path.join(airtable_media_path, mv_fn)
                path_from = os.path.join(airtable_media_backup_path, mv_fn)
                shutil.move(path_from, path_to)
        raise
    if not only_new_data:
        if os.path.exists(airtable_media_backup_path):
            # import succeeded, so remove backup files
            for rm_fn in os.listdir(airtable_media_backup_path):
                full_rm_path = os.path.join(airtable_media_backup_path, rm_fn)
                os.unlink(full_rm_path)


@transaction.atomic
def import_from_airtable_transaction(airtable_models, only_new_data):

    token = settings.AIRTABLE_API_KEY

    ###  Process:
    ###  1) get barcoding data from airtable
    ###  2) get all associated screening data (could be a list of tables)
    ###  3) create screening record in django for each screening record from airtable
    ###  4) create barcoding record in django for barcoding record from airtable
    ###  5) repeat with next barcoding record from airtable

    airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable/')

    page_size = 100
    #url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/Host%20DNA%20Barcoding%20Data?view=Grid%20view&maxRecords=15&pageSize={}'.format(page_size)
    url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/Host%20DNA%20Barcoding%20Data?view=Grid%20view&pageSize={}'.format(page_size)
    logger.info(url)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'Bearer {}'.format(token)}
    r_barcode = requests.get(url, headers=headers)
    logger.info(r_barcode)
    if r_barcode.status_code != 200:
        raise ValueError('Error: got return code {0} for AirTable barcoding read'.format(r_barcode.status_code))
    json_response_barcode = r_barcode.json()
    logger.info(json_response_barcode)
    if 'offset' in json_response_barcode:
        logger.info(json_response_barcode['offset'])
    logger.info(len(json_response_barcode['records']))
    record_batch_size = len(json_response_barcode['records'])

    bad_screening_list = []
    animal_id_barcoding_list = []
    animal_id_screening_list = []

    done = False
    while not done:

        for idx_records in range(record_batch_size):
            logger.info('****  {}  ****'.format(idx_records))
            logger.info('')

            # read in barcoding data
            logger.info('****  reading in barcoding data   ****')
            animal_id = json_response_barcode['records'][idx_records]['fields']['Unique ANIMAL ID']
            if animal_id in animal_id_barcoding_list:
                raise ValueError('Error: duplicate animal_id {0} in barcoding import'.format(animal_id))
            else:
                animal_id_barcoding_list.append(animal_id)

            logger.info(animal_id)
            cov_screening_data_id = json_response_barcode['records'][idx_records]['fields']['CoV Screening Data']
            logger.info(cov_screening_data_id)

            barcoding_field_dict = {}
            for field in json_response_barcode['records'][idx_records]['fields']:
                short_var_name = airtable_models.Barcoding.get_name_from_verbose(field)
                barcoding_field_dict[short_var_name] = json_response_barcode['records'][idx_records]['fields'][field]

            # Now create the barcoding table
            logger.info('*** creating barcoding record {}'.format(barcoding_field_dict['animal_id']))
            create_return_val = airtable_models.Barcoding.objects.create(
                animal_id='{}'.format(barcoding_field_dict['animal_id']),
                cov_screening_data='{}'.format(barcoding_field_dict['cov_screening_data'])
            )
            logger.info(create_return_val)

            curr_record = airtable_models.Barcoding.objects.get(animal_id='{}'.format(barcoding_field_dict['animal_id']))

            barcoding_keys = barcoding_field_dict.keys()

            for curr_key in barcoding_keys:
                # FIX: this list should be auto populated somewhere, so this
                #      list doesn't need to be maintained
                #      Really, these should all be foreign keys onto new tables
                array_field_list = ['gel_photo_labeled','raw_host_sequence_txt',
                                    'raw_host_sequence_ab1','raw_host_sequence_pdf',
                                    'aligned_host_sequence_submitted_to_blast',
                                    'screenshot_top_5_BLAST_matches']
                if curr_key in array_field_list:
                    # FIX: this is a list of dictionaries!!!
                    # FIX: should append timestamp to filename
                    # FIX: need to get thumbnails for images if available
                    logger.info('*** got barcoding file {} ***'.format(curr_key))
                    for idx_file_list in range(len(barcoding_field_dict[curr_key])):
                        targ_url = barcoding_field_dict[curr_key][idx_file_list]['url']
                        logger.info(targ_url)
                        targ_filename = barcoding_field_dict[curr_key][idx_file_list]['filename']
                        logger.info(targ_filename)
                        urllib.request.urlretrieve(targ_url, airtable_media_path + targ_filename)
                        setattr(curr_record, curr_key, barcoding_field_dict[curr_key][idx_file_list])
                elif curr_key != 'animal_id' and curr_key != 'cov_screening_data':
                    logger.info('updating screening key {}'.format(curr_key))
                    setattr(curr_record, curr_key, barcoding_field_dict[curr_key])
                ## FIX: remove cov_screening_data from elif above!

            for field in barcoding_keys:
                if field == 'gel_photo_labeled':
                    logger.info('******  we got a gel photo file!  ******')
                logger.info('barcoding field {0}: {1}'.format(field, getattr(curr_record, field)))

            instance = airtable_models.Barcoding.objects.all()
            logger.info(dir(instance))


            # read in screening data
            #airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable')
            logger.info('****  reading in screening data   ****')
            # FIX: screening id is a list!! must be able associate many screening tables with barcode table
            #      Actually, after conversation with Kendra, this won't happen so warn or error on multiple
            if len(cov_screening_data_id) > 1:
                ## FIX: this should probably raise and error
                logger.info("*** Error: we got multiple cov_screening_data_ids back ***")


            url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/CoV%20Screening%20Data/{}'.format(cov_screening_data_id[0])
            r_screening = requests.get(url, headers=headers)
            logger.info(r_screening)
            if r_screening.status_code != 200:
                raise ValueError('Error: got return code {0} for AirTable read of {1}'.format(r_screening.status_code, cov_screening_data_id[0]))

            json_response_screening = r_screening.json()
            logger.info(json_response_screening)
            screening_field_dict = {}
            for field in json_response_screening['fields']:
                short_var_name = airtable_models.Screening.get_name_from_verbose(field)
                # FIX: validation: we want to check the two inputs of animal name to make sure
                #      they're the same
                if short_var_name == 'None':
                    logger.info('*** Error: got \'None\' for short_var_name = {0}  {1}'.format(short_var_name, field))
                else:
                    screening_field_dict[short_var_name] = json_response_screening['fields'][field]
                    if short_var_name == 'animal_id':
                        logger.info('*** checking screening animal_id for dups ***')
                        logger.info('test screening animal_id = __{}__'.format(screening_field_dict['animal_id']))
                        if screening_field_dict['animal_id'] in animal_id_screening_list:
                            logger.info('Error: already have animal_id {} in import!!'.format(screening_field_dict['animal_id']))
                            raise ValueError('Error: duplicate animal_id {0} in screening import!'.format(screeing_field_dict['animal_id']))
                        else:
                            logger.info('Animal_id is new so proceeding')
                            animal_id_screening_list.append(screening_field_dict['animal_id'])

            for key,val in screening_field_dict.items():
                logger.info('{0}: {1}'.format(key, val))

            ## check if screening record exists before trying to make record
            if airtable_models.Barcoding.objects.filter(animal_id='{}'.format(screening_field_dict['animal_id'])).count() == 0:
                logger.info("Error: didn't find associated screening record for animal_id = {}".format(screening_field_dict['animal_id']))
                bad_screening_list.append(screening_field_dict['animal_id'])
                continue
            elif airtable_models.Barcoding.objects.filter(animal_id='{}'.format(screening_field_dict['animal_id'])).count() > 1:
                logger.info("*** Error: got multiple records back for animal_id = {}".format(screening_field_dict['animal_id']))
                ## Fix: this should raise an error if we're not going to handle it

            # create screening table(s)
            screening_keys = screening_field_dict.keys()
            logger.info('creating screening record with animal_id = ##{}##'.format(screening_field_dict['animal_id']))
            airtable_models.Screening.objects.create(
                animal_id = '{}'.format(screening_field_dict['animal_id']),
                barcoding_record=airtable_models.Barcoding.objects.get(animal_id='{}'.format(screening_field_dict['animal_id']))
            )

            logger.info('** curr screening animal_id = {}'.format(screening_field_dict['animal_id']))
            curr_record = airtable_models.Screening.objects.get(animal_id='{}'.format(screening_field_dict['animal_id']))
            logger.info(dir(curr_record))

            #airtable_media_path = os.path.join(settings.MEDIA_ROOT, 'airtable_georgia/')
            for curr_key in screening_keys:
                # FIX: this list should be auto populated somewhere, so this
                #      list doesn't need to be maintained
                #      Really, these should all be foreign keys onto new tables
                array_field_list = ['gel_photo_labeled', 'raw_cov_sequence_txt',
                                    'aligned_cov_sequence_submitted_to_blast',
                                    'screenshot_top_5_BLAST_matches',
                                    'raw_cov_sequence_ab1', 'raw_cov_sequence_pdf']
                if curr_key in array_field_list:
                    # FIX: this is a list of dictionaries!!!
                    # FIX: should append timestamp to filename?
                    # FIX: get thumbnails for images if available
                    logger.info('<--->len of screening_field_dict: {}'.format(len(screening_field_dict[curr_key])))
                    curr_list = []
                    for idx_file_list in range(len(screening_field_dict[curr_key])):
                        targ_url = screening_field_dict[curr_key][idx_file_list]['url']
                        targ_filename = screening_field_dict[curr_key][idx_file_list]['filename']
                        logger.info('*** aligned cov blast url: {} ***'.format(targ_url))
                        urllib.request.urlretrieve(targ_url, airtable_media_path + targ_filename)
                        logger.info('****  setattr for {}'.format(curr_key))
                        logger.info(screening_field_dict[curr_key][idx_file_list])
#                        setattr(curr_record, curr_key, screening_field_dict[curr_key][idx_file_list])
                        curr_list.append(screening_field_dict[curr_key][idx_file_list])
                        ## create data objects for each file
                        if curr_key == 'raw_cov_sequence_ab1':
                            airtable_models.RawCovSequenceAb1.objects.create(
                                airtable_id = '{}'.format(screening_field_dict[curr_key][idx_file_list]['id']),
                                url = '{}'.format(screening_field_dict[curr_key][idx_file_list]['url']),
                                filename = '{}'.format(screening_field_dict[curr_key][idx_file_list]['filename']),
                                size = screening_field_dict[curr_key][idx_file_list]['size'],
                                type = '{}'.format(screening_field_dict[curr_key][idx_file_list]['type']),
                                screening_parent=airtable_models.Screening.objects.get(animal_id='{}'.format(screening_field_dict['animal_id']))
                            )
                        setattr(curr_record, curr_key, curr_list)
                elif curr_key != 'animal_id':
                    logger.info('updating screening key {}'.format(curr_key))
                    setattr(curr_record, curr_key, screening_field_dict[curr_key])
            curr_record.save()

            for field in screening_keys:
                logger.info('screening field {0}: {1}'.format(field, getattr(curr_record, field)))

            ## show barcoding records associated with the screening record
            logger.info('*** show screening reports related to this barcoding report')
            logger.info(airtable_models.Screening.objects.filter(barcoding_record__animal_id=screening_field_dict['animal_id']))

            instance = airtable_models.Screening.objects.all()
            logger.info(dir(instance))

        if 'offset' in json_response_barcode:
            logger.info('*** we have an offset so getting another batch ***')
            # you need to be setting a new json_response_barcode here!!!
            url = 'https://api.airtable.com/v0/appAEhvMc4tSS32ll/Host%20DNA%20Barcoding%20Data?view=Grid%20view&pageSize={0}'.format(page_size)
            logger.info(url)
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': 'Bearer {}'.format(token)}
            params = {'offset': '{}'.format(json_response_barcode['offset'])}
            r_barcode = requests.get(url, headers=headers, params=params)
            logger.info(r_barcode)
            if r_barcode.status_code != 200:
                raise ValueError('Error: got return code {0} for AirTable barcoding read'.format(r_barcode.status_code))
            json_response_barcode = r_barcode.json()
            logger.info(json_response_barcode)
            if 'offset' in json_response_barcode:
                logger.info(json_response_barcode['offset'])
            logger.info(len(json_response_barcode['records']))
            record_batch_size = len(json_response_barcode['records'])
        else:
            done = True

    if len(bad_screening_list) > 0:
        logger.info('*** list of missing screening records ***')
    for bad_val in bad_screening_list:
        logger.info('__{}__'.format(bad_val))
