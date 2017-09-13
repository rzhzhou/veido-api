#-*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from observer.apps.yqj.views import (NewsView, RiskView,EventView,
	InspectionTableView, DashboardView)


urlpatterns = [
	url(r'^article$', NewsView.as_view()), 
	url(r'^event$', EventView.as_view()), 
	url(r'^risknews$',RiskView.as_view()), 
	url(r'^inspection$', InspectionTableView.as_view()), 
	url(r'^dashboard$', DashboardView.as_view()),
]
