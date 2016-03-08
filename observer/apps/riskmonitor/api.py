# -*- coding: utf-8 -*-
from tests import test_tools
test_tools()
import pytz
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

from observer.apps.base.views import BaseTemplateView
from observer.apps.riskmonitor.models import RiskNews
from observer.apps.riskmonitor.businesslogic.abstract import Abstract
from observer.apps.base.initialize import xls_to_response
from observer.utils.excel.briefing import article
from businesslogic.detail import *
from businesslogic.enterprise import EnterpriseRank
from businesslogic.homepage import *
from businesslogic.industry import IndustryTrack
from businesslogic.statistic import Statistic


class HomePageView(APIView, BaseTemplateView):

    def get(self, request):
        start = request.GET.get('start', '2015-11-22')
        end = request.GET.get('start', '2015-11-30')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        data = HomeData(start, end).get_all()
        return Response(data)


class IndustryTrackView(APIView):

    def get(self, request, pk):
        page = request.GET.get('page', 1)
        start = request.GET.get('start', '2015-11-22')
        end = request.GET.get('end', '2015-11-30')
        dtype = request.GET.get('type', '')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        if dtype == 'table':
            data = IndustryTrack(industry=pk, start=start,
                                 end=end, page=page).news_data()
        else:
            data = IndustryTrack(industry=pk, start=start,
                                 end=end, page=page).get_chart()
        return Response(data)


class IndustryDataDetail(APIView):

    def get(self, request, pk):
        page = request.GET.get('page', 1)
        start = request.GET.get('start', '2015-11-22')
        end = request.GET.get('start', '2015-11-30')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))
        return Response(data)


class EnterpriseRankView(APIView):

    def get(self, request):
        pk = request.GET.get('industry', 0)
        page = request.GET.get('page', 1)
        start = request.GET.get('start', '2015-11-22')
        end = request.GET.get('start', '2015-11-30')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        data = EnterpriseRank(industry=int(pk), start=start, end=end,
                              page=int(page)).get_all()
        return Response(data)


class StatisticView(APIView):

    def get(self, request):
        pk = request.GET.get('industry', 0)
        page = request.GET.get('page', 1)
        start = request.GET.get('start', '2015-11-22')
        end = request.GET.get('start', '2015-11-30')
        dtype = request.GET.get('type', '')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        if dtype == 'table':
            data = Statistic(industry=pk, start=start,
                             end=end, page=page).get_data()
            return Response(data)
        else:
            data = Statistic(industry=pk, start=start,
                             end=end, page=page).get_chart()
            return Response(data)


class StatisticExportView(View):

    def get(self, request):
        pk = request.GET.get('industry', 0)
        page = request.GET.get('page', 1)
        start = request.GET.get('start', '2015-11-22')
        end = request.GET.get('start', '2015-11-30')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        data = Statistic(industry=pk, start=start,
                         end=end, page=page).get_all()
        brief = article()
        output = brief.get_output(data)
        print output
        output.seek(0)
        response = HttpResponse(output.read(
        ), content_type='application/ms-excel')
        response['Content-Disposition'] = "attachment; filename=data.xlsx"
        return response


class DetailNewsView(APIView):

    def get(self, request):
        """
        {
          "title": "小米空气净化器疑涉“造假门” 多元化战略隐忧渐显",
          "source": "新华网",
          "time": "2015-12-11 18:00",
          "text": "就在小米科技CEO雷军宣布要将专注小米的核心业务，并将旗下核心业务分为自有产品与生态链产品的次日，小米科技旗下生态链企业智米科技，就曝出了空气净化器产品疑涉“造假门”的消息给这家明星公司的业务转型前景蒙上一层阴影。"
        }
        """
        risk_news = RiskNews.objects.get(pk=request.GET['id'])
        data = {
            'title': risk_news.title,
            'source': risk_news.publisher.publisher,
            'time': Abstract().pretty_date(risk_news.pubtime),
            'text': risk_news.content
        }
        return Response(data)


class SpeciesView(APIView, Abstract):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2016-2-1', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2016-2-3', '%Y-%m-%d'))
        type = 'species'
        species = self.risk_industry(start, end, type)
        data = {
            'species': {
                'items': [{'name': specie[0], 'level':specie[1], 'id': specie[2]}
                          for specie in species]
            }
        }
        return Response(data)
