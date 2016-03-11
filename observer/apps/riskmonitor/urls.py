from django.conf.urls import url

from observer.apps.riskmonitor.views import (
    HomePageView, IndustryList, IndustryDetail, NewsList, NewsDetail,
    EnterpriseList, Analytics, AnalyticsExport)


urlpatterns = [
    url(r'^dashboards$', HomePageView.as_view()),
    url(r'^industries$', IndustryList.as_view()),
    url(r'^industries/(?P<pk>[0-9]+)$', IndustryDetail.as_view()),
    url(r'^news$', NewsList.as_view()),
    url(r'^news/(?P<pk>[0-9]+)$', NewsDetail.as_view()),
    url(r'^enterprises$', EnterpriseList.as_view()),
    url(r'^analytics$', Analytics.as_view()),
    url(r'^analytics/export$', AnalyticsExport.as_view()),
]
