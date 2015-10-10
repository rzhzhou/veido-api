# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from observer.apps.base import sidebarUtil
from observer.apps.base.views import BaseTemplateView


class SearchView(BaseTemplateView):
    def get(self, request, keyword):
    	sidebar_name = sidebarUtil(request)
        return self.render_to_response('search/result.html',{'name': sidebar_name})
