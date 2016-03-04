# -*- coding: utf-8 -*-
from tests import test_tools
test_tools()
import pytz
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings

from observer.apps.base.views import BaseTemplateView
from observer.apps.riskmonitor.models import RiskNews
from businesslogic.detail import *
from businesslogic.enterprise_rank import EnterpriseRank
from businesslogic.homepage import *
from businesslogic.industry_track import IndustryTrack
from businesslogic.statistic import Statistic


class HomePageView(APIView, BaseTemplateView):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2016-2-1', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2016-2-3', '%Y-%m-%d'))
        start = end - timedelta(days=7)
        data = HomeData(start, end).get_all()
        return Response(data)


class IndustryTrackView(APIView):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2016-11-22', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2015-11-30', '%Y-%m-%d'))
        id = 2
        data = IndustryTrack(industry=id, start=start, end=end).get_all()
        return Response(data)


class EnterpriseRankView(APIView):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2015-11-22', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2015-11-30', '%Y-%m-%d'))
        id = 2
        data = EnterpriseRank(industry=id, start=start, end=end).get_all()
        return Response(data)


class StatisticView(APIView):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2015-11-22', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2015-11-30', '%Y-%m-%d'))
        data = Statistic(start=start, end=end).get_all()
        return Response(data)


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
            'time': risk_news.pubtime,
            'text': risk_news.content
        }
        return Response(data)


