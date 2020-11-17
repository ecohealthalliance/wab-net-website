from airtable_tools.import_from_airtable import import_from_airtable
from django.core.management.base import BaseCommand, CommandError
import importlib

class Command(BaseCommand):
    help = 'import data for the models in the given module'

    def add_arguments(self, parser):
        parser.add_argument('airtable_models')

    def handle(self, *args, **options):
        import_from_airtable(importlib.import_module(options['airtable_models']))
