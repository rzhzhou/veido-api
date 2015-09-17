# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from base import sidebarUtil
from base.views import BaseTemplateView
from base.models import Risk


class RisksView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('risk/list.html', {"name": sidebar_name})

class RisksDetailView(BaseTemplateView):

    def get(self, request, risk_id):
        sidebar_name = sidebarUtil(request)

        try:
            risk = Risk.objects.get(id=int(risk_id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        eval_keywords_list = eval(risk.keywords) if risk.keywords else []
        keywords_list = [{"name": name, "number": number} for name, number in eval_keywords_list]

        return self.render_to_response('risk/detail.html',
            {'risk': risk, 'keywords_list': keywords_list, 'name': sidebar_name})
