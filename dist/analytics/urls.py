from django.conf.urls import patterns, include, url
from views import LineTableView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^analytics/charts/(?P<id>\d+)/$', LineTableView.as_view()),
)