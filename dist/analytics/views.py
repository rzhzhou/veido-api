# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.views import APIView
from yqj.views import BaseView
from analytics.api_tools import analytics_data
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import utc
from yqj.models import Article, Weixin, Weibo
from rest_framework.response import Response


class TableAPIView(APIView):
    def __init__(self, request=None):
        self.request = request


class LineTableView(TableAPIView):
    """
    {
        "date": ["07-30", "07-31", "08-01", "08-02", "08-03", "08-04", "08-05"],
        "news_data": [491, 363, 164, 116, 331, 381, 168], 
    }
    """
    def get(self, request, id):
        start = datetime.strptime(request.GET['start'], "%Y-%m-%d")
        end = datetime.strptime(request.GET['end'], "%Y-%m-%d")
        date_range = end - start
        date = [(start + timedelta(days=x)).date() for x in xrange(date_range.days)]
        news_data = [Article.objects.filter(pubtime__gte=date[x], pubtime__lt=date[x] + timedelta(days=1)).count() for x in xrange(date_range.days)]
        weixin_data = [Weixin.objects.filter(pubtime__gte=date[x], pubtime__lt=date[x] + timedelta(days=1)).count() for x in xrange(date_range.days)]
        weibo_data = [Weibo.objects.filter(pubtime__gte=date[x], pubtime__lt=date[x] + timedelta(days=1)).count() for x in xrange(date_range.days)]
        return Response({
        "date": date,
        "news_data": news_data, 
        "weixin_data": weixin_data,
        "weibo_data": weibo_data,
        })


class PieTypeTableView(TableAPIView):
    def get(self, request):
        pass


class PieFeelingTableView(TableAPIView):
    def get(self, request):
        pass


class PieAreaTableView(TableAPIView):
    def get(self, request):
        pass


class AnalyticsView(BaseView):
    def get(self, request):
        return self.render_to_response('analytics/analytics.html', {'industry': {'name': u'综合'}})
