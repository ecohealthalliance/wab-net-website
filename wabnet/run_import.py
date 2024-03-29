import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from ec5_tools.import_from_epicollect import import_from_epicollect
from airtable_tools.import_from_airtable import import_from_airtable
from . import ec5_models
from . import airtable_models
from .models import EpiCollectImport
from django.core.mail import send_mail

def throttle(min_delay):
    def decorator(func):
        last_invocation = {}
        def wrapper(*args, **kwargs):
            if 'value' not in last_invocation or (last_invocation['value'] + min_delay) < datetime.datetime.now():
                last_invocation['value'] = datetime.datetime.now()
                return func(*args, **kwargs)
            else:
                return HttpResponseBadRequest("This action was performed recently. Please wait to invoke it agian.")
        return wrapper
    return decorator

@throttle(datetime.timedelta(seconds=60*60))
def reimport_all_data(request):
    import_data = EpiCollectImport(import_type="full")
    import_data.save()
    import_from_epicollect(ec5_models)
    import_data.success = True
    import_data.save()

    return HttpResponse('success')

@throttle(datetime.timedelta(seconds=10*60))
def sync_new_data(request):
    try:
        import_data = EpiCollectImport(import_type="sync")
        import_data.save()
        import_from_epicollect(ec5_models, only_new_data=True)
        import_from_airtable(airtable_models, only_new_data=True)
        import_data.success = True
        import_data.save()
    except Exception as e:
        send_mail('WAB-NET-Website sync failed',
                  str(e),
                  'young@ecohealthalliance.org',
                  ['young@ecohealthalliance.org'],
                  fail_silently=False)
        raise
        return HttpResponse('sync failed')
    return HttpResponse('success')
