from django.conf.urls import url

from observer.apps.yqj.views import (ArticleView, )


urlpatterns = [
    url(r'^article$', ArticleView.as_view()),
]
