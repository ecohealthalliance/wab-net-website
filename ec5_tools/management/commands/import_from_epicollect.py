from ec5_tools.import_from_epicollect import import_from_epicollect
from django.core.management.base import BaseCommand, CommandError
import importlib

class Command(BaseCommand):
    help = 'import data for the models in the given module'

    def add_arguments(self, parser):
        parser.add_argument('ec5_models')

    def handle(self, *args, **options):
        import_from_epicollect(importlib.import_module(options['ec5_models']))
