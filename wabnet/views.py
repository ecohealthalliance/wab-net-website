import datetime
import json
import re
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import django.forms as forms
from django.db import models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django_tables2 import RequestConfig
import django_tables2
from .models import SiteData, BatData, SecondaryData, TrappingEvent
from ec5_tools.entity_keywords_model import EntityKeywords
from .tables import SiteTable, BatTable, SecondaryDataTable
import inspect
from . import ec5_models
from . import airtable_models
import types
from django.forms.models import model_to_dict
import os

import logging


logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('./log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


child_models = {}
for name, obj in inspect.getmembers(ec5_models):
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        if hasattr(obj, 'parent'):
            child_models[name] = obj

airtable_download_models = {}
for name, obj in inspect.getmembers(airtable_models):
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        if name == 'Barcoding' or name == 'Screening':
            airtable_download_models[name] = obj

bat_family_fields = [field
    for field in BatData._meta.get_fields()
    if isinstance(field, models.TextField) and field.verbose_name.startswith("Family:")]

def get_bat_species(bat_data):
    bat_species = None
    bat_family = None
    for field in bat_data._meta.get_fields():
        if field.name.endswith('_Bat_family_x'):
            bat_family = getattr(bat_data, field.name)
    for field in bat_family_fields:
        if bat_family in field.verbose_name:
            bat_species = getattr(bat_data, field.name)
            break
    return bat_family, bat_species

class SecondaryDataForm(forms.ModelForm):
    class Meta:
        model = SecondaryData
        fields = ['file']

class SiteDataForm(forms.ModelForm):
    class Meta:
        model = SiteData
        exclude = ['title', 'uuid', 'created_at', 'created_by', 'country']

class TrappingEventForm(forms.ModelForm):
    class Meta:
        model = TrappingEvent
        exclude = ['title', 'uuid', 'parent']


def get_site_attr(site_data, attr_base_name):

    valid_attr_list = ['Site_location_GPS']

    if attr_base_name not in valid_attr_list:
        raise ValueError('views.py: get_bat_attr(): {} not supported'.format(attr_base_name))

    # find the correct attribute name for list elements
    found_targ_attr = False
    targ_attr = ''
    attr_source = site_data
    for curr_attr in dir(attr_source):
        if attr_base_name in curr_attr:
            if found_targ_attr:
                raise ValueError('views.py: get_site_attr(): found duplicate base attributes!')
            else:
                found_targ_attr = True
                targ_attr = curr_attr

    if not found_targ_attr:
        raise ValueError('views.py: get_bat_attr(): base_attr_name not found')

    return getattr(attr_source, targ_attr)


@login_required(login_url='/about')
def splash(request):
    from django.core import serializers
    all_countries = False
    user_viewable_countries = set([
        group.name.replace('View ', '') for group in request.user.groups.all()])
    if 'all countries' in user_viewable_countries:
        all_countries = True
    sites = []
    for site_data in SiteData.objects.all():
        if all_countries or site_data.country in user_viewable_countries:
            coords = json.loads(str(get_site_attr(site_data, 'Site_location_GPS')).replace("'", '"'))
            sites.append({
                'id': site_data.uuid,
                'country': site_data.country,
                'title': site_data.title,
                'coords': [coords['latitude'], coords['longitude']],
                'accessible': all_countries or site_data.country in user_viewable_countries,
            })
    samples_by_species = {}
    for bat_data in BatData.objects.all():
        bat_family, bat_species = get_bat_species(bat_data)
        samples_by_species[bat_species] = samples_by_species.get(bat_species, 0) + 1
    samples_by_species_list = [(k,v) for k,v in samples_by_species.items()]
    samples_by_species = sorted(samples_by_species_list)
    return render(request, 'splash.html', {
        'locations_json': json.dumps(sites),
        'samples_by_species': samples_by_species
    })

def about(request):
    return render(request, 'about.html')

@login_required
def site_table(request):
    user_viewable_countries = [
        group.name.replace('View ', '') for group in request.user.groups.all()]
    if 'all countries' in user_viewable_countries:
        sites = SiteData.objects.all()
    else:
        sites = SiteData.objects.filter(
            country__in=user_viewable_countries)
    table = SiteTable(sites)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'site_table.html', {'table': table})

