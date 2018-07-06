from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import django.forms as forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django_tables2 import RequestConfig
import django_tables2
from .models import SiteData, BatCaptureData, SecondaryData
from .entity_keywords_model import EntityKeywords
from .tables import SiteTable, BatTable, SecondaryDataTable


class SecondaryDataForm(forms.ModelForm):
    class Meta:
        model = SecondaryData
        exclude = ['parent']

import inspect
from . import ec5_models
child_models = {}
for name, obj in inspect.getmembers(ec5_models):
    if inspect.isclass(obj):
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
    return render(request, 'table.html', {'table': table})

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
def site(request, id):
    raise_if_user_cannot_access_site(request.user, id)
    tables = []
    site_data = SiteData.objects.get(uuid=id)
    for model_name, child_model in child_models.items():
        class MyTable(django_tables2.Table):
            name = child_model.name
            class Meta:
                model = child_model
                template_name = 'django_tables2/bootstrap.html'
                exclude = ('id', 'parent',)
                sequence = ('title', '...')
        objects = child_model.objects.filter(parent=id)
        table = MyTable(objects)
        RequestConfig(request).configure(table)
        tables.append(table)
    objects = SecondaryData.objects.filter(parent=id)
    print(len(objects))
    secondary_data_table = SecondaryDataTable(objects)
    RequestConfig(request).configure(secondary_data_table)
    return render(request, 'site.html', {
        'site_data': site_data,
        'tables': tables,
        'secondary_data_table': secondary_data_table})

def attach_data(request, id):
    if request.method == 'POST':
        form = SecondaryDataForm(request.POST, request.FILES)
        if form.is_valid():
            secondary_data = form.save(commit=False)
            secondary_data.parent = SiteData.objects.get(uuid=id)
            secondary_data.save()
            return HttpResponseRedirect('/sites/' + id)
        else:
            return render(request, 'attach.html', {'form': form})
    site_data = SiteData.objects.get(uuid=id)
    secondary_data = SecondaryData(parent=site_data)
    return render(request, 'attach.html', {'form': SecondaryDataForm(instance=secondary_data)})

from django_tables2.export.export import TableExport
import zipfile
from six import BytesIO
def download_site_data(request, id):
    raise_if_user_cannot_access_site(request.user, id)
    zip_buffer = BytesIO()
    zipf = zipfile.ZipFile(zip_buffer, 'a')
    for model_name, child_model in list(child_models.items()) + [('secondary_data', SecondaryData)]:
        class MyTable(django_tables2.Table):
            name = child_model.name
            class Meta:
                model = child_model
                template_name = 'django_tables2/bootstrap.html'
                exclude = ('id', 'parent',)
        objects = child_model.objects.filter(parent=id)
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
        bats = BatCaptureData.objects.all()
    else:
        bats = BatCaptureData.objects.filter(
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
        bats = BatCaptureData.objects.filter(
            parent__country__in=user_viewable_countries, id=bat_id)
        if len(bats) == 0:
            raise PermissionDenied

@login_required
def bat(request, bat_id):
    raise_if_user_cannot_access_bat(request.user, bat_id)
    bat_data = BatCaptureData.objects.get(id=bat_id)
    return render(request, 'bat.html', {
        'bat_data': bat_data,
        'tables': []})
