from django.urls import include, re_path
from rest_framework_jwt import views

from observer.apps.seer.views import logout_view

urlpatterns = [
    re_path(r'^yqj/', include('observer.apps.yqj.urls')),
    re_path(r'^seer/', include('observer.apps.seer.urls')),
    re_path(r'^postprocess/',include('observer.apps.postprocess.urls'))
]

urlpatterns += [
    re_path(r'^token-auth$', views.obtain_jwt_token),
    re_path(r'^token-refresh$', views.refresh_jwt_token),
    re_path(r'^token-verify$', views.verify_jwt_token),
    re_path(r'^token-revoke$', logout_view),
]
