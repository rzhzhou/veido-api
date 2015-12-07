from django.conf.urls import patterns, include, url

from observer.apps.collection.api import CollectView, CollecModifyView
from observer.apps.custom.api import CustomWeixinView, CustomWeiboView, \
    CustomModifyView, CustomNewsView
from observer.apps.event.api import EventDetailsView, EventTableView
from observer.apps.inspection.api import InspectionTableView, InspectionLocalView, \
    InspectionNationalView
from observer.apps.news.api import LocationTableView, NewsView, ArticleTableView, NewsDetailView
from observer.apps.risk.api import RisksView, RisksNewsView,\
    RisksWeixinView, RisksWeiboView
from observer.apps.product.api import ProductTableView
from observer.apps.search.api import SearchView
from observer.apps.weixin.api import WeixinView, LocationWeixinView, WeixinDetailView
from observer.apps.weibo.api import WeiboView, LocationWeiboView
from observer.apps.analytics.api import DispatchView
from observer.apps.yqj.api import login_view, registe_view, upload_image, change_passwd,\
    reset_passwd, delete_user_view, add_user_view, chart_line_index_view,\
    chart_pie_index_view, map_view, Sidebar, Dashboard, logout_view


urlpatterns = patterns(
    '',
    url(r'^token-auth$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^token-refresh$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^token-verify$', 'rest_framework_jwt.views.verify_jwt_token'),
)

urlpatterns += patterns(
    'observer.apps.news.api',
    url(r'^category/(?P<id>\d+)/news/$', ArticleTableView.as_view()),
    url(r'^location/(?P<id>\d+)/news/$', LocationTableView.as_view()),
    url(r'^news$', NewsView.as_view()),
    url(r'^news/(\d+)$', NewsDetailView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.event.api',
    url(r'^event/(?P<id>\d+)$', EventDetailsView.as_view()),
    url(r'^event$', EventTableView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.risk.api',
    url(r'^risk/$', RisksView.as_view()),
    url(r'^risk/(?P<id>\d+)/news/$', RisksNewsView.as_view()),
    url(r'^risk/(?P<id>\d+)/weixin/$', RisksWeixinView.as_view()),
    url(r'^risk/(?P<id>\d+)/weibo/$', RisksWeiboView.as_view()),
    url(r'^line/risk/(\d+)/$', 'chart_line_risk_view'),
    url(r'^pie/risk/(\d+)/$', 'chart_pie_risk_view'),
)

urlpatterns += patterns(
    'observer.apps.weibo.api',
    url(r'^weibo/$', WeiboView.as_view()),
    url(r'^location/(?P<id>\d+)/weibo/$', LocationWeiboView.as_view()),
)
urlpatterns += patterns(
    'observer.apps.weixin.api',
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^weixin/(?P<id>\d+)$', WeixinDetailView.as_view()),
    url(r'^location/(?P<id>\d+)/weixin/$', LocationWeixinView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.custom.api',
    url(r'^custom/(?P<custom_id>\d+)/news/$', CustomNewsView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weixin/$', CustomWeixinView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weibo/$', CustomWeiboView.as_view()),
    url(r'^custom/(?P<action>\w+)/$', CustomModifyView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.product.api',
    url(r'^product/(?P<id>\d*)/?news/(?P<page>\d+)/$', ProductTableView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.inspection.api',
    url(r'^inspection$', InspectionTableView.as_view()),
    url(r'^dashboard/local-inspection/$', InspectionLocalView.as_view()),
    url(r'^dashboard/national-inspection/$', InspectionNationalView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.search.api',
    url(r'^search/(.+)/$', SearchView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.analytics.api',
    url(r'^analytics/(?P<id>\d+)/$', DispatchView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.collection,api',
    url(r'^collection$', CollecModifyView.as_view()),
    url(r'^collection/(?P<table_type>\S+)/$', CollectView.as_view()),
)

urlpatterns += patterns(
    'observer.apps.yqj.api',
    url(r'^login/$', 'login_view'),
    url(r'^token-revoke$', 'logout_view'),
    url(r'^register/$', 'registe_view'),
    url(r'^settings/upload/$', 'upload_image'),
    url(r'^settings/change/$', 'change_passwd'),
    url(r'^user/reset/$', 'reset_passwd'),
    url(r'^user/remove/$', 'delete_user_view'),
    url(r'^user/add/$', 'add_user_view'),

    url(r'^line/$', 'chart_line_index_view'),
    url(r'^pie/$', 'chart_pie_index_view'),
    url(r'^map/$', 'map_view'),
    url(r'^app$', Sidebar.as_view()),
    url(r'^dashboard$', Dashboard.as_view()),
)
