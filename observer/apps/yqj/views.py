from datetime import date, datetime, timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.utils.date.convert import utc_to_local_time, data_format
from observer.apps.yqj.service.articles import (NewsQuerySet, EventsQuerySet,
                                                ReferencesQuerySet, InsightsQuerySet,
                                                RisksQuerySet, CategoryQuerySet,
                                                AreaQuerySet, )
from observer.apps.yqj.service.article_utils import (is_collection, get_area, )
from observer.apps.yqj.service.dashboard import DashboardQuerySet
from observer.apps.yqj.service.inspection import InspectionQuerySet


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


class DashboardView(BaseView):  # 主页

    def __init__(self):
        super(DashboardView, self).__init__()

    def set_params(self, request):
        super(DashboardView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = {'total':queryset[0], 
                'zjrd_count': queryset[1], 
                'zjrd_proportion': queryset[2], 
                'zlsj_count': queryset[3], 
                'zlsj_proportion': queryset[4], 
                'fxkx_count': queryset[5], 
                'fxkx_proportion': queryset[6], 
                'inspection_count': queryset[7], 
                'inspection_proportion': queryset[8], 
                'zjrd_list': map(lambda r: {
                                'guid': r['guid'],
                                'title': r['title'],
                                'reprinted': r['reprinted'],
                                }, queryset[9]), 
                'zlsj_list': map(lambda r: {
                                'guid': r['guid'],
                                'title': r['title'],
                                'reprinted': r['reprinted'],
                                }, queryset[10]), 
                'xxck_list': map(lambda r: {
                                'guid': r['guid'],
                                'title': r['title'],
                                'pubtime': r['pubtime'],
                                }, queryset[11]), 
                'zjsd_list': map(lambda r: {
                                'guid': r['guid'],
                                'title': r['title'],
                                'pubtime': r['pubtime'],
                                }, queryset[12]),
                'fxkx_list': map(lambda r: {
                                'title': r['title'],
                                'url': r['url'],
                                'source': r['source'],
                                'pubtime': r['pubtime'],
                                'score': r['score'],
                                }, queryset[13]),
                'inspection_list': map(lambda r: {
                                'product': r['product'],
                                'title': r['title'],
                                'url': r['url'],
                                'qualitied': r['qualitied'],
                                'source': r['source'],
                                'pubtime': r['pubtime'],
                                }, queryset[14]),
                }

        return data

    def get(self, request):
        self.set_params(request)
        queryset = DashboardQuerySet(params=self.query_params).get_data()

        return Response(self.serialize(queryset))


class NewsView(BaseView):  # 质监热点

    def __init__(self):
        super(NewsView, self).__init__()

    def set_params(self, request):
        super(NewsView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(NewsView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'area': get_area(r['area']),
            'pubtime': data_format(r['pubtime']),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = NewsQuerySet(params=self.query_params).get_all_news_list()

        return Response(self.serialize(queryset))


class EventView(BaseView):  # 质量事件

    def __init__(self):
        super(EventView, self).__init__()

    def set_params(self, request):
        super(EventView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(EventView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'area': get_area(r['area']),
            'pubtime': data_format(r['pubtime']),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = EventsQuerySet(
            params=self.query_params).get_all_event_list()

        return Response(self.serialize(queryset))


class ReferenceView(BaseView):  # 信息参考

    def __init__(self):
        super(ReferenceView, self).__init__()

    def set_params(self, request):
        super(ReferenceView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(ReferenceView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'pubtime': data_format(r['pubtime']),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = ReferencesQuerySet(
            params=self.query_params).get_all_reference_list()

        return Response(self.serialize(queryset))


class InsightView(BaseView):  # 专家视点

    def __init__(self):
        super(InsightView, self).__init__()

    def set_params(self, request):
        super(InsightView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(InsightView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'pubtime': data_format(r['pubtime']),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = InsightsQuerySet(
            params=self.query_params).get_all_insight_list()

        return Response(self.serialize(queryset))


class RiskView(BaseView):  # 风险快讯

    def __init__(self):
        super(RiskView, self).__init__()

    def set_params(self, request):
        super(RiskView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(RiskView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'pubtime': data_format(r['pubtime']),
            'score': r['score'],
            'relevancy': 0,
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = RisksQuerySet(params=self.query_params).get_all_risk_list()

        return Response(self.serialize(queryset))


class InspectionView(BaseView):  # 抽检信息

    def __init__(self):
        super(InspectionView, self).__init__()

    def set_params(self, request):
        super(InspectionView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(InspectionView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'product': r['product'],
            'title': r['title'],
            'url': r['url'],
            'qualitied': r['qualitied'],
            'source': r['source'],
            'level': r['level'],
            'pubtime': data_format(r['pubtime']),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = InspectionQuerySet(params=self.query_params).get_all_inspection_list()

        return Response(self.serialize(queryset))


class CategoryView(BaseView):  # 业务信息

    def __init__(self):
        super(CategoryView, self).__init__()

    def set_params(self, request):
        super(CategoryView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(CategoryView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'title': r['title'],
            'pubtime': data_format(r['pubtime']),
            'area': get_area(r['area']),
            'source': r['source'],
            'url': r['url'],
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request, id):
        self.set_params(request)
        queryset = CategoryQuerySet(
            params=self.query_params).get_all_category_list(id)

        return Response(self.serialize(queryset))


class AreaView(BaseView):  # 区域信息

    def __init__(self):
        super(AreaView, self).__init__()

    def set_params(self, request):
        super(AreaView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(AreaView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'title': r['title'],
            'pubtime': data_format(r['pubtime']),
            'area': get_area(r['area']),
            'source': r['source'],
            'url': r['url'],
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request, id):
        self.set_params(request)
        queryset = AreaQuerySet(params=self.query_params).get_all_area_list(id)

        return Response(self.serialize(queryset))
