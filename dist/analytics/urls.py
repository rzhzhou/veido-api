from django.conf.urls import patterns, include, url
from analytics.views import DispatchView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^analytics/(?P<id>\d*)/?$', DispatchView.as_view()),
)