from django.conf.urls import patterns, include, url
from api.views import ArticleTableView, NewsTableView, LocationTableView, CollectView, EventTableView,\
                      CollecModifyView, EventDetailTableView, SearchView, CustomTableView, InspectionTableView,\
                      WeixinTableView, WeiboTableView, LocationWeixinView, LocationWeiboView, EventDetailWeixinView,\
                      EventDetailWeiboView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^category/(\d+)/$', ArticleTableView.as_view()),
    url(r'^location/(?P<location_id>\d+)/weixin/new/(?P<page>\d+)/$', LocationWeixinView.as_view()),
    url(r'^location/(?P<location_id>\d+)/weibo/new/(?P<page>\d+)/$', LocationWeiboView.as_view()),
    url(r'^location/(\d+)/$', LocationTableView.as_view()),
    url(r'^news/$', NewsTableView.as_view()),
    url(r'^collection/$', CollectView.as_view()),
    url(r'^event/$', EventTableView.as_view()),
    url(r'^event/(\d+)/$', EventDetailTableView.as_view()),
    url(r'^event/(?P<id>\d+)/weixin/new/(?P<page>\d+)/$', EventDetailWeixinView.as_view()),
    url(r'^event/(?P<id>\d+)/weibo/new/(?P<page>\d+)/$', EventDetailWeiboView.as_view()),
    url(r'^search/(\S+)/$', SearchView.as_view()),
    url(r'^collection/(?P<action>\w+)/$', CollecModifyView.as_view()),
    #url(r'^collection/add/$', CollecModifyView.as_view()),
    url(r'^custom/(\d+)/$', CustomTableView.as_view()),
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
