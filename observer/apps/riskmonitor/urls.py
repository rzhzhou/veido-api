from django.conf.urls import url

from observer.apps.riskmonitor.views import (
    HomePageView, IndustryTrackView, EnterpriseRankView, StatisticView,
    DetailNewsView, SpeciesView, StatisticExportView)


urlpatterns = [
    url(r'^dashboard$', HomePageView.as_view()),
    url(r'^species$', SpeciesView.as_view()),
    url(r'^industry/(?P<pk>[0-9]+)$', IndustryTrackView.as_view()),
    url(r'^enterprise$', EnterpriseRankView.as_view()),
    url(r'^statistical$', StatisticView.as_view()),
    url(r'^statistical/export$', StatisticExportView.as_view()),
    url(r'^news$', DetailNewsView.as_view()),
]
