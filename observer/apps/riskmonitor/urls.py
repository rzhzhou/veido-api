from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from observer.apps.riskmonitor.views import (Analytics, AnalyticsExport,
                                             DashboardList, EnterpriseList,
                                             Filters, GenerateAnalyticsExport,
                                             IndustryDetail, IndustryList,
                                             NewsDetail, NewsList)

urlpatterns = [
    url(r'^dashboards$', DashboardList.as_view()),
    url(r'^industries$', IndustryList.as_view()),
    url(r'^industries/(?P<pk>[0-9]+)$', IndustryDetail.as_view()),
    url(r'^news$', NewsList.as_view()),
    url(r'^news/(?P<pk>[0-9]+)$', NewsDetail.as_view()),
    url(r'^enterprises$', EnterpriseList.as_view()),
    url(r'^analytics$', Analytics.as_view()),
    url(r'^analytics/filters$', Filters.as_view()),
    url(r'^analytics/export$', GenerateAnalyticsExport.as_view()),
]

urlpatterns += [
    url(r'^files/(?P<filename>[a-z]+)$', AnalyticsExport.as_view()),
]
