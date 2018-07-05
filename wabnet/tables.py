# tutorial/tables.py
import django_tables2 as tables
from .models import x_field_data_forms_x, x_43_Bat_capture_data_x, SecondaryData
from django_tables2.utils import A

class SiteTable(tables.Table):
    class Meta:
        model = x_field_data_forms_x
        template_name = 'django_tables2/bootstrap.html'
        fields = ('x_3_Site_name_x', 'x_1_Country_x', 'uuid')

    uuid = tables.LinkColumn('sites',
        args=[A('uuid')],
        text='View data for site',
        attrs={'th':{'hidden': True}})

class BatTable(tables.Table):
    class Meta:
        model = x_43_Bat_capture_data_x
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'parent',)
        sequence = ('title', '...')

    title = tables.LinkColumn('bats',
        args=[A('id')])

class SecondaryDataTable(tables.Table):
    name = "Secondary Data"
    class Meta:
        model = SecondaryData
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'parent',)
