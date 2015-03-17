from django.conf.urls import patterns, include, url
from api.views import ArticleTableView, NewsTableView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yuqing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^category/(\d+)/$', ArticleTableView.as_view()),
    url(r'^news/$', NewsTableView.as_view()),
)
