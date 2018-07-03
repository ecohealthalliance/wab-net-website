from django.http import HttpResponseRedirect
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

def site(request, id):
    tables = []
    site_data = x_field_data_forms_x.objects.get(uuid=id)
    for model_name, child_model in child_models.items():
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
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/sites/' + id)
        else:
            return render(request, 'attach.html', {'form': form})
    site_data = x_field_data_forms_x.objects.get(uuid=id)
    secondary_data = SecondaryData(parent=site_data)
    return render(request, 'attach.html', {'form': SecondaryDataForm(instance=secondary_data)})

# def site(request, id):
#     forms = []
#     for name, model in child_models.items():
#         print(name)
#         data = model.objects.filter(parent=id)
#         if len(data) > 0:
#             class MyForm(ModelForm):
#                 class Meta:
#                     model = next(iter(child_models.values()))
#                     exclude = []
#                     #fields = ['pub_date', 'headline', 'content', 'reporter']
#             forms.append(MyForm(data[0]))
#     return render(request, 'site.html', {'forms': forms})
