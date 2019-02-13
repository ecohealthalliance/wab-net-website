from django.contrib import admin
from .models import SecondaryData, EpiCollectImport

@admin.register(SecondaryData)
class SecondaryDataAdmin(admin.ModelAdmin):
    pass

@admin.register(EpiCollectImport)
class EpiCollectImportAdmin(admin.ModelAdmin):
    pass

admin.autodiscover()
import allauth.socialaccount.models as allauth_models
admin.site.unregister(allauth_models.SocialApp)
admin.site.unregister(allauth_models.SocialAccount)
admin.site.unregister(allauth_models.SocialToken)

from allauth.account.models import EmailAddress
admin.site.unregister(EmailAddress)

from django.contrib.sites.models import Site
admin.site.unregister(Site)

my_site = Site.objects.get(pk=1)
my_site.domain = 'wabnet.eha.io'
my_site.name = 'WAB-net'
my_site.save()