def raise_if_user_cannot_access_site(user, site_id):
    user_viewable_countries = [
        group.name.replace('View ', '') for group in user.groups.all()]
    if 'all countries' in user_viewable_countries:
        return
    else:
        sites = SiteData.objects.filter(
            country__in=user_viewable_countries, uuid=site_id)
        if len(sites) == 0:
            raise PermissionDenied

@login_required
def site_view(request, site_id):
    raise_if_user_cannot_access_site(request.user, site_id)
    site_data = SiteData.objects.get(uuid=site_id)
    tables = []
    for model_name, child_model in child_models.items():
        if child_model.parent.field.related_model != SiteData:
            continue
        class MyTable(django_tables2.Table):
            name = child_model.name
            class Meta:
                model = child_model
                exclude = ('id', 'uuid', 'parent',)
                sequence = ('title', '...')
        objects = child_model.objects.filter(parent=site_id)
        table = MyTable(objects)
        RequestConfig(request).configure(table)
        tables.append(table)
    objects = BatData.objects.filter(parent__parent=site_id)
    table = BatTable(objects)
    RequestConfig(request).configure(table)
    tables.append(table)
    site_data_dict = make_verbose_dict(site_data)

    return render(request, 'site.html', {
        'form': SiteDataForm(instance=site_data),
        'site_data': site_data,
        'site_data_dict': format_dict_data(site_data_dict, 'site'),
        'tables': tables})

@login_required
def attach_data(request, bat_id):
    if request.method == 'POST':
        form = SecondaryDataForm(request.POST, request.FILES)
        if form.is_valid():
            secondary_data = form.save(commit=False)
            secondary_data.parent = BatData.objects.get(uuid=bat_id)
            secondary_data.created_by = request.user
            secondary_data.created_at = datetime.datetime.now()
            secondary_data.save()
            return HttpResponseRedirect('/bats/' + bat_id)
        else:
            return render(request, 'attach.html', {'form': form})
    secondary_data = SecondaryData(parent=BatData.objects.get(uuid=bat_id))
    return render(request, 'attach.html', {'form': SecondaryDataForm(instance=secondary_data)})

from django_tables2.export.export import TableExport
import zipfile
from six import BytesIO
@login_required
def download_all_data(request):
    try:
        user_viewable_countries = [
            group.name.replace('View ', '') for group in request.user.groups.all()]
        zip_buffer = BytesIO()
        zipf = zipfile.ZipFile(zip_buffer, 'a')
        for model_name, child_model in list(child_models.items()) + [
            ('SiteData', SiteData),
            ('SecondaryData', SecondaryData)] + list(airtable_download_models.items()):
            class MyTable(django_tables2.Table):
                if model_name == 'Barcoding' or model_name == 'Screening':
                    name = model_name
                else:
                    name = child_model.name
                class Meta:
                    model = child_model
                    template_name = 'django_tables2/bootstrap.html'
                    exclude = ('id', 'uuid', 'parent',)
            if len(user_viewable_countries) == 0:
                objects = child_model.objects.none()
            elif 'all countries' in user_viewable_countries:
                objects = child_model.objects.all()
            else:
                objects = []
                for obj in child_model.objects.all():
                    if obj.get_country() in user_viewable_countries:
                        objects.append(obj)
            table = MyTable(objects)
            response = HttpResponse(content_type='application/octet-stream')
            zipf.writestr(model_name + ".csv", TableExport('csv', table).export())
        # fix for Linux zip files read in Windows
        for file in zipf.filelist:
            file.create_system = 0
        zipf.close()
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=export.zip'
        zip_buffer.seek(0)
        response.write(zip_buffer.read())
        return response
    except Exception as e:
        logger.error('failed csv download: ' + str(e))

