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
        fields = ('id', 'title', 'pubtime', 'source', 'area')

        args={}

        if category_id != 'null' and category_id is not None:
            args['category__id'] = category_id
        elif area_id != 'null' and area_id is not None:
            args['area'] =Area.objects.filter(pk =area_id)
        else:
            args = {
                'category__name':'质监热点',
                
            }

        
        if (starttime != "null" and starttime is not None) or \
            (endtime !="null" and endtime is not None):
            args['pubtime__range'] = (starttime,endtime)


        
        queryset = Article.objects.filter(**args).values(*fields)
    

        return queryset