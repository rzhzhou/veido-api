# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.origin.models import IndustryScore
from observer.apps.yqj.models import Article, Risk, Topic
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class EventQuerySet(Abstract):

    def __init__(self, params={}):
        super(EventQuerySet, self).__init__(params)




    def get_all_news_list(self, starttime=None, endtime=None):
        fields = ('id', 'title', 'pubtime', 'source', 'area')


        args = {

        }

        if (starttime != "null" and starttime is not None) or \
            (endtime !="null" and endtime is not None):
            args['pubtime__range'] = (starttime,endtime)

            
        queryset = Topic.objects.filter(**args).values(*fields)

        return queryset