# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from observer.apps.base import sidebarUtil
from observer.apps.base.views import BaseTemplateView


class InspectionView(BaseTemplateView):
    def get(self, request):
    	sidebar_name = sidebarUtil(request)
        return self.render_to_response('inspection/list.html', {'name': sidebar_name})
