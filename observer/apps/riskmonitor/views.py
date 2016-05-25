# -*- coding: utf-8 -*-
import time
from datetime import date, datetime, timedelta

import jwt
import pytz
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import View
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.apps.base.initialize import xls_to_response
from observer.apps.base.views import BaseTemplateView
from observer.apps.riskmonitor.models import (Enterprise, Industry, Product,
                                              RiskNews, RiskNewsPublisher,
                                              UserIndustry)
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.service.analytics import AnalyticsCal
from observer.apps.riskmonitor.service.dashboard import Dashboard
from observer.apps.riskmonitor.service.enterprise import EnterpriseRank
from observer.apps.riskmonitor.service.industry import IndustryTrack
from observer.apps.riskmonitor.service.news import NewsQuerySet
from observer.utils.date import pretty
from observer.utils.date.tz import get_loc_dt, get_timezone
from observer.utils.excel.briefing import article


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
            'start': str(self.today - timedelta(days=6)),
            'end': str(self.today)
        }

    def set_params(self, params, loc_dt=True):
        """
        set params
        """

        for param, value in params.iteritems():
            self.query_params[param] = value

        # end date add 1 day
        self.query_params['end'] = datetime.strptime(
            self.query_params['end'], '%Y-%m-%d') + timedelta(days=1)
        self.query_params['end'] = self.query_params[
            'end'].strftime('%Y-%m-%d')

        if loc_dt:
            self.query_params['start'] = get_loc_dt(
                self.tz, self.query_params['start'], pytz.utc)
            self.query_params['end'] = get_loc_dt(
                self.tz, self.query_params['end'], pytz.utc)

    def paging(self, queryset, page, num):
        paginator = Paginator(queryset, num)  # Show $num <QuerySet> per page

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            results = paginator.page(paginator.num_pages)

        return results


