# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base import sidebarUtil
from base.views import BaseTemplateView


class InspectionView(BaseTemplateView):
    def get(self, request):
    	sidebar_name = sidebarUtil(request)
        return self.render_to_response('inspection/inspection_list.html', {'name': sidebar_name})
