from datetime import date, datetime, timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.utils.date.convert import utc_to_local_time

from observer.apps.yqj.models import (Article, )
from observer.apps.base.models import (Area, Article, )

from observer.apps.yqj.service.articles import (NewsQuerySet, EventsQuerySet, 
                                                ReferencesQuerySet, InsightsQuerySet, 
                                                RisksQuerySet, CategoryQuerySet,
                                                AreaQuerySet, )

from observer.apps.yqj.service.inspection import InspectionQuerySet

from observer.apps.yqj.models import Inspection as YqjInspection


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
        self.query_params['endtime'] = self.query_params['endtime'] + timedelta(days=1)

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


class NewsView(BaseView):

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
            'area': Area.objects.get(id=r['area']).name,
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = NewsQuerySet(params=self.query_params).get_all_news_list()

        return Response(self.serialize(queryset))


class EventView(BaseView):

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
            'area': Area.objects.get(id=r['area']).name,
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = EventsQuerySet(params=self.query_params).get_all_event_list()

        return Response(self.serialize(queryset))        


class ReferenceView(BaseView):

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
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = ReferencesQuerySet(params=self.query_params).get_all_reference_list()

        return Response(self.serialize(queryset)) 


class InsightView(BaseView):

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
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = InsightsQuerySet(params=self.query_params).get_all_insight_list()

        return Response(self.serialize(queryset)) 


class RiskView(BaseView):

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
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'score':r['score'],
            'relevancy':0,
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = RisksQuerySet(params=self.query_params).get_all_risk_list()

        return Response(self.serialize(queryset)) 


class InspectionView(BaseView):

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
            'title': r['title'],
            'product': r['product'],
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'source':r['source'],
            'qualitied':YqjInspection.objects.filter(base_inspection=r['guid']).values('qualitied'),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = InspectionQuerySet(params=self.query_params).get_all_inspection_list()

        return Response(self.serialize(queryset)) 


class CategoryView(BaseView):

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
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'area': Area.objects.get(id=r['area']).name,
            'source': r['source'],
            'url': r['url'],
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request,id):
        self.set_params(request)
        queryset = CategoryQuerySet(params=self.query_params).get_all_category_list(id)

        return Response(self.serialize(queryset)) 


class AreaView(BaseView):

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
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'area': Area.objects.get(id=r['area']).name,
            'source': r['source'],
            'url': r['url'],
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request,id):
        self.set_params(request)
        queryset = AreaQuerySet(params=self.query_params).get_all_area_list(id)

        return Response(self.serialize(queryset))