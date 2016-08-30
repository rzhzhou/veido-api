# -*- coding: utf-8 -*-
import time
import uuid
from datetime import date, datetime, timedelta
import random
import jwt
import pytz
import operator
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import View
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.apps.riskmonitor.models import (Area, Enterprise, Industry, Product,
                                              RiskNews, RiskNewsPublisher,
                                              UserIndustry, UserArea)
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.service.analytics import AnalyticsCal
from observer.apps.riskmonitor.service.dashboard import Dashboard
from observer.apps.riskmonitor.service.enterprise import EnterpriseRank
from observer.apps.riskmonitor.service.industry import IndustryTrack
from observer.apps.riskmonitor.service.news import NewsQuerySet
from observer.utils.date import pretty
from observer.utils.date.tz import get_loc_dt, get_timezone
from observer.utils.excel import xls_to_response
from observer.utils.excel.briefing import article
from observer.utils.decorators.cache import token
from observer.utils.connector.redisconnector import RedisQueryApi


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
            'start': str(self.today - timedelta(days=32)),
            'end': str(self.today),
        }

    def set_params(self, params, loc_dt=True):
        """
        set params
        """

        for param, value in params.iteritems():
            self.query_params[param] = value

        # end date add 1 day
        if self.query_params['end'] > self.today.strftime('%Y-%m-%d'):
            self.query_params['end'] = self.today.strftime('%Y-%m-%d')

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
        super(DashboardList, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id
        self.query_params['name'] = None
        self.query_params['level'] = 3
        self.query_params['parent'] = None

    def serialize(self, queryset):
        weeks = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']
        categories = [weeks[(self.query_params['start'] + timedelta(days=(i + 1))).isoweekday() - 1]
                      for i in range(7)]
        data = {
            'summaries': [
                {
                    'name': '整体',
                    'value': 20
                },
                {
                    'name': '互联网',
                    'value': 61
                },
                {
                    'name': '抽检',
                    'value': 90
                }
            ],
            'products': {
                'categories': queryset['risk_product'][1],
                'data': queryset['risk_product'][2]
            },
            'source': [{
                'name': m['name'],
                'value': m['count']
            } for m in queryset['map']],
            'risk': {
                'categories': queryset['risk_data'][0],
                'data': queryset['risk_data'][1]
            },
            'industries': {
                'categories': [
                    '1月',
                    '2月',
                    '3月',
                    '4月',
                    '5月',
                    '6月',
                    '7月',
                    '8月',
                    '9月',
                    '10月',
                    '11月',
                    '12月'
                ],
                'data': [
                    {
                        'data': [
                            320,
                            100,
                            301,
                            334,
                            390,
                            330,
                            320,
                            110,
                            320,
                            332,
                            301,
                            334
                        ],
                        'type': 'bar',
                        'name': '家具'
                    },
                    {
                        'data': [
                            120,
                            132,
                            101,
                            134,
                            90,
                            230,
                            210,
                            110,
                            320,
                            332,
                            351,
                            334
                        ],
                        'type': 'bar',
                        'name': '儿童服装'
                    },
                    {
                        'data': [
                            220,
                            182,
                            191,
                            234,
                            290,
                            330,
                            310,
                            110,
                            320,
                            332,
                            201,
                            334
                        ],
                        'type': 'bar',
                        'name': '复合肥料'
                    }
                ]
            },
            'rank': {
                'categories': queryset['risk_level'][0],
                'data': queryset['risk_level'][1]
            }
        }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = Dashboard(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class IndustryList(BaseView):

    def __init__(self):
        super(IndustryList, self).__init__()
        self.query_params['name'] = None
        self.query_params['level'] = None
        self.query_params['parent'] = None

    def set_params(self, request):
        super(IndustryList, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id

    def serialize(self, queryset):
        data = [{
            'id': q[0],
            'category': q[1],
            'level': q[2],
            'score':q[3]
        } for q in queryset]
        data = sorted(data, key=operator.itemgetter('score'), reverse=False)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = IndustryTrack(params=self.query_params).get_industries()
        return Response(self.serialize(queryset))


# class IndustryDetail(BaseView):

#     def __init__(self):
#         super(IndustryDetail, self).__init__()

#     def set_params(self, request, pk):
#         super(IndustryDetail, self).set_params(request.GET)
#         self.query_params['industry'] = pk

#     def serialize(self, queryset):
#         data = {
#             'trend': {
#                 'labels': queryset[0]['date'],
#                 'data': queryset[0]['data']
#             },
#             'bar': {
#                 'name': [u'同比', u'环比'],
#                 'show': 'true',
#                 'lables': [queryset[1]['date']],
#                 'data': [queryset[1]['data']]
#             }
#         }
#         return data

#     def get(self, request, pk):
#         self.set_params(request, pk)

#         queryset = IndustryTrack(params=self.query_params).get_chart()

#         return Response(self.serialize(queryset))


class IndustryDetail(BaseView):

    def __init__(self):
        super(IndustryDetail, self).__init__()

    def set_params(self, request, pk):
        super(IndustryDetail, self).set_params(request.GET)
        self.query_params['industry'] = pk

    def serialize(self, queryset):
        data = {
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
                    'score': 100,
                    'color': '#95c5ab',
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
            user__id=request.user.id).area

    def paging(self, queryset):
        return super(EnterpriseList, self).paging(queryset, self.query_params['page'], 10)

    def serialize(self, queryset):
        # results = self.paging(queryset)
        # data = {
        #     'title': [u'排名', u'企业名称', u'风险信息总数', u'等级'],
        #     'items': map(lambda r: {
        #         'id': r[1]['enterprise__id'],
        #         'ranking': r[0],
        #         'title': r[1]['enterprise__name'],
        #         'level': round(r[1]['score__avg']),
        #         'number': RiskNews.objects.filter(enterprise__id=r[1]['enterprise__id']).count()
        #     }, enumerate(results, (int(self.query_params['page']) - 1) * 10 + 1)),
        #     'total': results.paginator.num_pages
        # }
        # return data
        data = [{
            'id': q.id,
            'name': q.name,
            'focus': (self.query_params['user_area'] == q.area),
            'total': RiskNews.objects.filter(enterprise__id=q.id).count()
        } for q in queryset[:25]]

        return data

    def get(self, request):
        self.set_params(request)

        queryset = EnterpriseRank(params=self.query_params).get_enterprises()

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

        queryset = RiskNews.objects.filter(enterprise__id=pk)

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

        area_id = Area.objects.get(name=self.query_params['area']).id
        areas_id = Area.objects.filter(
            parent__id=area_id).values_list('id', flat=True)

        if self.query_params['keyword']:
            queryset = RiskNews.objects.filter(
                Q(title__contains=self.query_params['keyword']) |
                Q(content__contains=self.query_params['keyword']),
                Q(area__id=area_id) |
                Q(area__id__in=areas_id) |
                Q(area__parent__id__in=areas_id)
            )
        else:
            queryset = RiskNews.objects.filter(
                Q(area__id=area_id) |
                Q(area__id__in=areas_id) |
                Q(area__parent__id__in=areas_id)
            )

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
