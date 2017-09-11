# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.origin.models import IndustryScore
from observer.apps.yqj.models import Article, Category
from observer.apps.seer.models import Area
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time

class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_all_news_list(self):
        fields = ('id', 'title', 'pubtime', 'publisher_id','area', 'url')
        '''
        args={
            'pubtime__gte': starttime,
            'pubtime__lt': endtime,
        }

        queryset =''

        if category_id != 'null' and category_id is not None:
            # args['category__id'] = category_id
            # category = Category.objects.get(pk =category_id)
            # queryset = category.articles.filter(**args).values(*fields)
            queryset = Article.objects.filter(category__id = category_id).filter(**args).values(*fields)
        elif area_id != 'null' and area_id is not None:
            args['area'] =Area.objects.filter(pk =area_id)
            queryset = Article.objects.filter(**args).values(*fields)
        else:
            args['category__name'] ='质监热点'
            queryset = Article.objects.filter(**args).values(*fields)
        '''
        # area_id = 
        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'category__id': getattr(self, 'category_id', None),
            # 'category__name':'质监热点',
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
        