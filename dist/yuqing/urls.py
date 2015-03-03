from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('yqj.views',
    url(r'^$', 'index_view'),
    url(r'^location/(\d+)/$', 'location_view'),
    url(r'^category/(\d+)/$', 'category_view'),
    url(r'^person/(\d+)/$', 'person_view'),
)
