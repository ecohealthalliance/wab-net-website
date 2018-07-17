import datetime
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


class SecondaryDataForm(forms.ModelForm):
    class Meta:
        model = SecondaryData
        fields = ['file']

class SiteDataForm(forms.ModelForm):
    class Meta:
        model = SiteData
        exclude = ['title', 'uuid', 'created_at', 'created_by', 'country']

class BatDataForm(forms.ModelForm):
    class Meta:
        model = BatData
        exclude = ['parent', 'title', 'created_at', 'created_by', 'uuid']

class TrappingEventForm(forms.ModelForm):
    class Meta:
        model = TrappingEvent
        exclude = ['title', 'uuid', 'parent']

import inspect
from . import ec5_models
child_models = {}
for name, obj in inspect.getmembers(ec5_models):
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        if hasattr(obj, 'parent'):
            child_models[name] = obj

def splash(request):
    return render(request, 'splash.html')

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
                template_name = 'django_tables2/bootstrap.html'
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
            tmp_model = child_model
            ancestors = 0
            while hasattr(tmp_model, 'parent'):
                tmp_model = tmp_model.parent.field.related_model
                ancestors += 1
            # Build a query that requires the root ancestor to have a country
            # property matching matching one of the user's viewalbe countries.
            objects = child_model.objects.filter(**{
                ('parent__' * ancestors) + "__country__in": user_viewable_countries
            })
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

@login_required
def bat_table(request):
    user_viewable_countries = [
        group.name.replace('View ', '') for group in request.user.groups.all()]
    if 'all countries' in user_viewable_countries:
        bats = BatData.objects.all()
    else:
        bats = BatData.objects.filter(
            parent__country__in=user_viewable_countries)
    if request.GET.get('q'):
        bats = bats.filter(keywords__keywords__contains=request.GET.get('q'))
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
            parent__country__in=user_viewable_countries, uuid=bat_id)
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
    return render(request, 'bat.html', {
        'form': BatDataForm(instance=bat_data),
        'bat_data': bat_data,
        'trapping_event_form': TrappingEventForm(instance=bat_data.parent),
        'tables': tables,
        'secondary_data_table': secondary_data_table})
