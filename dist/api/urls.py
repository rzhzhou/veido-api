from django.conf.urls import patterns, include, url
from api.views import ArticleTableView, NewsTableView, LocationTableView, CollectView, EventTableView,\
                      CollecModifyView, EventDetailTableView, SearchView, CustomTableView, InspectionTableView,\
                      WeixinTableView, WeiboTableView, LocationWeixinView, LocationWeiboView, EventDetailWeixinView,\
                      EventDetailWeiboView, CustomWeixinView, CustomWeiboView, CustomModifyView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^category/(?P<id>\d+)/news/(?P<page>\d+)/$', ArticleTableView.as_view()),
    url(r'^location/(?P<location_id>\d+)/weixin/new/(?P<page>\d+)/$', LocationWeixinView.as_view()),
    url(r'^location/(?P<location_id>\d+)/weibo/new/(?P<page>\d+)/$', LocationWeiboView.as_view()),
    url(r'^location/(?P<location_id>\d+)/news/(?P<page>\d+)/$', LocationTableView.as_view()),
    url(r'^news/news/(?P<page>\d+)/$', NewsTableView.as_view()),
    url(r'^collection/(?P<table_type>\S+)/(?P<page>\d+)/$', CollectView.as_view()),
    url(r'^event/event/(?P<page>\d+)/$', EventTableView.as_view()),
    url(r'^event/(?P<id>\d+)/news/(?P<page>\d+)/$', EventDetailTableView.as_view()),
    url(r'^event/(?P<id>\d+)/weixin/new/(?P<page>\d+)/$', EventDetailWeixinView.as_view()),
    url(r'^event/(?P<id>\d+)/weibo/new/(?P<page>\d+)/$', EventDetailWeiboView.as_view()),
    url(r'^search/(.+)/$', SearchView.as_view()),
    url(r'^collection/(?P<action>\w+)/$', CollecModifyView.as_view()),
    #url(r'^collection/add/$', CollecModifyView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/news/(?P<page>\d+)/$', CustomTableView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weixin/new/(?P<page>\d+)/$', CustomWeixinView.as_view()),
    url(r'^custom/(?P<custom_id>\d+)/weibo/new/(?P<page>\d+)/$', CustomWeiboView.as_view()),
    url(r'^custom/(?P<action>\w+)/$', CustomModifyView.as_view()),
    # url(r'^product/(?P<id>\d+)/news/(?P<page>\d+)/$', ProductTableView.as_view()),
    #url(r'^inspection/inspection/(?P<page>\d+)/$', InspectionTableView.as_view()),
    url(r'^inspection/$', InspectionTableView.as_view()),
    url(r'^weixin/(?P<weixin_type>\w+)/(?P<page>\d+)/$', WeixinTableView.as_view()),
    url(r'^weibo/(?P<weibo_type>\w+)/(?P<page>\d+)/$', WeiboTableView.as_view()),
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
    url(r'^line/event/(\d+)/$', 'chart_line_event_view'),
    url(r'^pie/event/(\d+)/$', 'chart_pie_event_view'),
    )
