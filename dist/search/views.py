# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base.views import BaseTemplateView


class SearchView(BaseTemplateView):
    def get(self, request, keyword):
        return self.render_to_response('search/result.html')
