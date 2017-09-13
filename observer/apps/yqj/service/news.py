# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.seer.models import IndustryScore
from observer.apps.base.models import Article
from observer.apps.seer.models import Area
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time

class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_all_news_list(self):
        fields = ('id', 'title', 'pubtime', 'source','area', 'url')
       
        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'category__id': getattr(self, 'category_id', None),
            'title__contains': getattr(self, 'search[value]', None),
            'area': Area.objects.filter(pk =getattr(self, 'area_id', None))
        }

        args = dict([k,v] for k, v in cond.iteritems() if v)
        if cond['category__id'] or cond['area']:
            queryset =Article.objects.filter(**args).values(*fields)
        else:
            args['category__name'] = '质监热点'
            print args
            queryset =Article.objects.filter(**args).values(*fields)
        return queryset
        