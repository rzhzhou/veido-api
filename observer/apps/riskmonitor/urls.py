from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from observer.apps.riskmonitor.views import (Analytics, AnalyticsExport,
                                             DashboardList, EnterpriseList,
                                             EnterpriseDetail, Filters,
                                             IndustryDetail, IndustryList,
                                             NewsDetail, NewsList, RiskNewsList,
                                             RiskNewsRecycleList,
                                             RiskNewsRecycle, RiskNewsRestore, RiskNewsDelete, 
                                             InspectionList, Search, SearchIndustry, 
                                             SearchPublisher, AdministrativePenaltieList)

urlpatterns = [
    url(r'^dashboards$', DashboardList.as_view()),
    url(r'^industries$', IndustryList.as_view()),
    url(r'^industries/(?P<pk>[0-9]+)$', IndustryDetail.as_view()),
    url(r'^news$', NewsList.as_view()),
    url(r'^news/(?P<pk>[0-9]+)$', NewsDetail.as_view()),
    url(r'^risknews$', RiskNewsList.as_view()),
    url(r'^risknews_list$', RiskNewsRecycleList.as_view()),
    url(r'^risknews_recycle$', RiskNewsRecycle.as_view()),
    url(r'^risknews_restore$', RiskNewsRestore.as_view()),
    url(r'^risknews_delete$', RiskNewsDelete.as_view()),
    url(r'^inspection$', InspectionList.as_view()),
    url(r'^enterprises$', EnterpriseList.as_view()),
    url(r'^enterprises/(?P<pk>[0-9]+)$', EnterpriseDetail.as_view()),
    url(r'^analytics$', Analytics.as_view()),
    url(r'^analytics/filters$', Filters.as_view()),
    url(r'^search$', Search.as_view()),
    url(r'^industries2$', SearchIndustry.as_view()),
    url(r'^publishers$', SearchPublisher.as_view()),
    url(r'^administrativepenalties$', AdministrativePenaltieList.as_view()),
]

urlpatterns += [
    url(r'^files/(?P<filename>[a-z]+)$', AnalyticsExport.as_view()),
]
