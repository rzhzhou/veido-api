import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

from yqj.views import *
from news.views import NewsView, NewsDetailView
from event.views import EventView, EventDetailView
from weixin.views import WeixinView, WeixinDetailView
from weibo.views import WeiboView
from custom.views import CustomView, CustomDetailView
from product.views import ProductView
from inspection.views import InspectionView


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^vendor/(?P<path>.*)$', serve,  {'document_root': os.path.join(settings.BASE_DIR, 'vendor')}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('yqj.views',
    url(r'^$', 'index_view'),
    url(r'^location/(\d+)/$', LocationView.as_view()),
    url(r'^category/(\d+)/$', CategoryView.as_view()),
    url(r'^collection/$', CollectionView.as_view()),
    url(r'^settings/$', SettingsView.as_view()),
    url(r'^user/$', UserAdminView.as_view()),
    url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
    url(r'^search/(.+)/$', SearchView.as_view()),
)

urlpatterns += patterns('news.views',
    url(r'^news/$', NewsView.as_view()),
    url(r'^news/(\d+)/$', NewsDetailView.as_view()),
)

urlpatterns += patterns('event.views',
    url(r'^event/$', EventView.as_view()),
    url(r'^event/(\d+)/$', EventDetailView.as_view()),
)

urlpatterns += patterns('weibo.views',
    url(r'^weibo/$', WeiboView.as_view()),
)

urlpatterns += patterns('weixin.views',
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^weixin/(\d+)/$', WeixinDetailView.as_view()),
)

urlpatterns += patterns('custom.views',
    url(r'^custom/$', CustomView.as_view()),
    url(r'^custom/(\d+)/$', CustomDetailView.as_view()),
)

urlpatterns += patterns('product.views',
    url(r'^product/(?P<id>\d*)/?$', ProductView.as_view()),
)

urlpatterns += patterns('inspection.views',
    url(r'^inspection/$', InspectionView.as_view()),
)
