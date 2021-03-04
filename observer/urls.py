from django.contrib import admin
from django.urls import include, re_path


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('observer.apps.dyy.urls')),
    re_path(r'^api/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path('accounts/', include('django.contrib.auth.urls')),
]
