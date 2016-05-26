from django.conf.urls import include, url
from rest_framework_jwt import views

from observer.apps.riskmonitor.urls import urlpatterns as riskmonitor_urls

urlpatterns = [
    url(r'', include(riskmonitor_urls, app_name='riskmonitor_urls',
                     namespace='riskmonitor_urls')),
]

urlpatterns += [
    url(r'^token-auth$', views.obtain_jwt_token),
    url(r'^token-refresh$', views.refresh_jwt_token),
    url(r'^token-verify$', views.verify_jwt_token),
]
