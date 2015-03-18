from django.conf.urls import patterns, include, url
from api.views import ArticleTableView, NewsTableView, LocationTableView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^category/(\d+)/$', ArticleTableView.as_view()),
    url(r'^location/(\d+)/$', LocationTableView.as_view()),
    url(r'^news/$', NewsTableView.as_view()),
    url(r'^login/$', 'login_view'),
)