class OccurrenceTable(django_tables2.Table):
    occurrenceID = django_tables2.Column()
    basisOfRecord = django_tables2.Column()
    scientificName = django_tables2.Column()
    eventDate = django_tables2.Column()
    countryCode = django_tables2.Column()
    country = django_tables2.Column()
    taxonRank = django_tables2.Column()
    order = django_tables2.Column()
    kingdom = django_tables2.Column()
    decimalLatitude = django_tables2.Column()
    decimalLongitude = django_tables2.Column()
    geodeticDatum = django_tables2.Column()

def get_bat_attr(bat_data, attr_base_name):

    valid_attr_list = ['Site_location_GPS', 'ANIMAL_ID',
                       'Bat_prepared_as', 'Date_of_trapping']
    if attr_base_name not in valid_attr_list:
        raise ValueError('views.py: get_bat_attr(): {} not supported'.format(attr_base_name))

    if attr_base_name == 'ANIMAL_ID' or attr_base_name == 'Bat_prepared_as':
        attr_source = bat_data
    elif attr_base_name == 'Date_of_trapping':
        attr_source = bat_data.parent
    elif attr_base_name == 'Site_location_GPS':
        attr_source = bat_data.parent.parent
    else:
        raise ValueError('views.py: get_bat_attr(): invalid attr_base_name')

    # find the correct attribute name for list elements
    found_targ_attr = False
    targ_attr = ''
    for curr_attr in dir(attr_source):
        if attr_base_name in curr_attr:
            if found_targ_attr:
                raise ValueError('views.py: get_bat_attr(): found duplicate base attributes!')
            else:
                found_targ_attr = True
                targ_attr = curr_attr

    if not found_targ_attr:
        raise ValueError('views.py: get_bat_attr(): attr_base_name not found')

    return getattr(attr_source, targ_attr)

@login_required
def download_occurrence_data(request):
    user_viewable_countries = [
        group.name.replace('View ', '') for group in request.user.groups.all()]
    if len(user_viewable_countries) == 0:
        bats = BatData.objects.none()
    if 'all countries' in user_viewable_countries:
        bats = BatData.objects.all()
    else:
        bats = BatData.objects.filter(
            parent__parent__country__in=user_viewable_countries)
    rows = []
    for bat_data in bats:
        bat_family, bat_species = get_bat_species(bat_data)
        coords = json.loads(str(get_bat_attr(bat_data, 'Site_location_GPS')).replace("'", '"'))
        animal_id = get_bat_attr(bat_data, 'ANIMAL_ID')
        rows.append({
            "basisOfRecord": "PreservedSpecimen" if get_bat_attr(bat_data, 'Bat_prepared_as') == "Yes" else "Occurrence",
            "taxonRank": "species",
            "order": "Chiroptera",
            "kingdom": "Animalia",
            # A prefix is added to ensure global uniqueness
            "occurrenceID": 'EHA-WAB-NET-' + animal_id,
            "scientificName": bat_species,
            "eventDate": datetime.datetime.strptime(get_bat_attr(bat_data, 'Date_of_trapping'), "%d/%m/%Y").strftime("%B %d, %Y"),
            # Only take country codes from ids that match the standard pattern.
            "countryCode": animal_id[0:2] if re.match(r"\D\D\d+", animal_id) else "",
            "country": bat_data.parent.parent.country,
            "decimalLatitude": coords['latitude'],
            "decimalLongitude": coords['longitude'],
            "geodeticDatum": "WGS 84"
        })
    zip_buffer = BytesIO()
    zipf = zipfile.ZipFile(zip_buffer, 'a')
    table = OccurrenceTable(rows)
    response = HttpResponse(content_type='application/octet-stream')
    zipf.writestr("occurrences.csv", TableExport('csv', table).export())
    # fix for Linux zip files read in Windows
    for file in zipf.filelist:
        file.create_system = 0
    zipf.close()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=export.zip'
    zip_buffer.seek(0)
    response.write(zip_buffer.read())
    return response

