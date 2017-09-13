from django.conf.urls import include, url
from rest_framework_jwt import views

from observer.apps.seer.views import logout_view

urlpatterns = [
    url(r'^yqj/', include('observer.apps.yqj.urls')),
    url(r'^seer/', include('observer.apps.seer.urls'))
]

urlpatterns += [
    url(r'^token-auth$', views.obtain_jwt_token),
    url(r'^token-refresh$', views.refresh_jwt_token),
    url(r'^token-verify$', views.verify_jwt_token),
    url(r'^token-revoke$', logout_view),
]
