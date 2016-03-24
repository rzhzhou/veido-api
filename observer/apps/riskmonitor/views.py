# -*- coding: utf-8 -*-
import pytz
import jwt
import time
from datetime import date, datetime, timedelta

from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

from observer.apps.base.views import BaseTemplateView
from observer.apps.riskmonitor.models import (
    RiskNews, Industry, Enterprise, Product, RiskNewsPublisher,
    UserIndustry)
from observer.apps.riskmonitor.businesslogic.abstract import Abstract
from observer.apps.base.initialize import xls_to_response
from observer.utils.excel.briefing import article
from businesslogic.detail import *
from businesslogic.enterprise import EnterpriseRank
from businesslogic.homepage import *
from businesslogic.industry import IndustryTrack
from businesslogic.statistic import Statistic


class HomePageView(APIView):

    def get(self, request):
        user_id = request.user.id
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        data = HomeData(start, end, user_id).get_all()
        return Response(data)


class IndustryList(APIView, Abstract):

    def get(self, request):
        user_id = request.user.id
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))
        field = request.GET.get('field', 'name')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        industries = self.risk_industry(start, end, user_id)
        data = {
            'industries': {
                'items': [{field: industry[0], 'level':industry[1], 'id': industry[2]}
                          for industry in industries]
            }
        }
        return Response(data)


class IndustryDetail(APIView):

    def get(self, request, pk):
        page = request.GET.get('page', 1)
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        try:
            pk = UserIndustry.objects.get(id=pk).industry.id
        except ObjectDoesNotExist:
            pk = None

        data = IndustryTrack(industry=pk, start=start,
                             end=end, page=page).get_chart()
        return Response(data)


class NewsList(APIView):

    def get(self, request):
        pk = request.GET.get('industry', None)
        page = request.GET.get('page', 1)
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        try:
            pk = UserIndustry.objects.get(id=pk).industry.id
        except ObjectDoesNotExist:
            pk = None

        data = IndustryTrack(industry=pk, start=start,
                             end=end, page=page).news_data()
        return Response(data)


class NewsDetail(APIView):

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


class EnterpriseList(APIView):

    def get(self, request):
        pk = request.GET.get('industry', 0)
        page = request.GET.get('page', 1)
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        data = EnterpriseRank(industry=int(pk), start=start, end=end,
                              page=int(page)).get_all()

        return Response(data)


class Analytics(APIView):

    def get(self, request):
        pk = request.GET.get('industry', 0)
        page = request.GET.get('page', 1)
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))
        dtype = request.GET.get('type', '')

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(start, '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(end, '%Y-%m-%d'))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        if dtype == 'table':
            data = Statistic(industry=pk, start=start,
                             end=end, page=page).get_data()
            return Response(data)
        else:
            data = Statistic(industry=pk, start=start,
                             end=end, page=page).get_chart()
            return Response(data)


class AnalyticsExport(View):

    def get(self, request, filename, format=None):
        try:
            jwt_payload = jwt.decode(
                request.GET['payload'], settings.JWT_AUTH['JWT_SECRET_KEY'])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            return JsonResponse({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

        tz = pytz.timezone(settings.TIME_ZONE)
        start = tz.localize(datetime.strptime(
            jwt_payload['start'], '%Y-%m-%d'))
        end = tz.localize(datetime.strptime(jwt_payload['end'], '%Y-%m-%d'))

        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)

        data = Statistic(industry=jwt_payload[
                         'pk'], start=start, end=end, page=jwt_payload['page']).get_all()
        brief = article()
        output = brief.get_output(data)
        output.seek(0)

        response = xls_to_response(
            fname=filename, format=format, source=output)
        return response


class GenerateAnalyticsExport(APIView):

    def get(self, request):
        pk = request.GET.get('industry', 0)
        page = request.GET.get('page', 1)
        today = date.today()
        start = request.GET.get('start', str(today - timedelta(days=7)))
        end = request.GET.get('end', str(today))

        jwt_payload = jwt.encode({
            'pk': pk,
            'page': page,
            'start': start,
            'end': end,
            'exp': datetime.utcnow() + timedelta(seconds=60)
        }, settings.JWT_AUTH['JWT_SECRET_KEY'])

        return Response({'url': '/api/files/%s.xlsx?payload=%s' % ('data', jwt_payload)})


class Filters(APIView):

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
        industries = Industry.objects.annotate(
            text=F('name')).values('id', 'text')[:10]
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