def get_recording_parent_ids():
    targ_name = ''
    for name, obj in inspect.getmembers(ec5_models):
        if '_Acoustic_recordi_x' in name:
             targ_name = name

    if targ_name ==  '':
        raise ValueError('Acoustic Recording label not found in ec5_models')

    parent_ids = getattr(ec5_models, targ_name).objects.values('parent')

    return list(parent_ids.values_list('parent', flat=True))

def get_recording_bat_list(bat_list):
    parent_id_list = get_recording_parent_ids()

    recording_uuid_list = []
    for bat in bat_list:
        if bat.uuid in parent_id_list:
            recording_uuid_list.append(bat)

    return recording_uuid_list

def get_query_bat_list(bat_list, q):
    query_bat_list = []
    for bat in bat_list:
        bat_family, bat_species = get_bat_species(bat)
        if bat_species.lower() == q.lower():
            query_bat_list.append(bat)
        elif get_bat_attr(bat, 'ANIMAL_ID').lower() == q.lower():
            query_bat_list.append(bat)
    return query_bat_list

@login_required
def bat_table(request):
    user_viewable_countries = [
        group.name.replace('View ', '') for group in request.user.groups.all()]
    if len(user_viewable_countries) == 0:
        bats = BatData.objects.none()
    elif 'all countries' in user_viewable_countries:
        bats = BatData.objects.all()
    else:
        bats = BatData.objects.filter(
            parent__parent__country__in=user_viewable_countries)
    bats = bats.order_by(bats[0].get_long_name('ANIMAL_ID'))

    if request.GET.get('q'):
        bats = get_query_bat_list(bats, request.GET.get('q'))
    if request.GET.get('hasRecording') == 'on':
        bats = get_recording_bat_list(bats)
    table = BatTable(bats)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'bat_table.html', {'table': table})

def raise_if_user_cannot_access_bat(user, bat_id):
    user_viewable_countries = [
        group.name.replace('View ', '') for group in user.groups.all()]
    if 'all countries' in user_viewable_countries:
        return
    else:
        bats = BatData.objects.filter(
            parent__parent__country__in=user_viewable_countries, uuid=bat_id)
        if len(bats) == 0:
            raise PermissionDenied

def format_dict_data(dict_data, mode):

    # remove keys based on mode
    if mode == 'trapping':
        del dict_data['uuid']
        del dict_data['title']
        del dict_data['parent']
    elif mode == 'site':
        del dict_data['uuid']
        del dict_data['created by']
        del dict_data['created at']
        del dict_data['title']

    # finer changes
    for key,val in dict_data.items():
        # remove time from all dates
        if isinstance(val, datetime.date):
            dict_data[key] = val.date()
        # remove square brackes from python list strings
        if isinstance(val, str) and len(val) > 0 and val[0] == '[':
            dict_data[key] = val.lstrip('[').rstrip(']')
        if val != '' and mode == 'trapping' and 'Page' in key:
            url_list = dict_data[key].url.split('/')
            fn = url_list[-1]
            dict_data[key] = (dict_data[key].url, fn)
        if mode == 'trapping' and 'Number of ' in key and val == None:
            dict_data[key] = 0
        if val != '' and mode == 'site' and key == 'Site location (GPS coords.)':
            tmp_json = json.loads(val.replace("'",'"'))
            dict_data[key] = 'latitude: ' + str(tmp_json['latitude']) + ', ' + 'longitude: ' + str(tmp_json['longitude'])
    return dict_data

