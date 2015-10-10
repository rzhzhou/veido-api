import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

from backend.urlservice import urls, urls_api

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('backend.urlservice.urls')),
    url(r'^api/', include('backend.urlservice.urls_api')),
    url(r'^vendor/(?P<path>.*)$', serve,  {'document_root': os.path.join(settings.BASE_DIR, 'vendor')}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






