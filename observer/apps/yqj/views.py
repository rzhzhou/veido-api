from datetime import date, datetime, timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.utils.date.convert import utc_to_local_time,data_format

from observer.apps.yqj.models import (Article, )
from observer.apps.base.models import (Area, Article, )

from observer.apps.yqj.service.articles import ArticlesQuerySet,EventsQuerySet,\
ReferencesQuerySet,InsightsQuerySet,RisksQuerySet,CategoryQuerySet,AreaQuerySet

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


class ArticleView(BaseView):#质监热点

    def __init__(self):
        super(ArticleView, self).__init__()

    def set_params(self, request):
        super(ArticleView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(ArticleView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'area': Area.objects.get(id=r['area']).name,
            'pubtime': data_format(r['pubtime']),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = ArticlesQuerySet(params=self.query_params).get_all_article_list()

        return Response(self.serialize(queryset))


class EventView(BaseView):#质量事件

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
            'pubtime': data_format(r['pubtime']),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = EventsQuerySet(params=self.query_params).get_all_event_list()

        return Response(self.serialize(queryset))        


class ReferenceView(BaseView):#信息参考

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
        queryset = ReferencesQuerySet(params=self.query_params).get_all_reference_list()

        return Response(self.serialize(queryset)) 


class InsightView(BaseView):#专家视点

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
        queryset = InsightsQuerySet(params=self.query_params).get_all_insight_list()

        return Response(self.serialize(queryset)) 


class RiskView(BaseView):#风险快讯

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
            'score':r['score'],
            'relevancy':0,
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = RisksQuerySet(params=self.query_params).get_all_risk_list()

        return Response(self.serialize(queryset)) 


class InspectionView(BaseView):#抽检信息

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
            'pubtime': data_format(r['pubtime']),
            'source':r['source'],
            'qualitied':YqjInspection.objects.filter(base_inspection=r['guid']).values('qualitied'),
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = InspectionQuerySet(params=self.query_params).get_all_inspection_list()

        return Response(self.serialize(queryset)) 


class CategoryView(BaseView):#业务信息

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


class AreaView(BaseView):#区域信息

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


class HomeView(BaseView):#主页

    def __init__(self):
        super(HomeView, self).__init__()

    def serialize(self, q1,q2,q3,q4,q5,q6):
        #print(q1,',||',q2,',||',q3,',||',q4,',||',q5,',||',q6)
        data1=map(lambda i: {'title': i['title'],'pubtime': data_format(i['pubtime']),'url': i['url']}, q1[0:10])
        data2=map(lambda i: {'title': i['title'],'pubtime': data_format(i['pubtime']),'url': i['url']}, q2[0:10])
        data3=map(lambda i: {'title': i['title'],'pubtime': data_format(i['pubtime']),'url': i['url']}, q3[0:10])
        data4=map(lambda i: {'title': i['title'],'pubtime': data_format(i['pubtime']),'url': i['url']}, q4[0:10])
        data5=map(lambda i: {'title': i['title'],'pubtime': data_format(i['pubtime']),'url': i['url']}, q5[0:10])
        data6=map(lambda i: {'title': i['title'],'pubtime': data_format(i['pubtime']),'url': i['url']}, q6[0:10])
        data={"article":data1,"event":data2,"reference":data3,"insight":data4,"risk":data5,"inspection":data6}
        return data

    def get(self, request):
        q1 = ArticlesQuerySet(params=self.query_params).get_all_article_list()#质监热点
        q2 = EventsQuerySet(params=self.query_params).get_all_event_list()#质量事件
        q3 = ReferencesQuerySet(params=self.query_params).get_all_reference_list()#信息参考
        q4 = InsightsQuerySet(params=self.query_params).get_all_insight_list()#专家视点
        q5 = RisksQuerySet(params=self.query_params).get_all_risk_list()#风险快讯
        q6 = InspectionQuerySet(params=self.query_params).get_all_inspection_list()#抽检信息

        return Response(self.serialize(q1,q2,q3,q4,q5,q6))