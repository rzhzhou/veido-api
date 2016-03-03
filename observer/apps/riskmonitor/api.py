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
from businesslogic.detail import *
from businesslogic.enterprise_rank import *
from businesslogic.homepage import *
from businesslogic.industry_track import IndustryTrack
from businesslogic.statistic import *


class HomePageView(APIView, BaseTemplateView):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2015-11-22', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2015-11-30', '%Y-%m-%d'))
        start = end - timedelta(days=7)
        data = HomeData(start, end).get_all()
        return Response(data)


class IndustryTrackView(APIView):

    def get(self, request):
        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime('2015-11-22', '%Y-%m-%d'))
        end = tz.localize(datetime.strptime('2015-11-30', '%Y-%m-%d'))
        id =2
        data = IndustryTrack(industry=id, start=start, end=end).get_all()
        return Response(data)


def enterprise_rank(self, request, id):
    pass


def statistic(self, request, id):
    pass


def detail(self, request, id):
    pass
