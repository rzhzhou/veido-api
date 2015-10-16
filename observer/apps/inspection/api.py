# -*- coding: utf-8 -*-
import pytz

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base.views import BaseAPIView
from observer.apps.base.models import Inspection


class InspectionTableView(BaseAPIView):
    def get(self, request):
<<<<<<< HEAD
        container = self.requestContainer(limit_list=settings.EVENT_PAGE_LIMIT)
        items = Inspection.objects.exclude(qualitied__lt=0).order_by('-pubtime')
        datas = self.paging(items, container['limit'], container['page'])
        result = self.inspection_to_json(datas['items'])
        html_string = render_to_string('inspection/list_tpl.html', {'inspection_list':  result})
        return Response({'total': datas['total_number'], 'html': html_string})
=======
        result = []
        news = Inspection.objects.exclude(qualitied__lt=0).order_by('-pubtime').all()

        for item in news:
            title = self.title_html(item.url, item.name, item.id, 'inspection')
            quality = str(int(item.qualitied * 100)) + '%'
            tz = pytz.timezone(settings.TIME_ZONE)
            timel = item.pubtime.astimezone(tz)

            one_record = [item.product, title, quality, item.source, timel.strftime('%Y-%m-%d')]
            result.append(one_record)

        return Response({"inspection": result})

    def inspection_to_json(self, items):
        result = []
        for data in items:
            item = {}
            item['title'] = data.name
            item['source'] = data.source
            item['category'] = data.product
            item['quality'] = str(data.qualitied * 100)[:4] + "%"
            item['time'] = data.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d')
            item['source'] = data.source
            result.append(item)
        return result
>>>>>>> master


class InspectionLocalView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def get(self, request):
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

<<<<<<< HEAD
        inspection = render_to_string('inspection/abstract.html', {'inspection_list': inspection_list})
        return HttpResponse(inspection)
=======
        inspection = render_to_string('inspection/dashboard_inspection.html', {
            'inspection_list': inspection_list})
        return HttpResponse(inspection)
>>>>>>> master
