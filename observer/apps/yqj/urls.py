from django.conf.urls import url

from observer.apps.yqj.views import (ArticleView, EventView,ReferenceView,
	InsightView,RiskView,InspectionView,CategoryView)


urlpatterns = [
    url(r'^article$', ArticleView.as_view()),
    url(r'^event$', EventView.as_view()),
    url(r'^reference$', ReferenceView.as_view()),
    url(r'^insight$', ReferenceView.as_view()),
    url(r'^risk$', RiskView.as_view()),
    url(r'^inspection$', InspectionView.as_view()),
    url(r'^category/(?P<id>\d+)$', CategoryView.as_view()),
    url(r'^area/(?P<id>\d+)$', CategoryView.as_view()),
]
