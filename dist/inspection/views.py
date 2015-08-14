# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base.views import BaseTemplateView


class InspectionView(BaseTemplateView):
    def get(self, request):
        return self.render_to_response('inspection/inspection_list.html', {})
