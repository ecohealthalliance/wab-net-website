import requests
import os
from ec5_tools.utils import format_name
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import sys

class Command(BaseCommand):
    help = 'Create models for the EC5 survey specified in settings'

    def add_arguments(self, parser):
        parser.add_argument('project_dir', nargs='?', default='')

    def handle(self, *args, **options):
        response = requests.post('https://five.epicollect.net/api/oauth/token', data={
          'grant_type': 'client_credentials',
          'client_id': settings.EC5_CLIENT_ID,
          'client_secret': settings.EC5_SECRET_KEY
        })

        response.raise_for_status()
        token = response.json()

        response = requests.get('https://five.epicollect.net/api/export/project/' + settings.EC5_PROJECT_NAME, headers={
            'Authorization': 'Bearer ' + token['access_token']
        })
        response.raise_for_status()
        resp_json = response.json()

        def get_form_mappings(form):
            result = {}
            for key, value in form.items():
                result[key] = value['map_to']
                if len(value['branch']) > 0:
                    result.update(get_form_mappings(value['branch']))
                if len(value['group']) > 0:
                    result.update(get_form_mappings(value['group']))
            return result


        all_form_mappings = {}
        for mapping in resp_json['meta']['project_mapping']:
            if mapping['is_default']:
                for form_meta in mapping['forms'].values():
                    all_form_mappings.update(get_form_mappings(form_meta))
                break

        def generate_form_models(inputs, ref, parent_ref=None, is_branch=False, name=None):
            result = []
            result.append("class %s(models.Model):" % format_name(all_form_mappings[ref]))
            result.append("    keywords = GenericRelation(entity_keywords_model.EntityKeywords)")
            result.append("    name = '%s'" % name)
            result.append("    ec5_is_branch = " + str(is_branch))
            result.append("    ec5_ref = '%s'" % ref)
            if not is_branch:
                result.append("    uuid = models.CharField(max_length=100, primary_key=True)")
            else:
                result.append("    id = models.CharField(max_length=100, primary_key=True)")
            result.append("    created_at = models.DateTimeField()")
            result.append("    created_by = models.TextField()")
            result.append("    title = models.TextField()")
            if parent_ref:
                result.append("    parent = models.ForeignKey(%s, on_delete=models.CASCADE)" % format_name(all_form_mappings[parent_ref]))
            def generate_vars_from_inputs(inputs):
                for inp in inputs:
                    # if inp['ref'] not in all_form_mappings:
                    #     print(inp)
                    if inp['type'] == 'group':
                        generate_vars_from_inputs(inp['group'])
                    elif inp['type'] in ['photo', 'video', 'audio']:
                        result.append("    %s = models.FileField(upload_to='ec5/', verbose_name='%s')" % (format_name(all_form_mappings[inp['ref']]), inp['question']))
                    elif inp['type'] == 'integer':
                        result.append("    %s = models.IntegerField(verbose_name='%s', blank=True, null=True)" % (format_name(all_form_mappings[inp['ref']]), inp['question']))
                    elif inp['type'] == 'branch':
                        pass
                    elif inp['type'] == 'readme':
                        pass
                    else:
                        result.append("    %s = models.TextField(verbose_name='%s')" % (format_name(all_form_mappings[inp['ref']]), inp['question']))
            generate_vars_from_inputs(inputs)

            def generate_get_country_method(model_name):
                print(model_name)
                out_str = ''
                if 'Site_photographs' in model_name:
                    out_str = '\n    def get_country(self):\n'
                    out_str += '        return self.parent.country'
                elif 'Site_video_option' in model_name:
                    out_str = '\n    def get_country(self):\n'
                    out_str += '        return self.parent.country'
                elif model_name == 'SiteData':
                    out_str = '\n    def get_country(self):\n'
                    out_str += '        return self.country'
                elif model_name == 'TrappingEvent':
                    out_str = '\n    def get_country(self):\n'
                    out_str += '        return self.parent.country'
                elif 'Acoustic_recordi' in model_name:
                    out_str = '\n    def get_country(self):\n'
                    out_str += '        return self.parent.parent.parent.country'
                elif model_name == 'BatData':
                    out_str = '\n    def get_country(self):\n'
                    out_str += '        return self.parent.parent.country'
                print(out_str)
                return out_str

            result.append(generate_get_country_method(format_name(all_form_mappings[ref])))

            for inp in inputs:
                if inp['type'] == 'branch':
                    result.append("\n")
                    result.append(generate_form_models(inp['branch'], inp['ref'], ref, is_branch=True, name=inp['question']))
            return "\n".join(result)

        with open(os.path.join(options['project_dir'], 'ec5_models.py'), 'w') as f:
            f.write("""# These models were generated from an Epicollect 5 project via generate_models.py
from django.db import models
from ec5_tools import entity_keywords_model
from django.contrib.contenttypes.fields import GenericRelation

project_name = '%s'

""" % resp_json['data']['project']['slug'])
            parent_form_ref = None
            for form in resp_json['data']['project']['forms']:
                all_form_mappings[form['ref']] = form['slug'].replace('-', '_')
                f.write(generate_form_models(
                    form['inputs'],
                    form['ref'],
                    name=form['name'],
                    parent_ref=parent_form_ref))
                f.write('\n\n')
                parent_form_ref = form['ref']
