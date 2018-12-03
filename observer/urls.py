from django.contrib import admin
from django.urls import include, re_path


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('observer.base.urls')),
    # re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # re_path(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myapp/login.html'}),
]
