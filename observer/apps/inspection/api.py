# -*- coding: utf-8 -*-
import pytz

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base import read_redis
from observer.apps.base.views import BaseAPIView
from observer.apps.base.models import Inspection
from observer.apps.yqj.redisconnect import RedisQueryApi

class InspectionTableView(BaseAPIView):
    def get(self, request):
        container = self.requesthead(limit_list=settings.EVENT_PAGE_LIMIT)
        items = Inspection.objects.exclude(qualitied__lt=0).order_by('-pubtime')
        datas = self.paging(items, container['limit'], container['page'])
        result = self.inspection_to_json(datas['items'])
        html_string = render_to_string('inspection/list_tpl.html', {'inspection_list':  result})
        return Response({'total': datas['total_number'], 'html': html_string})


class InspectionLocalView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def get(self, request):
        parameter = request.GET
        catch = int(parameter['catch']) if parameter.has_key('catch') else 1
        try:
            data = None
            if catch:
                data = RedisQueryApi().hget('inspection', 'abstract')
                if data:
                    return HttpResponse(data)
            user = request.myuser
            company = user.group.company
            inspection_list = Inspection.objects.exclude(qualitied__lt=0).filter(
                source=company).order_by('-pubtime')[:self.HOME_PAGE_LIMIT]

            tz = pytz.timezone(settings.TIME_ZONE)
            for item in inspection_list:
                timel = item.pubtime.astimezone(tz)
                item.pubtime = timel
                item.qualitied = str(int(item.qualitied * 100)) + '%'

            inspection = render_to_string('inspection/abstract.html', {'inspection_list': inspection_list})
            return HttpResponse(inspection)
        except:
            return Response({})


class InspectionNationalView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def get(self, request):
        user = request.myuser
        user.company = user.group.company
        inspection_list = Inspection.objects.exclude(
            qualitied__lt=0).all().order_by('-pubtime')[:self.HOME_PAGE_LIMIT]

        tz = pytz.timezone(settings.TIME_ZONE)
        for item in inspection_list:
            timel = item.pubtime.astimezone(tz)
            item.pubtime = timel
            item.qualitied = str(int(item.qualitied * 100)) + '%'

        inspection = render_to_string('inspection/abstract.html', {'inspection_list': inspection_list})
        return HttpResponse(inspection)

