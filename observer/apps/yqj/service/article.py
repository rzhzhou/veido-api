# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.origin.models import IndustryScore
from observer.apps.yqj.models import Article, Category
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time

class ArticleQuerySet(Abstract):

    def __init__(self, params={}):
        super(ArticleQuerySet, self).__init__(params)

    # def get_news_list(self, search_value, industry=None, publisher=None):
    #     fields = ('id', 'title', 'pubtime', 'url', 'risk_keyword', 'invalid_keyword', 'publisher__name', 'industry__name')

    #     max_id = Article.objects.all().aggregate(Max('id'))

    #     args = {
    #         'id__lte': max_id.get('id__max'),
    #         # 'is_delete': False,
    #     }

    #     if search_value:
    #         args['title__contains'] = search_value
            
    #     if publisher != "null" and publisher is not None:
    #         args['publisher__id'] = publisher

    #     if industry != "null" and industry is not None:
    #         args['industry'] = industry

    #     queryset = Article.objects.filter(**args).values(*fields)

    #     return queryset

    def get_all_news_list(self, starttime=None, endtime=None, category_id=None):
        fields = ('id', 'title', 'pubtime', 'source', 'area')

        # max_id = Article.objects.all().aggregate(Max('id'))

        args = {
            # 'id__lte': max_id.get('id__max'),
            # 'category_id':category_id 
            
        }

        if category_id != 'null' and category_id is not None:
            args['category__id'] = category_id
        
        if (starttime != "null" and starttime is not None) or \
            (endtime !="null" and endtime is not None):
            args['pubtime__range'] = (starttime,endtime)


            
        queryset = Article.objects.filter(**args).values(*fields)

        return queryset