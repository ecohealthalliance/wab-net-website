# tutorial/tables.py
import django_tables2 as tables
from .models import x_field_data_forms_x
from django_tables2.utils import A

class x_field_data_forms_x_Table(tables.Table):
    class Meta:
        model = x_field_data_forms_x
        template_name = 'django_tables2/bootstrap.html'
        fields = ('x_3_Site_name_x', 'x_1_Country_x', 'uuid')

    uuid = tables.LinkColumn('sites',
        args=[A('uuid')],
        text='View data for site',
        attrs={'th':{'hidden': True}})
