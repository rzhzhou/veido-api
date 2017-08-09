# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from observer.apps.yqj.views import (NewsView, RiskView,EventView,
	InspectionTableView )


urlpatterns = [
	url(r'^news$', NewsView.as_view()), #质监热点
	url(r'^event$', EventView.as_view()), #质量事件
	url(r'^risknews$',RiskView.as_view()), #风险快讯
	url(r'^inspection/$', InspectionTableView.as_view()), #抽检信息
]