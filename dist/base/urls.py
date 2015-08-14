import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

from yqj.views import *
from news.views import NewsView, NewsDetailView
from event.views import EventView, EventDetailView


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^vendor/(?P<path>.*)$', serve,  {'document_root': os.path.join(settings.BASE_DIR, 'vendor')}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('yqj.views',
    url(r'^$', 'index_view'),
    url(r'^location/(\d+)/$', LocationView.as_view()),
    url(r'^category/(\d+)/$', CategoryView.as_view()),
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^weixin/(\d+)/$', WeixinDetailView.as_view()),
    url(r'^weibo/$', WeiboView.as_view()),
    url(r'^custom/$', CustomListView.as_view()),
    url(r'^custom/(\d+)/$', CustomView.as_view()),
    # url(r'^product/(\d*)/?$', ProductView.as_view()),
    url(r'^product/(?P<id>\d*)/?$', ProductView.as_view()),
    url(r'^collection/$', CollectionView.as_view()),
    url(r'^settings/$', SettingsView.as_view()),
    url(r'^user/$', UserAdminView.as_view()),
    url(r'^inspection/$', InspectionView.as_view()),
    url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
    url(r'^search/(.+)/$', SearchView.as_view()),
    # url(r'^search/(\s+)/$', SearchView.as_view()),
)

urlpatterns += patterns('news.views',
    url(r'^news/$', NewsView.as_view()),
    url(r'^news/(\d+)/$', NewsDetailView.as_view()),
)

urlpatterns += patterns('event.views',
    url(r'^event/$', EventView.as_view()),
    url(r'^event/(\d+)/$', EventDetailView.as_view()),
)
