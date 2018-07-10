import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from ec5_tools.import_from_epicollect import import_from_epicollect
from . import ec5_models

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
    import_from_epicollect(ec5_models)
    return HttpResponse('success')

@throttle(datetime.timedelta(seconds=10*60))
def sync_new_data(request):
    import_from_epicollect(ec5_models, only_new_data=True)
    return HttpResponse('success')
