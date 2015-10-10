from django.conf.urls import patterns, include, url

from backend.collection.views_api import CollectView, CollecModifyView
from backend.custom.views_api import CustomWeixinView, CustomWeiboView, \
    CustomModifyView, CustomNewsView
from backend.event.views_api import EventView, EventNewsView, \
    EventWeixinView, EventWeiboView
from backend.inspection.views_api import InspectionTableView, InspectionLocalView, \
    InspectionNationalView
from backend.news.views_api import LocationTableView, NewsView, ArticleTableView
from backend.risk.views_api import RisksView, RisksNewsView,\
    RisksWeixinView, RisksWeiboView
from backend.product.views_api import ProductTableView
from backend.search.views_api import SearchView
from backend.weixin.views_api import WeixinView, LocationWeixinView
from backend.weibo.views_api import WeiboView, LocationWeiboView
from backend.analytics.views import DispatchView
from backend.yqj.views_api import login_view, registe_view, upload_image, change_passwd,\
    reset_passwd, delete_user_view, add_user_view, chart_line_index_view,\
    chart_pie_index_view, map_view


urlpatterns = patterns('news.views_api',
    url(r'^category/(?P<id>\d+)/news/$', ArticleTableView.as_view()),
    url(r'^location/(?P<id>\d+)/news/$', LocationTableView.as_view()),
    url(r'^news/$', NewsView.as_view()),
)

urlpatterns += patterns('event.views_api',
    url(r'^event/$', EventView.as_view()),
    url(r'^event/(?P<id>\d+)/news/$', EventNewsView.as_view()),
    url(r'^event/(?P<id>\d+)/weixin/$', EventWeixinView.as_view()),
    url(r'^event/(?P<id>\d+)/weibo/$', EventWeiboView.as_view()),
    url(r'^line/event/(\d+)/$', 'chart_line_event_view'),
    url(r'^pie/event/(\d+)/$', 'chart_pie_event_view'),
)

urlpatterns += patterns('risk.views_api',
    url(r'^risk/$', RisksView.as_view()),
    url(r'^risk/(?P<id>\d+)/news/$', RisksNewsView.as_view()),
    url(r'^risk/(?P<id>\d+)/weixin/$', RisksWeixinView.as_view()),
    url(r'^risk/(?P<id>\d+)/weibo/$', RisksWeiboView.as_view()),
    url(r'^line/risk/(\d+)/$', 'chart_line_risk_view'),
    url(r'^pie/risk/(\d+)/$', 'chart_pie_risk_view'),
)

urlpatterns += patterns('weibo.views_api',
    url(r'^weibo/$', WeiboView.as_view()),
    url(r'^location/(?P<id>\d+)/weibo/$', LocationWeiboView.as_view()),
)
urlpatterns += patterns('weixin.views_api',
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^location/(?P<id>\d+)/weixin/$', LocationWeixinView.as_view()),
)

urlpatterns += patterns('custom.views_api',
    url(r'^custom/(?P<custom_id>\d+)/news/$', CustomNewsView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weixin/$', CustomWeixinView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weibo/$', CustomWeiboView.as_view()),
    url(r'^custom/(?P<action>\w+)/$', CustomModifyView.as_view()),
)

urlpatterns += patterns('product.views_api',
    url(r'^product/(?P<id>\d*)/?news/(?P<page>\d+)/$', ProductTableView.as_view()),
)

urlpatterns += patterns('inspection.views_api',
    url(r'^inspection/$', InspectionTableView.as_view()),
    url(r'^dashboard/local-inspection/$', InspectionLocalView.as_view()),
    url(r'^dashboard/national-inspection/$', InspectionNationalView.as_view()),
)

urlpatterns += patterns('search.views_api',
    url(r'^search/(.+)/$', SearchView.as_view()),
)

urlpatterns += patterns('analytics.views',
    url(r'^analytics/(?P<id>\d+)/$', DispatchView.as_view()),
)

urlpatterns += patterns('collection,views_api',
    url(r'^collection/$', CollecModifyView.as_view()),
    url(r'^collection/(?P<table_type>\S+)/$', CollectView.as_view()),
)

urlpatterns += patterns('yqj.views_api',
    url(r'^login/$', 'login_view'),
    url(r'^register/$', 'registe_view'),
    url(r'^settings/upload/$', 'upload_image'),
    url(r'^settings/change/$', 'change_passwd'),
    url(r'^user/reset/$', 'reset_passwd'),
    url(r'^user/remove/$', 'delete_user_view'),
    url(r'^user/add/$', 'add_user_view'),

    url(r'^line/$', 'chart_line_index_view'),
    url(r'^pie/$', 'chart_pie_index_view'),
    url(r'^map/$', 'map_view'),
)
