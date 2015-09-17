from django.conf.urls import patterns, include, url
from api.views import (ArticleTableView, CollectView, CollecModifyView,
    CustomNewsView, CustomWeixinView, CustomWeiboView, CustomModifyView,
    EventView, EventNewsView, EventWeixinView, EventWeiboView,
    InspectionTableView, InspectionLocalView, InspectionNationalView,
    LocationTableView, LocationWeixinView, LocationWeiboView, NewsView,
    ProductTableView, RisksView, RisksNewsView, RisksWeixinView, RisksWeiboView,
    SearchView, WeixinView, WeiboView)


urlpatterns = patterns('',
    url(r'^category/(?P<id>\d+)/news/(?P<page>\d+)/$', ArticleTableView.as_view()),
    url(r'^location/(?P<location_id>\d+)/weixin/new/(?P<page>\d+)/$', LocationWeixinView.as_view()),
    url(r'^location/(?P<location_id>\d+)/weibo/new/(?P<page>\d+)/$', LocationWeiboView.as_view()),
    url(r'^location/(?P<location_id>\d+)/news/(?P<page>\d+)/$', LocationTableView.as_view()),
    url(r'^news/$', NewsView.as_view()),
    url(r'^collection/(?P<table_type>\S+)/(?P<page>\d+)/$', CollectView.as_view()),

    url(r'^risk/$', RisksView.as_view()),
    url(r'^risk/(?P<id>\d+)/news/$', RisksNewsView.as_view()),
    url(r'^risk/(?P<id>\d+)/weixin/$', RisksWeixinView.as_view()),
    url(r'^risk/(?P<id>\d+)/weibo/$', RisksWeiboView.as_view()),

    url(r'^event/$', EventView.as_view()),
    url(r'^event/(?P<id>\d+)/news/$', EventNewsView.as_view()),
    url(r'^event/(?P<id>\d+)/weixin/$', EventWeixinView.as_view()),
    url(r'^event/(?P<id>\d+)/weibo/$', EventWeiboView.as_view()),

    url(r'^search/(.+)/$', SearchView.as_view()),
    url(r'^collection/(?P<action>\w+)/$', CollecModifyView.as_view()),
    #url(r'^collection/add/$', CollecModifyView.as_view()),

    url(r'^custom/(?P<custom_id>\d+)/news/$', CustomNewsView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weixin/$', CustomWeixinView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weibo/$', CustomWeiboView.as_view()),
    url(r'^custom/(?P<action>\w+)/$', CustomModifyView.as_view()),

    url(r'^product/(?P<id>\d*)/?news/(?P<page>\d+)/$', ProductTableView.as_view()),
    #url(r'^inspection/inspection/(?P<page>\d+)/$', InspectionTableView.as_view()),
    url(r'^inspection/$', InspectionTableView.as_view()),
    url(r'^dashboard/local-inspection/$', InspectionLocalView.as_view()),
    url(r'^dashboard/national-inspection/$', InspectionNationalView.as_view()),
    url(r'^weixin/$', WeixinView.as_view()),
    url(r'^weibo/$', WeiboView.as_view()),
)

urlpatterns += patterns('api.views',
    url(r'^login/$', 'login_view'),
    url(r'^register/$', 'registe_view'),
    url(r'^settings/upload/$', 'upload_image'),
    url(r'^settings/change/$', 'change_passwd'),


    url(r'^user/reset/$', 'reset_passwd'),
    url(r'^user/remove/$', 'delete_user_view'),
    url(r'^user/add/$', 'add_user_view'),

    url(r'^line/$', 'chart_line_index_view'),
    url(r'^pie/$', 'chart_pie_index_view'),
    url(r'^line/risk/(\d+)/$', 'chart_line_risk_view'),
    url(r'^pie/risk/(\d+)/$', 'chart_pie_risk_view'),
    url(r'^line/event/(\d+)/$', 'chart_line_event_view'),
    url(r'^pie/event/(\d+)/$', 'chart_pie_event_view'),
    url(r'^map/$', 'map_view'),
    )
