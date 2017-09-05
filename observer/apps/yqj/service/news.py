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

    def get_all_news_list(self, starttime=None, endtime=None, category_id=None, area_id=None):
        fields = ('id', 'title', 'pubtime', 'publisher_id')

        args={
            'pubtime__gte': self.starttime,
            'pubtime__lt': self.endtime,
        }

        queryset =''

        if category_id != 'null' and category_id is not None:
            # args['category__id'] = category_id
            category = Category.objects.get(pk =category_id)
            queryset = category.articles.filter(**args).values(*fields)
            # queryset = Article.categorys
        elif area_id != 'null' and area_id is not None:
            args['area'] =Area.objects.filter(pk =area_id)
            queryset = Article.objects.filter(**args).values(*fields)
        else:
            args['category__name'] ='质监热点'
            queryset = Article.objects.filter(**args).values(*fields)
        
        # category = CategoryTwo.objects.get(name='信息参考')
        # queryset = category.articletwos.filter(**args).values(*fields)

        return queryset
        