import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve
from yqj.views import *

from django.conf import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^vendor/(?P<path>.*)$', serve,  {'document_root': os.path.join(settings.BASE_DIR, 'vendor')}),
)

urlpatterns += patterns('yqj.views',
    url(r'^$', 'index_view'),
    url(r'^location/(\d+)/$', LocationView.as_view()),
    url(r'^category/(\d+)/$', CategoryView.as_view()),
    url(r'^register/$', 'register_view'),
    url(r'^news/$', NewsView.as_view()),
    url(r'^news/(\d+)/$', NewsDetailView.as_view()),
    url(r'^event/$', EventView.as_view()),
    url(r'^event/(\d+)$', EventDetailView.as_view()),
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^weixin/(\d+)/$', WeixinDetailView.as_view()),
    url(r'^weibo/$', WeiboView.as_view()),
    url(r'^custom/$', 'custom_view'),
    url(r'^collection/$', CollectionView.as_view()),
    url(r'^settings/$', SettingsView.as_view()),
    url(r'^user/$', UserView.as_view()),
    url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
    url(r'^search/(\S+)/$', 'search_view'),
)
