from django.conf.urls import patterns, include, url
from analytics.views import PieTypeTableView, PieFeelingTableView, PieAreaTableView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^analytics/chart-type/',PieTypeTableView.as_view()),
    url(r'^analytics/chart-emotion/(?P<id>\d+)/$',PieFeelingTableView.as_view()),
    url(r'^analytics/chart-weibo/(?P<id>\d+)/$',PieAreaTableView.as_view()),

)