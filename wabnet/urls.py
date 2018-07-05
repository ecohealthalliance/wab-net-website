"""wabnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import site_table, site, attach_data, splash, download_site_data, bat_table, bat
from . import settings

urlpatterns = [
    path('', splash),
    path('admin/', admin.site.urls),
    path('sites/', site_table),
    path('sites/<id>', site, name='sites'),
    path('sites/<id>/download', download_site_data, name='download_site'),
    path('sites/<id>/attach', attach_data, name='attach_data'),
    path('bats/', bat_table),
    path('bats/<bat_id>', bat, name='bats'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
