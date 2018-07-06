# tutorial/tables.py
import django_tables2 as tables
from .models import SiteData, BatCaptureData, SecondaryData
from django_tables2.utils import A

class SiteTable(tables.Table):
    class Meta:
        model = SiteData
        template_name = 'django_tables2/bootstrap.html'
        fields = ('title', 'country', 'uuid')

    uuid = tables.LinkColumn('sites',
        args=[A('uuid')],
        text='View data for site',
        attrs={'th':{'hidden': True}})

class BatTable(tables.Table):
    class Meta:
        model = BatCaptureData
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
