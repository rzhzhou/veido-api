# -*- coding: utf-8 -*-
import time
import uuid
import random
import jwt
import pytz
from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import View
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.apps.origin.models import Inspection
from observer.apps.riskmonitor.models import (Area, Cache, Enterprise, Industry, Product,
                                              RiskNews, RiskNewsPublisher,
                                              AreaIndustry, UserArea)
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.service.analytics import AnalyticsCal
from observer.apps.riskmonitor.service.dashboard import Dashboard
from observer.apps.riskmonitor.service.enterprise import EnterpriseRank
from observer.apps.riskmonitor.service.industry import IndustryTrack
from observer.apps.riskmonitor.service.inspection import InspectionQuerySet
from observer.apps.riskmonitor.service.news import NewsQuerySet
from observer.apps.riskmonitor.jobs.hourly.dashboard import Job as DashboardJob
from observer.apps.riskmonitor.jobs.hourly.industries import Job as IndustriesJob
from observer.utils.date import pretty
from observer.utils.date.convert import utc_to_local_time
from observer.utils.excel import xls_to_response
from observer.utils.excel.briefing import article
from observer.utils.decorators.cache import token
from observer.utils.connector.redisconnector import RedisQueryApi


class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {
            'start': self.today - timedelta(days=30),
            'end': self.today,
        }

    def set_params(self, params):
        for k, v in params.iteritems():
            self.query_params[k] = v

        # start, end convert to local datetime
        self.query_params['start'], self.query_params['end'] = utc_to_local_time(
            [self.query_params['start'], self.query_params['end']]
        )

        # end add 1 day
        self.query_params['end'] = self.query_params['end'] + timedelta(days=1)

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
        super(DashboardList, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id
        self.query_params['level'] = 3

    def serialize(self, queryset):
        data = {
            'summaries': [
                {
                    'name': '整体',
                    'value': queryset['summaries_score'][0]
                },
                {
                    'name': '互联网',
                    'value': queryset['summaries_score'][1]
                },
                {
                    'name': '抽检',
                    'value': queryset['summaries_score'][2]
                }
            ],
            'products': {
                'categories': queryset['risk_product'][1],
                'data': queryset['risk_product'][3]
            },
            'source': [{
                'name': m['name'],
                'value': m['count']
            } for m in queryset['map']],
            'risk': queryset['risk'],
            'industries': {
                'categories': [
                    '空调器/5月',
                    '空调器/6月',
                    '水泥/7月',
                    '水泥/8月',
                    '床上用品/9月',
                    '床上用品/10月',
                    '床上用品/11月',
                    'LED灯/12月',
                ],
                'data': [
                    {
                        'data': [
                            65.4,
                            65.4,
                            63.5,
                            56.1,
                            44.8,
                            52.5,
                            54.9,
                            64.5,
                        ],
                        'barWidth': '30%',
                        'type': 'bar'
                    }
                ]
            },
            'rank': {
                'categories': queryset['risk_level'][0],
                'data': queryset['risk_level'][1]
            }
        }

        return data

    def generate_cache_name(self):
        self.query_params['cache_conf_name'] = 'dashboard'
        self.query_params['days'] = (
            self.query_params['end'] - self.query_params['start']).days
        return DashboardJob().generate_cache_name(self.query_params)

    def get(self, request):
        self.set_params(request)

        try:
            cache = Cache.objects.get(k=self.generate_cache_name())
            queryset = eval(cache.v)
        except Cache.DoesNotExist:
            queryset = Dashboard(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class IndustryList(BaseView):

    def __init__(self):
        super(IndustryList, self).__init__()

    def set_params(self, request):
        super(IndustryList, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id

    def serialize(self, queryset):
        data = [{
            'id': q[0],
            'category': q[1],
            'level': q[2],
            'score':q[3],
        } for q in queryset]

        if queryset[0][2] == 1 and self.query_params.get('externalcall') is not None:

            queryset2 = IndustryTrack(params=self.query_params).while_risk()

            data.append({'first': queryset2[0],
                         'second': queryset2[1],
                         'third': queryset2[2],
                         'forth': queryset2[3],
                         'fifth': queryset2[4],
                         'sixth': queryset2[5],
                         'seventh': queryset2[6],
                         'datetime': queryset2[7],
                         'totalScore': queryset2[8],
                         })

        return data

    def generate_cache_name(self):
        self.query_params['cache_conf_name'] = 'industries'
        self.query_params['days'] = (
            self.query_params['end'] - self.query_params['start']).days
        return IndustriesJob().generate_cache_name(self.query_params)

    def get(self, request):
        self.set_params(request)

        limit = int(self.query_params.get('limit', 0))

        try:
            cache = Cache.objects.get(k=self.generate_cache_name())
            queryset = eval(cache.v)
        except Cache.DoesNotExist:
            queryset = IndustryTrack(params=self.query_params).get_industries()

        if limit:
            queryset = queryset[:limit]

        return Response(self.serialize(queryset))


class IndustryDetail(BaseView):

    def __init__(self):
        super(IndustryDetail, self).__init__()

    def set_params(self, request, pk):
        super(IndustryDetail, self).set_params(request.GET)
        self.query_params['industry'] = pk

    def serialize(self, queryset):
        data = {
            'name': queryset['name'],
            'total': {
                'level': queryset['risk_rank'][0],
                'score': queryset['risk_rank'][1],
                'color': queryset['risk_rank'][2]
            },
            'indicators': [
                {
                    'title': u'消费指标',
                    'score': queryset['indicators'][0][1],
                    'color': queryset['indicators'][0][2],
                    'norms': [
                        {
                            'name': u'国家强制性要求',
                            'options': [
                                {'label': u'有', 'selected': queryset[
                                    'indicators'][0][0][0] == 1},
                                {'label': u'无', 'selected': queryset[
                                    'indicators'][0][0][0] == 0}
                            ]
                        },
                        {
                            'name': u'密切程度',
                            'options': [
                                {'label': u'高', 'selected': queryset[
                                    'indicators'][0][0][1] == 3},
                                {'label': u'中', 'selected': queryset[
                                    'indicators'][0][0][1] == 2},
                                {'label': u'低', 'selected': queryset[
                                    'indicators'][0][0][1] == 1}
                            ]
                        },
                        {
                            'name': u'涉及特定消费群体',
                            'options': [
                                {'label': u'是', 'selected': queryset[
                                    'indicators'][0][0][2] == 1},
                                {'label': u'否', 'selected': queryset[
                                    'indicators'][0][0][2] == 0}
                            ]
                        }
                    ]
                },
                {
                    'title': u'社会性指标',
                    'score': queryset['indicators'][1][1],
                    'color': queryset['indicators'][1][2],
                    'norms': [
                        {
                            'name': u'贸易量',
                            'options': [
                                {'label': u'高', 'selected': queryset[
                                    'indicators'][1][0][0] == 3},
                                {'label': u'中', 'selected': queryset[
                                    'indicators'][1][0][0] == 2},
                                {'label': u'低', 'selected': queryset[
                                    'indicators'][1][0][0] == 1}
                            ]
                        },
                        {
                            'name': u'抽检合格率',
                            'options': [
                                {'label': u'高', 'selected': queryset[
                                    'indicators'][1][0][1] == 3},
                                {'label': u'中', 'selected': queryset[
                                    'indicators'][1][0][1] == 2},
                                {'label': u'低', 'selected': queryset[
                                    'indicators'][1][0][1] == 1}
                            ]
                        },
                        {
                            'name': u'案例发生状况',
                            'options': [
                                {'label': u'高', 'selected': queryset[
                                    'indicators'][1][0][2] == 3},
                                {'label': u'中', 'selected': queryset[
                                    'indicators'][1][0][2] == 2},
                                {'label': u'低', 'selected': queryset[
                                    'indicators'][1][0][2] == 1}
                            ]
                        }
                    ]
                },
                {
                    'title': '管理指标',
                    'score': queryset['indicators'][2][1],
                    'color': queryset['indicators'][2][2],
                    'norms': [
                        {
                            'name': u'列入许可证目录',
                            'options': [
                                {'label': u'是', 'selected': queryset[
                                    'indicators'][2][0][0] == 1},
                                {'label': u'否', 'selected': queryset[
                                    'indicators'][2][0][0] == 0}
                            ]
                        },
                        {
                            'name': u'列入产品认证目录',
                            'options': [
                                {'label': u'是', 'selected': queryset[
                                    'indicators'][2][0][1] == 1},
                                {'label': u'否', 'selected': queryset[
                                    'indicators'][2][0][1] == 0}
                            ]
                        },
                        {
                            'name': u'是否鼓励',
                            'options': [
                                {'label': u'是', 'selected': queryset[
                                    'indicators'][2][0][2] == 1},
                                {'label': u'否', 'selected': queryset[
                                    'indicators'][2][0][2] == 0}
                            ]
                        },
                        {
                            'name': u'是否限制',
                            'options': [
                                {'label': u'是', 'selected': queryset[
                                    'indicators'][2][0][3] == 1},
                                {'label': u'否', 'selected': queryset[
                                    'indicators'][2][0][3] == 0}
                            ]
                        },
                        {
                            'name': u'是否淘汰',
                            'options': [
                                {'label': u'是', 'selected': queryset[
                                    'indicators'][2][0][4] == 1},
                                {'label': u'否', 'selected': queryset[
                                    'indicators'][2][0][4] == 0}
                            ]
                        }
                    ]
                },
                {
                    'title': '风险新闻',
                    # 'score': random.randint(85, 95),
                    'score': queryset['indicators'][3][1],
                    'color': queryset['indicators'][3][2],
                    'norms': [{
                        'title': q.title,
                        'source': q.publisher.name,
                        'time': q.pubtime.strftime('%Y-%m-%d'),
                        'url': q.url
                    } for q in queryset['indicators'][3][0]]
                },
                {
                    'title': '风险抽检',
                    'score': queryset['indicators'][4][1],
                    'color': queryset['indicators'][4][2],
                    'norms': [{
                        'title': q.title,
                        'source': q.publisher.name,
                        'time': q.pubtime.strftime('%Y-%m-%d'),
                        'url': q.url,
                        'qualitied': q.qualitied
                    } for q in queryset['indicators'][4][0]]
                }
            ],
            'trend': {
                'categories': queryset['trend']['categories'],
                'data': queryset['trend']['data']
            }

        }
        return data

    def get(self, request, pk):
        self.set_params(request, pk)

        queryset = IndustryTrack(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class NewsList(BaseView):

    def __init__(self):
        super(NewsList, self).__init__()

    def set_params(self, request):
        super(NewsList, self).set_params(request.GET)
        self.query_params['industry'] = int(self.query_params['id'])

    def paging(self, queryset):
        return super(NewsList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        results = self.paging(queryset)
        data = map(lambda r: {
            'id': r['id'],
            'url': r['url'],
            'title': r['title'],
            'time': r['pubtime'].strftime('%Y-%m-%d %H:%M'),
            'source': r['publisher__name']
        }, results)

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
        self.query_params['user_area'] = UserArea.objects.get(
            user__id=request.user.id).area.name

    def paging(self, queryset):
        return super(EnterpriseList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        data = [{
            'id': q[0],
            'name': q[1],
            'focus': (self.query_params['user_area'] == q[2]),
            'area': q[2],
            'product': q[3],
            'issure': q[4],
            'total': Inspection.objects.filter(enterprise_unqualified__id=q[0]).count()
        } for q in queryset]

        return data

    def get(self, request):
        self.set_params(request)

        limit = int(self.query_params.get('limit', 0))

        queryset = EnterpriseRank(params=self.query_params).get_enterprises()

        if limit:
            queryset = queryset[:limit]

        return Response(self.serialize(queryset))


class EnterpriseDetail(BaseView):

    def __init__(self):
        super(EnterpriseDetail, self).__init__()

    def set_params(self, request):
        super(EnterpriseDetail, self).set_params(request.GET)

    def serialize(self, queryset):
        data = map(lambda r: {
            'id': r.id,
            'url': r.url,
            'title': r.title,
            'time': r.pubtime.strftime('%Y-%m-%d %H:%M'),
            'source': r.publisher.name
        }, queryset)

        return data

    def get(self, request, pk):
        self.set_params(request)

        queryset = Inspection.objects.filter(enterprise_unqualified__id=pk)

        return Response(self.serialize(queryset))


class RiskNewsList(BaseView):

    def __init__(self):
        super(RiskNewsList, self).__init__()

    def set_params(self, request):
        super(RiskNewsList, self).set_params(request.GET)

    def paging(self, queryset):
        return super(RiskNewsList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        results = self.paging(queryset)
        data = map(lambda r: {
            'id': r['id'],
            'url': r['url'],
            'title': r['title'],
            'time': r['pubtime'].strftime('%Y-%m-%d %H:%M'),
            'source': r['publisher__name']
        }, results)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = NewsQuerySet(params=self.query_params).get_news_list()

        return Response(self.serialize(queryset))



class InspectionList(BaseView):

    def __init__(self):
        super(InspectionList, self).__init__()

    def set_params(self, request):
        super(InspectionList, self).set_params(request.GET)

    def paging(self, queryset):
        return super(InspectionList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        results = self.paging(queryset)
        data = map(lambda r: {
            'id': r['id'],
            'url': r['url'],
            'title': r['title'],
            'time': r['pubtime'].strftime('%Y-%m-%d %H:%M'),
            'source': r['publisher__name']
        }, results)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = InspectionQuerySet(params=self.query_params).get_inspection_list()

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


class Search(BaseView):

    def __init__(self):
        super(Search, self).__init__()

    def set_params(self, request):
        self.query_params['keyword'] = request.GET.get('keyword')
        self.query_params['area'] = request.GET.get('area')

    def serialize(self, queryset):
        data = [{
            'title': q.title,
            'source': q.publisher.name,
            'reprint': q.reprinted,
            'time': q.pubtime.strftime('%Y-%m-%d'),
            'url': q.url
        } for q in queryset[:25]]

        return data

    def get(self, request):
        self.set_params(request)

        area = Area.objects.get(name=self.query_params['area'])
        areas_id = [area.id]

        if area.level == 1:
            areas_id = None
        elif area.level == 2:
            level_3_id = Area.objects.filter(
                parent__id=area.id
            ).values_list(
                'id',
                flat=True
            )
            level_4_id = Area.objects.filter(
                parent__id__in=level_3_id
            ).values_list(
                'id',
                flat=True
            )
            areas_id = areas_id + list(level_3_id) + list(level_4_id)
        elif area.level == 3:
            level_4_id = Area.objects.filter(
                parent__id=area.id
            ).values_list(
                'id',
                flat=True
            )
            areas_id = areas_id + list(level_4_id)

        cond = {
            'area__id__in': areas_id
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        if self.query_params['keyword']:
            queryset = RiskNews.objects.filter(
                Q(title__contains=self.query_params['keyword']) |
                Q(content__contains=self.query_params['keyword']),
                **args
            )
        else:
            queryset = RiskNews.objects.filter(**args)

        queryset = queryset.distinct()

        return Response(self.serialize(queryset))


def logout_view(request):
    auth = settings.JWT_AUTH
    secret_key = auth['JWT_SECRET_KEY']
    algorithm = auth['JWT_ALGORITHM']
    token = eval(request.body)['token']
    result = jwt.decode(token, secret_key, algorithm)
    name = result['username'] + str(uuid.uuid1())
    RedisQueryApi().set(name, token)
    RedisQueryApi().expire(name, result['exp'])
    return JsonResponse({'status': 'true'})
