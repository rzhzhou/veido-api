# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.views import APIView

from base.views import BaseView


class TableAPIView(APIView):
    def __init__(self, request=None):
        self.request = request


class LineTableView(TableAPIView):
    def get(self, request ):
        pass


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
