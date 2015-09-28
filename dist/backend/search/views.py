# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base import sidebarUtil
from base.views import BaseTemplateView


class SearchView(BaseTemplateView):
    def get(self, request, keyword):
    	sidebar_name = sidebarUtil(request)
        return self.render_to_response('search/result.html',{'name': sidebar_name})
