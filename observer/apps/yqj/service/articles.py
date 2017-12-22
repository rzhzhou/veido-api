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
        fields = ('guid', 'url', 'title', 'pubtime',
                  'source', 'reprinted', 'area', )
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'area__name': getattr(self, 'area', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
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
        fields = ('guid', 'url', 'title', 'pubtime',
                  'source', 'reprinted', 'area', )
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'area__name': getattr(self, 'area', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
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
        fields = ('guid', 'url', 'title', 'pubtime', 'source',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
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
        fields = ('guid', 'url', 'title', 'pubtime', 'source',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
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
        fields = ('guid', 'url', 'title', 'pubtime', 'source', 'score',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
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
        fields = ('guid', 'url', 'title', 'pubtime',
                  'source', 'reprinted', 'area')
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'area__name': getattr(self, 'area', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
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
        fields = ('guid', 'url', 'title', 'pubtime',
                  'source', 'reprinted', 'area')
        cond = {
            'area__id': id,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset
