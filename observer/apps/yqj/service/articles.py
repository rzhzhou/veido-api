from observer.apps.base.models import Article as BaseArticle
from observer.apps.yqj.models import Article as YqjArticle
from observer.apps.seer.service.abstract import Abstract

# 质监热点
class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_all_new_list(self):

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
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class EventsQuerySet(Abstract):

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
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class ReferencesQuerySet(Abstract):

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
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class InsightsQuerySet(Abstract):

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
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class RisksQuerySet(Abstract):

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
        fields = ('url', 'title', 'pubtime', 'source','score',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class CategoryQuerySet(Abstract):

    def __init__(self, params={}):
        super(CategoryQuerySet, self).__init__(params)

    def get_all_category_list(self,id):
        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__id': id,
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source','reprinted','area')
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class AreaQuerySet(Abstract):

    def __init__(self, params={}):
        super(AreaQuerySet, self).__init__(params)

    def get_all_area_list(self,id):
        # base article query
        fields = ('url', 'title', 'pubtime', 'source','reprinted','area')
        cond = {
            'area__id': id,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset