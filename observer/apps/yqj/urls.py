from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from observer.apps.yqj.views import (NewsView, InspectionTableView, DashboardView, AnalyticsView)
	


urlpatterns = [
	url(r'^article$', NewsView.as_view()), 
	url(r'^inspection$', InspectionTableView.as_view()), 
	url(r'^dashboard$', DashboardView.as_view()),
	url(r'^analytics$', AnalyticsView.as_view()),
]
