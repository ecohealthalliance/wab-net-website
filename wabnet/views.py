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
    return render(request, 'site.html', {
        'form': SiteDataForm(instance=site_data),
        'site_data': site_data,
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
    user_viewable_countries = [
        group.name.replace('View ', '') for group in request.user.groups.all()]
    zip_buffer = BytesIO()
    zipf = zipfile.ZipFile(zip_buffer, 'a')
    for model_name, child_model in list(child_models.items()) + [
        ('SiteData', SiteData),
        ('SecondaryData', SecondaryData)]:
        class MyTable(django_tables2.Table):
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

    valid_attr_list = ['Site_location_GPS', 'ANIMAL_ID_eg_PK00',
                       'Bat_prepared_as', 'Date_of_trapping']
    if attr_base_name not in valid_attr_list:
        raise ValueError('views.py: get_bat_attr(): {} not supported'.format(attr_base_name))

    if attr_base_name == 'ANIMAL_ID_eg_PK00' or attr_base_name == 'Bat_prepared_as':
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
        raise ValueError('views.py: get_bat_attr(): base_attr_name not found')

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
        animal_id = get_bat_attr(bat_data, 'ANIMAL_ID_eg_PK00')
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
        if bat_species == q:
            query_bat_list.append(bat)
        elif get_bat_attr(bat, 'ANIMAL_ID_eg_PK00') == q:
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

@login_required
def bat_view(request, bat_id):
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
    logger.info(getattr(bat_data, 'x_63_ANIMAL_ID_eg_PK00_x'))
    curr_animal_id = getattr(bat_data, 'x_63_ANIMAL_ID_eg_PK00_x')
    barcoding_data = {}
    barcoding_filename_list_dict = {}
    special_barcoding_keys_short = ['gel_photo_labeled', 'raw_host_sequence_txt',
                                    'raw_cov_sequence_ab1', 'raw_cov_sequence_pdf',
                                    'aligned_host_sequence_submitted_to_blast',
                                    'screenshot_top_5_BLAST_matches']
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
    special_screening_keys_short = ['raw_cov_sequence_ab1', 'raw_cov_sequence_txt',
                                    'raw_cov_sequence_pdf', 'screenshot_top_5_BLAST_matches',
                                    'aligned_cov_sequence_submitted_to_blast',
                                    'gel_photo_labeled']
    if airtable_models.Screening.objects.filter(animal_id=curr_animal_id).count() > 0:
        curr_obj = airtable_models.Screening.objects.get(animal_id='{}'.format(curr_animal_id))
        screening_data = model_to_dict(airtable_models.Screening.objects.get(animal_id=curr_animal_id))
        # change dictionary keys to verbose string
        '''  retrieve from separate class (not currently used)
        raw_cov_sequence_ab1_data = airtable_models.RawCovSequenceAb1.objects.filter(screening_parent__animal_id=curr_animal_id)
        if len(raw_cov_sequence_ab1_data) > 0:
            raw_cov_sequence_ab1_data = list(raw_cov_sequence_ab1_data.values())
        '''

        for special_key in special_screening_keys_short:
            if special_key in screening_data.keys() and screening_data[special_key]:
                file_data = json.loads(screening_data[special_key].replace("'", '"'))
                tmp_filename_list = []
                for curr_file_dict in file_data:
                    tmp_filename_list.append(curr_file_dict['filename'])
                screening_filename_list_dict[special_key] = tmp_filename_list

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
    for field in BatData._meta.get_fields():
        if field.is_relation or field.name in exclude_fields:
            continue
        main_data.append((field, getattr(bat_data, field.name),))

    raw_cov_sequence_ab1_filename = "foo"
    base_url = '/media/airtable/'
    special_screening_keys = ['Gel photo - labeled', 'Raw CoV sequence - .txt files',
                              'Raw CoV sequence - .ab1 files',
                              'Raw CoV sequence - .pdf files',
                              'Aligned CoV sequence (.fasta file) submitted to BLAST',
                              'Screenshot photo of top 5 BLAST matches']
    special_barcoding_keys = ['Gel photo - labeled', 'Raw host sequence - .txt files',
                              'Raw host sequence - .ab1 files',
                              'Raw host sequence - .pdf files',
                              'Aligned host sequence (.fasta file) submitted to BLAST',
                              'Screenshot photo of top 5 BLAST matches']
    return render(request, 'bat.html', {
        'main_data': main_data,
        'bat_data': bat_data,
        'bat_species': bat_species,
        'trapping_event_form': TrappingEventForm(instance=bat_data.parent),
        'tables': tables,
        'secondary_data_table': secondary_data_table,
        'barcoding_data': barcoding_data,
        'screening_data': screening_data,
        'base_url': base_url,
        'screening_filename_list_dict': screening_filename_list_dict,
        'barcoding_filename_list_dict': barcoding_filename_list_dict,
        'special_screening_keys': special_screening_keys,
        'special_barcoding_keys': special_barcoding_keys})
