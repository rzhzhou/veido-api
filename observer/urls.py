from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path, path


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'^api/', include('observer.apps.base.urls')),
]
