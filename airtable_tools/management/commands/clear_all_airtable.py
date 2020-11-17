from airtable_tools.import_from_airtable import clear_all_airtable
from django.core.management.base import BaseCommand, CommandError
import importlib

class Command(BaseCommand):
    help = 'remove all airtable models and media files'

    def add_arguments(self, parser):
        parser.add_argument('airtable_models')

    def handle(self, *args, **options):
        clear_all_airtable(importlib.import_module(options['airtable_models']))
