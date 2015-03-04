import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve

from django.conf import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^vendor/(?P<path>.*)$', serve,  {'document_root': os.path.join(settings.BASE_DIR, 'vendor')}),
)

urlpatterns += patterns('yqj.views',
    url(r'^$', 'index_view'),
    url(r'^location/(\d+)/$', 'location_view'),
    url(r'^category/(\d+)/$', 'category_view'),
    url(r'^person/(\d+)/$', 'person_view'),
    url(r'^login/$', 'login_view'),
)