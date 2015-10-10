# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from backend.base import sidebarUtil
from backend.base.views import BaseTemplateView


class SearchView(BaseTemplateView):
    def get(self, request, keyword):
    	sidebar_name = sidebarUtil(request)
        return self.render_to_response('search/result.html',{'name': sidebar_name})
