# -*- coding: utf-8 -*-
import time
from datetime import date, datetime, timedelta

import jwt
import pytz
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import View
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from businesslogic.detail import *
from businesslogic.enterprise import EnterpriseRank
from businesslogic.homepage import *
from businesslogic.industry import IndustryTrack
from businesslogic.statistic import Statistic
from observer.apps.base.initialize import xls_to_response
from observer.apps.base.views import BaseTemplateView
from observer.apps.riskmonitor.businesslogic.abstract import Abstract
from observer.apps.riskmonitor.models import (Enterprise, Industry, Product,
                                              RiskNews, RiskNewsPublisher,
                                              UserIndustry)
from observer.utils.excel.briefing import article
from utils.date.tz import get_loc_dt, get_timezone


class BaseView(APIView):

    def __init__(self):
        self.tz = pytz.timezone(settings.TIME_ZONE)
        self.today = date.today()
        self.query_params = {
            'industry': None,
            'enterprise': None,
            'product': None,
            'source': None,
            'page': 1,
            'start': str(self.today - timedelta(days=7)),
            'end': str(self.today)
        }

    def set_params(self, params, loc_dt=True):
        """
        set params
        """

        for param, value in params.iteritems():
            self.query_params[param] = value

        if loc_dt:
            self.query_params['start'] = get_loc_dt(
                self.tz, self.query_params['start'], pytz.utc)
            self.query_params['end'] = get_loc_dt(
                self.tz, self.query_params['end'], pytz.utc)


class HomePageView(BaseView):

    def __init__(self):
        super(HomePageView, self).__init__()

    def set_params(self, request):
        super(HomePageView, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id

    def get(self, request):
        self.set_params(request)

        data = HomeData(params=self.query_params).get_all()
        return Response(data)


class IndustryList(BaseView, Abstract):

    def __init__(self):
        super(IndustryList, self).__init__()
        self.query_params['field'] = 'name'

    def set_params(self, request):
        super(IndustryList, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id

    def get(self, request):
        self.set_params(request)

        industries = self.risk_industry(self.query_params['start'],
                                        self.query_params['end'],
                                        self.query_params['user_id'])
        data = {
            'industries': {
                'items': [{
                    self.query_params['field']: industry[0],
                    'level':industry[1],
                    'id': industry[2]
                } for industry in industries]
            }
        }
        return Response(data)


class IndustryDetail(BaseView):

    def __init__(self):
        super(IndustryDetail, self).__init__()

    def set_params(self, request, pk):
        super(IndustryDetail, self).set_params(request.GET)
        self.query_params['industry'] = pk

    def get(self, request, pk):
        self.set_params(request, pk)

        data = IndustryTrack(params=self.query_params).get_chart()
        return Response(data)


class NewsList(BaseView):

    def __init__(self):
        super(NewsList, self).__init__()

    def set_params(self, request):
        super(NewsList, self).set_params(request.GET)

    def get(self, request):
        self.set_params(request)

        data = IndustryTrack(params=self.query_params).news_data()
        return Response(data)


class NewsDetail(BaseView):

    def get(self, request, pk):
        """
        {
          "title": "小米空气净化器疑涉“造假门” 多元化战略隐忧渐显",
          "source": "新华网",
          "time": "2015-12-11 18:00",
          "text": "就在小米科技CEO雷军宣布要将专注小米的核心业务，并将旗下核心业务分为自有产品与生态链产品的次日，小米科技旗下生态链企业智米科技，就曝出了空气净化器产品疑涉“造假门”的消息给这家明星公司的业务转型前景蒙上一层阴影。"
        }
        """
        try:
            risk_news = RiskNews.objects.get(pk=pk)
        except RiskNews.DoesNotExist:
            raise Http404("RiskNews does not exist")

        data = {
            'title': risk_news.title,
            'source': risk_news.publisher.publisher,
            'time': Abstract().pretty_date(risk_news.pubtime),
            'text': risk_news.content
        }
        return Response(data)


class EnterpriseList(BaseView):

    def __init__(self):
        super(EnterpriseList, self).__init__()

    def set_params(self, request):
        super(EnterpriseList, self).set_params(request.GET)

    def get(self, request):
        self.set_params(request)

        data = EnterpriseRank(params=self.query_params).get_all()
        return Response(data)


class Analytics(BaseView):

    def __init__(self):
        super(Analytics, self).__init__()

    def set_params(self, request):
        super(Analytics, self).set_params(request.GET)

    def get(self, request):
        self.set_params(request)

        data = Statistic(params=self.query_params).get_chart()
        return Response(data)


class GenerateAnalyticsExport(BaseView):

    def __init__(self):
        super(GenerateAnalyticsExport, self).__init__()

    def set_params(self, request, loc_dt=False):
        super(GenerateAnalyticsExport, self).set_params(request.GET, loc_dt)
        self.query_params['exp'] = datetime.utcnow() + timedelta(seconds=60)

    def get(self, request):
        self.set_params(request)

        jwt_payload = jwt.encode(
            self.query_params, settings.JWT_AUTH['JWT_SECRET_KEY'])
        return Response({'url': '/api/files/%s?payload=%s' % ('data', jwt_payload)})


class AnalyticsExport(BaseView):

    def __init__(self):
        super(AnalyticsExport, self).__init__()

    def set_params(self, params):
        super(AnalyticsExport, self).set_params(params)

    def get(self, request, filename):
        try:
            jwt_payload = jwt.decode(
                request.GET['payload'], settings.JWT_AUTH['JWT_SECRET_KEY'])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            return JsonResponse({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

        self.set_params(jwt_payload)

        data = Statistic(params=self.query_params).get_all()
        brief = article()
        output = brief.get_output(data)
        output.seek(0)

        response = xls_to_response(
            fname=filename, format='xlsx', source=output)
        return response


class Filters(BaseView):

    def get(self, request):
        """
        Industries, Enterprises, Products, Publishers Filters
        {
            'industries': {
                'items': [{
                    'id': 1,
                    'name': '行业',
                }]
            },
            'enterprises': {
                'items': [{
                    'id': 1,
                    'name': '企业',
                }]
            },
            'products': {
                'items': [{
                    'id': 1,
                    'nam'e: '产品',
                }]
            },
            'publishers': {
                'items': [{
                    'id': 1,
                    'name': '发布者',
                }]
            }
        }
        """
        industries = UserIndustry.objects.filter(
            user__id=request.user.id).annotate(text=F('name')).values('id', 'text')
        enterprises = Enterprise.objects.annotate(
            text=F('name')).values('id', 'text')[:10]
        products = Product.objects.annotate(
            text=F('name')).values('id', 'text')[:10]
        publishers = RiskNewsPublisher.objects.annotate(
            text=F('publisher')).values('id', 'text')[:10]

        data = {
            'industries': {
                'items': industries,
            },
            'enterprises': {
                'items': enterprises,
            },
            'products': {
                'items': products,
            },
            'publishers': {
                'items': publishers,
            }
        }

        return Response(data)
