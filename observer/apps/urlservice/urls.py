# import os

# from django.conf import settings
# from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.views.static import serve

# from observer.apps.yqj.views import *
# from observer.apps.news.views import CategoryView, LocationView, NewsView, NewsDetailView
# from observer.apps.event.views import EventView, EventDetailView
# from observer.apps.risk.views import RisksView, RisksDetailView
# from observer.apps.weixin.views import WeixinView, WeixinDetailView
# from observer.apps.weibo.views import WeiboView
# from observer.apps.custom.views import CustomView, CustomDetailView
# from observer.apps.product.views import ProductView
# from observer.apps.inspection.views import InspectionView
# from observer.apps.search.views import SearchView
# from observer.apps.analytics.api import AnalyticsChildView

# urlpatterns = patterns(
#     'observer.apps.yqj.views',
#     url(r'^$', 'index_view'),
#     url(r'^person/$', 'person_view'),
#     url(r'^collection/$', CollectionView.as_view()),
#     url(r'^settings/$', SettingsView.as_view()),
#     url(r'^user/$', UserAdminView.as_view()),
#     url(r'^login/$', 'login_view'),
#     url(r'^logout/$', 'logout_view'),
# )

# urlpatterns += patterns(
#     'news.views',
#     url(r'^news/$', NewsView.as_view()),
#     url(r'^news/(\d+)/$', NewsDetailView.as_view()),
#     url(r'^category/(\d+)/$', CategoryView.as_view()),
#     url(r'^location/(\d+)/$', LocationView.as_view()),
# )

# urlpatterns += patterns(
#     'event.views',
#     url(r'^event/$', EventView.as_view()),
#     url(r'^event/(\d+)/$', EventDetailView.as_view()),
# )

# urlpatterns += patterns(
#     'risk.views',
#     url(r'^risk/$', RisksView.as_view()),
#     url(r'^risk/(\d+)/$', RisksDetailView.as_view()),
# )

# urlpatterns += patterns(
#     'weibo.views',
#     url(r'^weibo/$', WeiboView.as_view()),
# )
# urlpatterns += patterns(
#     'weixin.views',
#     url(r'^weixin/$', WeixinView.as_view()),
#     url(r'^weixin/(\d+)/$', WeixinDetailView.as_view()),
# )

# urlpatterns += patterns(
#     'custom.views',
#     url(r'^custom/$', CustomView.as_view()),
#     url(r'^custom/(\d+)/$', CustomDetailView.as_view()),
# )

# urlpatterns += patterns(
#     'product.views',
#     url(r'^product/(?P<id>\d*)/?$', ProductView.as_view()),
# )

# urlpatterns += patterns(
#     'inspection.views',
#     url(r'^inspection/$', InspectionView.as_view()),
# )

# urlpatterns += patterns(
#     'search.views',
#     url(r'^search/(.+)/$', SearchView.as_view()),
# )

# urlpatterns += patterns(
#     'analytics.api',
#     url(r'^analytics/(?P<id>\d+)/$', AnalyticsChildView.as_view()),
# )
