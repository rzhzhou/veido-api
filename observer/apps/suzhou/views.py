from datetime import date, datetime, timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from observer.apps.seer.models import Inspection as SeerInspection,Cache
from observer.utils.date.convert import utc_to_local_time, data_format
from observer.apps.suzhou.service.szarticle import (RiskProductData,RiskEnterprisesData,RiskInspectionData,
                                                    InternetRiskData)

class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {
            'starttime': self.today - timedelta(days=30),
            'endtime': self.today,
        }

    def set_params(self, params):
        for k, v in params.items():
            self.query_params[k] = v
        # self.start=self.query_params.get('start')

        # start, end convert to local datetime
        self.query_params['starttime'], self.query_params['endtime'] = utc_to_local_time(
            [self.query_params['starttime'], self.query_params['endtime']]
        )

        # end add 1 day
        self.query_params['endtime'] = self.query_params[
            'endtime'] + timedelta(days=1)

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


class RiskProductView(BaseView):  # 风险产品

    def __init__(self):
        super(RiskProductView, self).__init__()

    def set_params(self, request):
        super(RiskProductView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = [{
            'id': q[0],
            'category': q[1],
            'level': q[2],
            'score':q[3],
            'status':q[4],
            'trend':q[5]
        } for q in queryset]
        return data

    def get(self, request):
        self.set_params(request)

        limit = int(self.query_params.get('limit', 0))
        queryset = RiskProductData(params=self.query_params).get_industries()
        if limit:
            queryset = queryset[:limit]
        return Response(self.serialize(queryset))


class RiskEnterprisesView(BaseView):  # 风险企业

    def __init__(self):
        super(RiskEnterprisesView, self).__init__()

    def set_params(self, request):
        super(RiskEnterprisesView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = [{
            'id': q[0],
            'name': q[1],
            'focus': 'focus',
            'area': q[2],
            'total': SeerInspection.objects.filter(enterprise_unqualified__id=q[0]).count()
        } for q in queryset]
        return data

    def get(self, request):
        self.set_params(request)
        limit = int(self.query_params.get('limit', 0))
        queryset = RiskEnterprisesData(params=self.query_params).get_enterprises()
        if limit:
            queryset = queryset[:limit]

        return Response(self.serialize(queryset))


class RiskNewsView(BaseView):  # 风险新闻

    pass 


class RiskInspectionView(BaseView):  # 风险抽检
    def __init__(self):
        super(RiskInspectionView, self).__init__()

    def set_params(self, request):
        super(RiskInspectionView, self).set_params(request.GET)

    def paging(self, queryset):
        page = int(self.query_params['start'])+1
        return super(RiskInspectionView, self).paging(queryset, page, self.query_params['end'])

    def serialize(self, queryset):
        results = self.paging(queryset)
        data = {
            "draw": self.query_params['draw'],
            "recordsTotal": len(results),
            "recordsFiltered": len(results),
            "data": map(lambda r: {
                'id': r['guid'],
                'titleAndurl': [r['title'], r['url']],
                'time': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
                'source': r['source'],
                'qualitied': "%.2f%%" % (r['qualitied'] * 100),
                'product': r['product']
            }, results)
        }

        return data

    def get(self, request):
        self.set_params(request)
        limit = int(self.query_params.get('limit', 0))
        queryset = RiskInspectionData(params=self.query_params).get_inspection_list().order_by('-pubtime')
        if limit:
            queryset = queryset[:limit]
        return Response(self.serialize(queryset))


class WholeRiskView(BaseView):  # 整体风险变化趋势

    pass


class InternetRiskView(BaseView):  # 互联网风险数据变化趋势
    def __init__(self):
        super(InternetRiskView, self).__init__()

    def set_params(self, request):
        # request.GET add key --> level
        super(InternetRiskView, self).set_params(request.GET)
        self.query_params['user_id'] = request.user.id
        self.query_params['area_name'] = '全国'

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
                    '空气净化器/11月',
                    '空气净化器/12月',
                    '空气净化器/1月',
                    '空气净化器/2月',
                    '水泥/3月',
                    '水泥/4月',
                    '空调器/5月',
                    '空调器/6月'
                ],
                'data': [
                    {
                        'data': [
                            75.4,
                            75.9,
                            74.6,
                            76.3,
                            76.6,
                            77.1,
                            75.5,
                            73.2,
                        ],
                        'barWidth': '30%',
                        'type': 'bar'
                    }
                ]
            } if self.query_params['area_name'] == u'常州' else {
                'categories': [
                    '农药/7月',
                    '眼镜/8月',
                    '农药/9月',
                    '床上用品/10月',
                    '床上用品/11月',
                    '儿童服装/12月',
                    '烟花爆竹/1月',
                    '电热毯/2月'
                ],
                'data': [
                    {
                        'data': [
                            58.3,
                            48.2,
                            46.9,
                            53,
                            56.1,
                            49.4,
                            42.9,
                            60,
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
        start = self.query_params.get("starttime").strftime('%Y-%m-%d')
        end = self.query_params.get("endtime").strftime('%Y-%m-%d')
        user = self.query_params['user_id']
        return u'%s.%s.%s.%s.%s.%s' % ('dashboard', start, end, 3, user, '苏州')

    def get(self, request):
        self.set_params(request)
        cache = Cache.objects.filter(k=self.generate_cache_name())
        if cache:
            queryset = eval(cache.v)
        if not cache:
            queryset = InternetRiskData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))