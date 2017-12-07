from observer.apps.base.models import Article as BaseArticle, Area
from observer.apps.yqj.models import Article as YqjArticle
from observer.apps.seer.service.abstract import Abstract
from datetime import datetime, timedelta
from django.db.models import Count
from observer.utils.date.convert import data_format


class NewsQuerySet(Abstract):  # 质监热点

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_all_news_list(self):

        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'reprinted', 'area', )
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class EventsQuerySet(Abstract):  # 质量事件

    def __init__(self, params={}):
        super(EventsQuerySet, self).__init__(params)

    def get_all_event_list(self):

        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'reprinted', 'area', )
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class ReferencesQuerySet(Abstract):  # 信息参考

    def __init__(self, params={}):
        super(ReferencesQuerySet, self).__init__(params)

    def get_all_reference_list(self):

        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class InsightsQuerySet(Abstract):  # 专家视点

    def __init__(self, params={}):
        super(InsightsQuerySet, self).__init__(params)

    def get_all_insight_list(self):

        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class RisksQuerySet(Abstract):  # 风险快讯

    def __init__(self, params={}):
        super(RisksQuerySet, self).__init__(params)

    def get_all_risk_list(self):
        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'score',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class CategoryQuerySet(Abstract):  # 业务信息

    def __init__(self, params={}):
        super(CategoryQuerySet, self).__init__(params)

    def get_all_category_list(self, id):
        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__id': id,
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'reprinted', 'area')
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class AreaQuerySet(Abstract):  # 区域状况

    def __init__(self, params={}):
        super(AreaQuerySet, self).__init__(params)

    def get_all_area_list(self, id):
        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'reprinted', 'area')
        cond = {
            'area__id': id,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset


class NewsCount(Abstract):  # 质监热点占比

    def __init__(self, params={}):
        super(NewsCount, self).__init__(params)

    def get_NewsCount():
        cond = {
            'category__level': 1,
            'category__name': '质监热点',
        }
        newsCount = YqjArticle.objects.filter(**cond).count()
        articleCount = BaseArticle.objects.all().count()
        data = {'newsCount': newsCount, 'articleCount': articleCount}
        return data


class EventCount(Abstract):  # 质量事件占比

    def __init__(self, params={}):
        super(EventCount, self).__init__(params)

    def get_EventCount():
        cond = {
            'category__level': 1,
            'category__name': '质量事件',
        }
        eventCount = YqjArticle.objects.filter(**cond).count()
        articleCount = BaseArticle.objects.all().count()
        data = {'eventCount': eventCount, 'articleCount': articleCount}
        return data


class LineData(Abstract):  # 数据概览

    def __init__(self, params={}):
        super(LineData, self).__init__(params)

    def show(self):
        def getCount(feeling_type, starttime, endtime):
            fields = ('pubtime',)
            cond = {
                'pubtime__gte': starttime,
                'pubtime__lt': endtime,
            }

            if feeling_type == 'positive':  # 正面的
                cond['feeling_factor__gt'] = 0
            elif feeling_type == 'negative':  # 负面的
                cond['feeling_factor__lt'] = 0
            else:  # 中立的
                cond['feeling_factor'] = 0
            queryset = BaseArticle.objects.filter(
                **cond).values_list('pubtime').annotate(num_pubtime=Count('pubtime'))
            return queryset
        count1 = getCount('positive', getattr(
            self, 'starttime', None), getattr(self, 'endtime', None))
        count2 = getCount('netrual', getattr(
            self, 'starttime', None), getattr(self, 'endtime', None))
        count3 = getCount('negative', getattr(
            self, 'starttime', None), getattr(self, 'endtime', None))
        data = {}

        data['time'] = {'starttime': self.starttime.strftime(
            "%m-%d"), 'endtime': self.endtime.strftime("%m-%d")}
        if len(count1) != 0:
            data['positive'] = map(lambda i: {'pubtime': data_format(
                i[0]), 'count': i[1]}, count1)
        if len(count2) != 0:
            data['netrual'] = map(lambda i: {'pubtime': data_format(
                i[0]), 'count': i[1]}, count2)
        if len(count3) != 0:
            data['negative'] = map(lambda i: {'pubtime': data_format(
                i[0]), 'count': i[1]}, count3)
        return data


class PieData(Abstract):  # 区域状况

    def __init__(self, params={}):
        super(PieData, self).__init__(params)

    def pieCount(self):
        # base article query
        area_parentId = Area.objects.filter(
            name=self.area).values('id')
        area_result = Area.objects.filter(
            parent=area_parentId[0].get('id')).values('id','name')
        area_sonId=[]
        area_sonName=[]
        for a in area_result:
            area_sonId.append(a.get('id'))
            area_sonName.append(a.get('name'))
        cond = {
            'area__id__in': area_sonId,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        data1={}
        i=0;
        length=len(area_sonId);
        data={}
        while i<length:
            cond['area__id']=area_sonId[i]
            args = dict([k, v] for k, v in cond.items() if v)
            queryset = BaseArticle.objects.filter(
                **args).count()
            data[area_sonName[i]]=queryset
            i=i+1
        return data