def make_verbose_dict(curr_model):
    # make model dictionary with keys from model's verbose names
    name_dict = {}
    for field in curr_model._meta.get_fields():
        if hasattr(field, 'verbose_name'):
            name_dict[field.name] = field.verbose_name
    tmp_dict = model_to_dict(curr_model)
    new_dict = {}
    for key,val in tmp_dict.items():
        if key in name_dict.keys():
            new_dict[name_dict[key]] = val
        else:
            new_dict[key] = val
    return new_dict


@login_required
def bat_view(request, bat_id):
    base_url = '/media/airtable/'
    raise_if_user_cannot_access_bat(request.user, bat_id)
    tables = []
    for model_name, child_model in child_models.items():
        if child_model.parent.field.related_model != BatData:
            continue
        class MyTable(django_tables2.Table):
            name = child_model.name
            class Meta:
                model = child_model
                template_name = 'django_tables2/bootstrap.html'
                exclude = ('id', 'uuid', 'parent',)
                sequence = ('title', '...')
        objects = child_model.objects.filter(parent=bat_id)
        table = MyTable(objects)
        RequestConfig(request).configure(table)
        tables.append(table)
    bat_data = BatData.objects.get(uuid=bat_id)
    objects = SecondaryData.objects.filter(parent=bat_id)
    secondary_data_table = SecondaryDataTable(objects)
    RequestConfig(request).configure(secondary_data_table)
    bat_family, bat_species = get_bat_species(bat_data)
    ### FIX: this need to be generic so it doens't need to be updated
    ###      every time they change the survey!!
    curr_animal_id = get_bat_attr(bat_data, 'ANIMAL_ID')
    #curr_animal_id = getattr(bat_data, 'x_63_ANIMAL_ID_eg_PK00_x')
    barcoding_data = {}
    barcoding_filename_list_dict = {}
    special_barcoding_keys_short = ['gel_photo_labeled', 'raw_host_sequence_txt',
                                    'raw_host_sequence_ab1', 'raw_host_sequence_pdf',
                                    'aligned_host_sequence_submitted_to_blast',
                                    'screenshot_top_5_BLAST_matches',
                                    'rerun_gel_photo_labeled',
                                    'rerun_raw_host_sequence_txt',
                                    'rerun_raw_host_sequence_ab1',
                                    'rerun_raw_host_sequence_pdf',
                                    'rerun_aligned_host_sequence_submitted_to_blast',
                                    'rerun_screenshot_top_5_BLAST_matches',
                                    'rerun2_gel_photo_labeled',
                                    'rerun2_raw_host_sequence_txt',
                                    'rerun2_raw_host_sequence_ab1',
                                    'rerun2_raw_host_sequence_pdf',
                                    'rerun2_aligned_host_sequence_submitted_to_blast',
                                    'rerun2_screenshot_top_5_BLAST_matches']
    if airtable_models.Barcoding.objects.filter(animal_id=curr_animal_id).count() > 0:
        barcoding_data = model_to_dict(airtable_models.Barcoding.objects.get(animal_id=curr_animal_id))

        for special_key in special_barcoding_keys_short:
            if special_key in barcoding_data.keys() and barcoding_data[special_key]:
                file_data = json.loads(barcoding_data[special_key].replace("'", '"'))
                tmp_filename_list = []
                for curr_file_dict in file_data:
                    tmp_filename_list.append(curr_file_dict['filename'])
                barcoding_filename_list_dict[special_key] = tmp_filename_list

    # FIX: may get back a list of screeing data
    screening_data = {}
    screening_filename_list_dict = {}
    new_screening_filename_list_dict = {}
    special_screening_keys_short = ['raw_cov_sequence_ab1', 'raw_cov_sequence_txt',
                                    'raw_cov_sequence_pdf', 'screenshot_top_5_BLAST_matches',
                                    'aligned_cov_sequence_submitted_to_blast',
                                    'gel_photo_labeled','rerun_raw_cov_sequence_ab1',
                                    'rerun_raw_cov_sequence_txt',
                                    'rerun_raw_cov_sequence_pdf',
                                    'rerun_screenshot_top_5_BLAST_matches',
                                    'rerun_aligned_cov_sequence_submitted_to_blast',
                                    'rerun_gel_photo_labeled',
                                    'rerun2_raw_cov_sequence_ab1',
                                    'rerun2_raw_cov_sequence_txt',
                                    'rerun2_raw_cov_sequence_pdf',
                                    'rerun2_screenshot_top_5_BLAST_matches',
                                    'rerun2_aligned_cov_sequence_submitted_to_blast',
                                    'rerun2_gel_photo_labeled']
    if airtable_models.Screening.objects.filter(animal_id=curr_animal_id).count() > 0:
        curr_obj = airtable_models.Screening.objects.get(animal_id='{}'.format(curr_animal_id))
        screening_data = model_to_dict(airtable_models.Screening.objects.get(animal_id=curr_animal_id))

        '''  retrieve from separate class (not currently used)
        raw_cov_sequence_ab1_data = airtable_models.RawCovSequenceAb1.objects.filter(screening_parent__animal_id=curr_animal_id)
        if len(raw_cov_sequence_ab1_data) > 0:
            raw_cov_sequence_ab1_data = list(raw_cov_sequence_ab1_data.values())
        logger.info('*** raw_cov_sequence_ab1_data ***')
        logger.info(raw_cov_sequence_ab1_data)
        ab1_list = []
        for json_obj in raw_cov_sequence_ab1_data:
            if 'filename' in json_obj.keys():
                ab1_list.append(json_obj['filename'])
        new_screening_filename_list_dict['raw_cov_sequence_ab1'] = ab1_list
        logger.info('*** new_screening_filename_list_dict ***')
        logger.info(new_screening_filename_list_dict)
        '''


        for special_key in special_screening_keys_short:
            if special_key in screening_data.keys() and screening_data[special_key]:
                file_data = json.loads(screening_data[special_key].replace("'", '"'))
                tmp_filename_list = []
                for curr_file_dict in file_data:
                    if '.' in curr_file_dict['filename']:
                        thumb_filename_list = curr_file_dict['filename'].split('.')
                        thumb_path = '.' + base_url + '.'.join(thumb_filename_list[:-1]) + '_thumb.' + thumb_filename_list[-1]
                    else:
                        thumb_path = '.' + base_url + curr_file_dict['filename'] + '_thumb'
                    ''' thumbnails are not a current priority, so commenting untill I can get back to it
                    logger.info('*** thumb_path ***')
                    logger.info(thumb_path)
                    if os.path.isfile(thumb_path):
                        logger.info('* got one *')
                    else:
                        logger.info('* no thumb *')
                    '''
                    ## FIX: need to make this a tuple with thubmnail file name
                    tmp_filename_list.append(curr_file_dict['filename'], )
                screening_filename_list_dict[special_key] = tmp_filename_list
        #logger.info('*** screening_filename_list_dict ***')
        #logger.info(screening_filename_list_dict)

    ## convert short key names to verbose - screening
    mod_key_list = []
    for key,value in screening_data.items():
        verbose_name = airtable_models.Screening.get_verbose_from_name(key)
        if verbose_name != '':
            mod_key_list.append((key,verbose_name))
    for tup in mod_key_list:
        screening_data[tup[1]] = screening_data[tup[0]]
        del screening_data[tup[0]]

    ## convert short key names to verbose - barcoding
    mod_key_list = []
    for key,value in barcoding_data.items():
        verbose_name = airtable_models.Barcoding.get_verbose_from_name(key)
        if verbose_name != '':
            mod_key_list.append((key,verbose_name))
    for tup in mod_key_list:
        barcoding_data[tup[1]] = barcoding_data[tup[0]]
        del barcoding_data[tup[0]]

    exclude_fields = ['parent', 'title', 'created_at', 'created_by', 'uuid'] + [f.name for f in bat_family_fields]
    main_data = []
    main_data_dict = {}
    for field in BatData._meta.get_fields():
        if field.is_relation or field.name in exclude_fields:
            continue
        main_data.append((field, getattr(bat_data, field.name),))
        filename = ''
        if 'Picture' in field.name:
            filename_list = str(getattr(bat_data, field.name)).split('/')
            filename = filename_list[-1]
        main_data_dict[field.name] = (field, getattr(bat_data, field.name), filename)

    raw_cov_sequence_ab1_filename = "foo"
    special_screening_keys = ['Gel photo - labeled', 'Raw CoV sequence - .txt files',
                              'Raw CoV sequence - .ab1 files',
                              'Raw CoV sequence - .pdf files',
                              'Aligned CoV sequence (.fasta file) submitted to BLAST',
                              'Screenshot photo of top 5 BLAST matches',
                              'RE-RUN Gel photo - labeled', 'RE-RUN Raw CoV sequence - .txt files',
                              'RE-RUN Raw CoV sequence - .ab1 files',
                              'RE-RUN Raw CoV sequence - .pdf files',
                              'RE-RUN Aligned CoV sequence (.fasta file) submitted to BLAST',
                              'RE-RUN Screenshot photo of top 5 BLAST matches',
                              'RE-RUN 2 Gel photo - labeled', 'RE-RUN Raw CoV sequence - .txt files',
                              'RE-RUN 2 Raw CoV sequence - .ab1 files',
                              'RE-RUN 2 Raw CoV sequence - .pdf files',
                              'RE-RUN 2 Aligned CoV sequence (.fasta file) submitted to BLAST',
                              'RE-RUN 2 Screenshot photo of top 5 BLAST matches']
    special_barcoding_keys = ['Gel photo - labeled', 'Raw host sequence - .txt files',
                              'Raw host sequence - .ab1 files',
                              'Raw host sequence - .pdf files',
                              'Aligned host sequence (.fasta file) submitted to BLAST',
                              'Screenshot photo of top 5 BLAST matches',
                              'RE-RUN Gel photo - labeled',
                              'RE-RUN Raw host sequence - .txt files',
                              'RE-RUN Raw host sequence - .ab1 files',
                              'RE-RUN Raw host sequence - .pdf files',
                              'RE-RUN Aligned host sequence (.fasta file) submitted to BLAST',
                              'RE-RUN Screenshot photo of top 5 BLAST matches',
                              'RE-RUN 2 Gel photo - labeled',
                              'RE-RUN 2 Raw host sequence - .txt files',
                              'RE-RUN 2 Raw host sequence - .ab1 files',
                              'RE-RUN 2 Raw host sequence - .pdf files',
                              'RE-RUN 2 Aligned host sequence (.fasta file) submitted to BLAST',
                              'RE-RUN 2 Screenshot photo of top 5 BLAST matches']

    trapping_event_data = make_verbose_dict(bat_data.parent)

    return render(request, 'bat.html', {
        'main_data': main_data,
        'main_data_dict': main_data_dict,
        'bat_data': bat_data,
        'bat_species': bat_species,
        'trapping_event_form': TrappingEventForm(instance=bat_data.parent),
        'tables': tables,
        'secondary_data_table': secondary_data_table,
        'barcoding_data': format_dict_data(barcoding_data, 'barcoding'),
        'screening_data': format_dict_data(screening_data, 'screening'),
        'trapping_event_data': format_dict_data(trapping_event_data, 'trapping'),
        'base_url': base_url,
        'screening_filename_list_dict': screening_filename_list_dict,
        'barcoding_filename_list_dict': barcoding_filename_list_dict,
        'special_screening_keys': special_screening_keys,
        'special_barcoding_keys': special_barcoding_keys})
