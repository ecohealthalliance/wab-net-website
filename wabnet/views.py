from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.forms import ModelForm
from django_tables2 import RequestConfig
import django_tables2
from .models import x_field_data_forms_x, SecondaryData
from .tables import x_field_data_forms_x_Table

class SecondaryDataForm(ModelForm):
    class Meta:
        model = SecondaryData
        exclude = []


import inspect
from . import ec5_models
child_models = {}
for name, obj in inspect.getmembers(ec5_models):
    if inspect.isclass(obj):
        if hasattr(obj, 'parent'):
            child_models[name] = obj

def splash(request):
    return render(request, 'splash.html')

def site_table(request):
    table = x_field_data_forms_x_Table(x_field_data_forms_x.objects.all())
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'table.html', {'table': table})

# def bat_table(request):
#     #table = x_field_data_forms_x_Table(x_field_data_forms_x.objects.all())
#     RequestConfig(request, paginate={'per_page': 20}).configure(table)
#     return render(request, 'bat_table.html', {'table': table})

def site(request, id):
    tables = []
    site_data = x_field_data_forms_x.objects.get(uuid=id)
    for model_name, child_model in list(child_models.items()) + [(None, SecondaryData)]:
        class MyTable(django_tables2.Table):
            name = child_model.name
            class Meta:
                model = child_model
                template_name = 'django_tables2/bootstrap.html'
                exclude = ('id', 'parent',)
        objects = child_model.objects.filter(parent=id)
        table = MyTable(objects)
        RequestConfig(request).configure(table)
        tables.append(table)
    return render(request, 'site.html', {'site_data': site_data, 'tables': tables})

def attach_data(request, id):
    if request.method == 'POST':
        form = SecondaryDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sites/' + id)
        else:
            return render(request, 'attach.html', {'form': form})
    site_data = x_field_data_forms_x.objects.get(uuid=id)
    secondary_data = SecondaryData(parent=site_data)
    return render(request, 'attach.html', {'form': SecondaryDataForm(instance=secondary_data)})

from django_tables2.export.export import TableExport
import zipfile
from six import BytesIO
def download_site_data(request, id):
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
