import requests
from wabnet.utils import format_name
from wabnet.settings import EC5_SECRET_KEY, EC5_CLIENT_ID, EC5_PROJECT_NAME

response = requests.post('https://five.epicollect.net/api/oauth/token', data={
  'grant_type': 'client_credentials',
  'client_id': EC5_CLIENT_ID,
  'client_secret': EC5_SECRET_KEY
})

response.raise_for_status()
token = response.json()

response = requests.get('https://five.epicollect.net/api/export/project/' + EC5_PROJECT_NAME, headers={
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
    result.append("    created_at = models.TextField()")
    result.append("    created_by = models.TextField()")
    result.append("    title = models.TextField()")
    if parent_ref:
        result.append("    parent = models.ForeignKey(%s, on_delete=models.CASCADE)" % format_name(all_form_mappings[parent_ref]))
    def generate_vars_from_inputs(inputs):
        for inp in inputs:
            if inp['type'] == 'group':
                generate_vars_from_inputs(inp['group'])
            elif inp['type'] in ['photo', 'video', 'audio']:
                result.append("    %s = models.FileField(upload_to='ec5/', verbose_name='%s')" % (format_name(all_form_mappings[inp['ref']]), inp['question']))
            elif inp['type'] != 'branch':
                result.append("    %s = models.TextField(verbose_name='%s')" % (format_name(all_form_mappings[inp['ref']]), inp['question']))
    generate_vars_from_inputs(inputs)
    for inp in inputs:
        if inp['type'] == 'branch':
            result.append("\n")
            result.append(generate_form_models(inp['branch'], inp['ref'], ref, is_branch=True, name=inp['question']))
    return "\n".join(result)

with open('wabnet/ec5_models.py', 'w') as f:
    f.write("""# These models were generated from the Epicollect 5 project via generate_models.py
from django.db import models
from . import entity_keywords_model
from django.contrib.contenttypes.fields import GenericRelation

project_name = '%s'

""" % resp_json['data']['project']['slug'])
    for form in resp_json['data']['project']['forms']:
        all_form_mappings[form['ref']] = form['slug'].replace('-', '_')
        f.write(generate_form_models(form['inputs'], form['ref'], name=form['name']))