class DashboardList(BaseView):

    def __init__(self):
        super(DashboardList, self).__init__()

    def set_params(self, request):
        # request.GET add key --> level
        request_value = {}
        for param, value in request.GET.iteritems():
            request_value[param] = value
        request_value["level"] = request_value.get("level", 3)

        super(DashboardList, self).set_params(request_value)
        self.query_params['user_id'] = request.user.id

    def serialize(self, queryset):
        weeks = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五', u'星期六', u'星期日']
        data = {
            'map': [{
                'name': m['name'],
                'value': m['count']
            } for m in queryset['map']],
            'rankData': {
                'labels': [weeks[(self.query_params['start'] + timedelta(days=(i + 1))).isoweekday() - 1]
                           for i in range(7)],
                'data': queryset['rank_data']
            },
            'grade': queryset['status'],
            'enterpriseRank': {
                'items': [{
                    'id': e['enterprise__id'],
                    'name': e['enterprise__name'],
                    'level': round(e['score__avg'])
                } for e in queryset['enterprises']]
            },
            'industry': {
                'amount': queryset['risk_count'][0]
            },
            'industryRank': {
                'items': [{
                    'id': i[0],
                    'name': i[1],
                    'level':i[2]
                } for i in queryset['industries']]
            },

            'risk_product': {
                'name': queryset['risk_product'][0],
                'value': queryset['risk_product'][1]
            },
            'product': {
                'amount': queryset['risk_count'][2]
            },
            'riskData': {
                'labels': [weeks[(self.query_params['start'] + timedelta(days=(i + 1))).isoweekday() - 1]
                           for i in range(7)],
                'data': queryset['risk_data']
            },
            'keywordsRank': {
                'items': [{
                    'name': name,
                    'level': value
                } for name, value in zip(*queryset['keywords'])]
            },
            'enterprise': {
                'amount': queryset['risk_count'][1]
            },
            'boards': [
                {'value': 20, 'name': '整体'},
                {'value': 61, 'name': '互联网'},
                {'value': 90, 'name': '抽检'}
              ]
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = Dashboard(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class IndustryList(BaseView):

    def __init__(self):
        super(IndustryList, self).__init__()
        self.query_params['field'] = 'name'

    def set_params(self, request):
        # request.GET add key --> level
        request_value = {}
        for param, value in request.GET.iteritems():
            request_value[param] = value
        request_value["level"] = request_value.get("level", 3)

        super(IndustryList, self).set_params(request_value)
        self.query_params['user_id'] = request.user.id

    def serialize(self, queryset):
        data = {
            'industries': {
                'items': [{
                    'id': q[0],
                    self.query_params['field']: q[1],
                    'level':q[2]
                } for q in queryset]
            }
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = IndustryTrack(params=self.query_params).get_industries()

        return Response(self.serialize(queryset))


class IndustryDetail(BaseView):

    def __init__(self):
        super(IndustryDetail, self).__init__()

    def set_params(self, request, pk):
        super(IndustryDetail, self).set_params(request.GET)
        self.query_params['industry'] = pk

    def serialize(self, queryset):
        data = {
            'trend': {
                'labels': queryset[0]['date'],
                'data': queryset[0]['data']
            },
            'bar': {
                'name': [u'同比', u'环比'],
                'show': 'true',
                'lables': [queryset[1]['date']],
                'data': [queryset[1]['data']]
            }
        }
        return data

    def get(self, request, pk):
        self.set_params(request, pk)

        queryset = IndustryTrack(params=self.query_params).get_chart()

        return Response(self.serialize(queryset))


class NewsList(BaseView):

    def __init__(self):
        super(NewsList, self).__init__()

    def set_params(self, request):
        super(NewsList, self).set_params(request.GET)

    def paging(self, queryset):
        return super(NewsList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        results = self.paging(queryset)
        data = {
            'title': [u'序号', u'标题', u'来源', u'发表时间'],
            'items': map(lambda r: {
                'id': r['id'],
                'title': r['title'],
                'time': r['pubtime'].strftime('%Y-%m-%d %H:%M'),
                'source': r['publisher__name']
            }, results),
            'total': results.paginator.num_pages
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = NewsQuerySet(params=self.query_params).get_news_list()

        return Response(self.serialize(queryset))


class NewsDetail(BaseView):

    def serialize(self, queryset):
        data = {
            'title': queryset.title,
            'source': queryset.publisher.name,
            'time': pretty(queryset.pubtime),
            'text': queryset.content
        }
        return data

    def get(self, request, pk):
        try:
            queryset = RiskNews.objects.get(pk=pk)
        except RiskNews.DoesNotExist:
            raise Http404("RiskNews does not exist")

        return Response(self.serialize(queryset))


class EnterpriseList(BaseView):

    def __init__(self):
        super(EnterpriseList, self).__init__()

    def set_params(self, request):
        super(EnterpriseList, self).set_params(request.GET)

    def paging(self, queryset):
        return super(EnterpriseList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        results = self.paging(queryset)
        data = {
            'title': [u'排名', u'企业名称', u'风险信息总数', u'等级'],
            'items': map(lambda r: {
                'id': r[1]['enterprise__id'],
                'ranking': r[0],
                'title': r[1]['enterprise__name'],
                'level': round(r[1]['score__avg']),
                'number': RiskNews.objects.filter(enterprise__id=r[1]['enterprise__id']).count()
            }, enumerate(results, (int(self.query_params['page']) - 1) * 10 + 1)),
            'total': results.paginator.num_pages
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = EnterpriseRank(params=self.query_params).get_enterprises()

        return Response(self.serialize(queryset))


class Analytics(BaseView):

    def __init__(self):
        super(Analytics, self).__init__()

    def set_params(self, request):
        super(Analytics, self).set_params(request.GET)

    def serialize(self, queryset):
        data = {
            'trend': {
                'labels': queryset['trend']['date'],
                'data': queryset['trend']['data']
            },
            'bar': {
                'name': [u'关键字'],
                'show': 'false',
                'labels': queryset['bar'][0],
                'data': [queryset['bar'][1]]
            },
            'source': {
                'labels': zip(*queryset['source'])[0] if queryset['source'] else [],
                'data': [{
                    'name': q[0],
                    'value': q[1]
                } for q in queryset['source']]
            }
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = AnalyticsCal(params=self.query_params).get_chart()

        return Response(self.serialize(queryset))


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

    def paging(self, queryset):
        return super(AnalyticsExport, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        results = self.paging(queryset['list'])
        data = {
            'trend': {
                'labels': queryset['trend']['date'],
                'data': queryset['trend']['data']
            },
            'bar':  {
                'name': [u'关键字'],
                'show': 'false',
                'labels': queryset['bar'][0],
                'data': [queryset['bar'][1]]
            },
            'source': {
                'labels': zip(*queryset['source'])[0] if queryset['source'] else [],
                'data': [{
                    'name': q[0],
                    'value': q[1]
                } for q in queryset['source']]
            },
            'list': {
                'title': [u'序号', u'标题', u'来源', u'发表时间'],
                'items': map(lambda r: {
                    'id': r['id'],
                    'title': r['title'],
                    'time': r['pubtime'].strftime('%Y-%m-%d %H:%M'),
                    'source': r['publisher__name']
                }, queryset['list']),
                'total': results.paginator.num_pages
            }
        }
        return data

    def get(self, request, filename):
        try:
            jwt_payload = jwt.decode(
                request.GET['payload'], settings.JWT_AUTH['JWT_SECRET_KEY'])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            return JsonResponse({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

        self.set_params(jwt_payload)

        queryset = AnalyticsCal(params=self.query_params).get_all()

        brief = article()
        output = brief.get_output(self.serialize(queryset))
        output.seek(0)

        response = xls_to_response(
            fname=filename, format='xlsx', source=output)
        return response


class Filters(BaseView):

    def __init__(self):
        super(Filters, self).__init__()

    def set_params(self, request):
        super(Filters, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id

    def serialize(self, queryset):
        data = {
            'industries': {
                'items': [{
                    'id': q['id'],
                    'text': q['name']
                } for q in queryset[0]],
            },
            'enterprises': {
                'items': queryset[1],
            },
            'products': {
                'items': queryset[2],
            },
            'publishers': {
                'items': [{
                    'id': q['publisher__id'],
                    'text': q['publisher__name']
                } for q in queryset[3]],
            }
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = AnalyticsCal(params=self.query_params).get_filters()

        return Response(self.serialize(queryset))
