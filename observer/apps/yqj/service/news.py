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
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
            'title__contains': getattr(self, 'search[value]', None),
            'area__name__contains': getattr(self, 'area_name', None)
        }

        args = dict([k,v] for k, v in cond.iteritems() if v)
        queryset =Article.objects.filter(**args).values(*fields).order_by('-pubtime')
        return queryset
        