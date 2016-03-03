from django.conf.urls import include, url
from rest_framework_jwt import views

from observer.apps.analytics.api import DispatchView
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
from observer.apps.risk.api import chart_line_risk_view, chart_pie_risk_view
from observer.apps.weixin.api import WeixinView, LocationWeixinView, WeixinDetailView
from observer.apps.weibo.api import WeiboView, LocationWeiboView
from observer.apps.yqj.api import login_view, registe_view, upload_image, change_passwd,\
    reset_passwd, delete_user_view, add_user_view, chart_line_index_view,\
<<<<<<< HEAD
    chart_pie_index_view, map_view, Sidebar, Dashboard, logout_view, ObtainJSONWebToken
from observer.apps.riskmonitor.api import HomePageView, IndustryTrackView
=======
    chart_pie_index_view, map_view, Sidebar, Dashboard, logout_view
>>>>>>> 82623ee8e0925ff26d3098d03d29857d103c81fb


urlpatterns = [
    url(r'^token-auth$', views.obtain_jwt_token),
    url(r'^token-refresh$', views.refresh_jwt_token),
    url(r'^token-verify$', views.verify_jwt_token),
]

urlpatterns += [
    url(r'^category/(?P<id>\d+)/news/$', ArticleTableView.as_view()),
    url(r'^location/(?P<id>\d+)/news/$', LocationTableView.as_view()),
    url(r'^news$', NewsView.as_view()),
    url(r'^news/(\d+)$', NewsDetailView.as_view()),
]

urlpatterns += [
    url(r'^event/(?P<id>\d+)$', EventDetailsView.as_view()),
    url(r'^event$', EventTableView.as_view()),
]

urlpatterns += [
    url(r'^risk/$', RisksView.as_view()),
    url(r'^risk/(?P<id>\d+)/news/$', RisksNewsView.as_view()),
    url(r'^risk/(?P<id>\d+)/weixin/$', RisksWeixinView.as_view()),
    url(r'^risk/(?P<id>\d+)/weibo/$', RisksWeiboView.as_view()),
    url(r'^line/risk/(\d+)/$', chart_line_risk_view),
    url(r'^pie/risk/(\d+)/$', chart_pie_risk_view),
]

urlpatterns += [
    url(r'^weibo/$', WeiboView.as_view()),
    url(r'^location/(?P<id>\d+)/weibo/$', LocationWeiboView.as_view()),
]

urlpatterns += [
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^weixin/(?P<id>\d+)$', WeixinDetailView.as_view()),
    url(r'^location/(?P<id>\d+)/weixin/$', LocationWeixinView.as_view()),
]

urlpatterns += [
    url(r'^custom/(?P<custom_id>\d+)/news/$', CustomNewsView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weixin/$', CustomWeixinView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weibo/$', CustomWeiboView.as_view()),
    url(r'^custom/(?P<action>\w+)/$', CustomModifyView.as_view()),
]

urlpatterns += [
    url(r'^product/(?P<id>\d*)/?news/(?P<page>\d+)/$', ProductTableView.as_view()),
]

urlpatterns += [
    url(r'^inspection$', InspectionTableView.as_view()),
    url(r'^dashboard/local-inspection/$', InspectionLocalView.as_view()),
    url(r'^dashboard/national-inspection/$', InspectionNationalView.as_view()),
]

urlpatterns += [
    url(r'^search/(.+)/$', SearchView.as_view()),
]

urlpatterns += [
    url(r'^analytics/(?P<id>\d+)/$', DispatchView.as_view()),
]

urlpatterns += [
    url(r'^collection$', CollecModifyView.as_view()),
    url(r'^collection/(?P<table_type>\S+)/$', CollectView.as_view()),
]

urlpatterns += [
    url(r'^login/$', login_view),
    url(r'^token-revoke$', logout_view),
    url(r'^register/$', registe_view),
    url(r'^settings/upload/$', upload_image),
    url(r'^settings/change/$', change_passwd),
    url(r'^user/reset/$', reset_passwd),
    url(r'^user/remove/$', delete_user_view),
    url(r'^user/add/$', add_user_view),

    url(r'^line/$', chart_line_index_view),
    url(r'^pie/$', chart_pie_index_view),
    url(r'^map/$', map_view),
    url(r'^app$', Sidebar.as_view()),
    url(r'^dashboard$', Dashboard.as_view()),
    url(r'^token-auth$', ObtainJSONWebToken.as_view()),
]

urlpatterns += [
    url(r'^dashboard/$', HomePageView.as_view()),
    url(r'^industry/$', IndustryTrackView.as_view())
]
