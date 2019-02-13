# tutorial/tables.py
import django_tables2 as tables
from .models import SiteData, BatData, SecondaryData
from django_tables2.utils import A

class SiteTable(tables.Table):
    class Meta:
        model = SiteData
        fields = ('title', 'country', 'uuid')

    uuid = tables.LinkColumn('sites',
        args=[A('uuid')],
        text='View data for site',
        attrs={'th':{'hidden': True}})

class BatTable(tables.Table):
    name = "Bat Information"
    class Meta:
        model = BatData
        exclude = ('uuid', 'parent',)
        sequence = ('title', '...')

    title = tables.LinkColumn('bats',
        args=[A('uuid')])

class SecondaryDataTable(tables.Table):
    name = "Secondary Data"
    class Meta:
        model = SecondaryData
        exclude = ('id', 'parent',)
