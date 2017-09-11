# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.seer.models import IndustryScore
from observer.apps.base.models import Article
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class EventQuerySet(Abstract):

    def __init__(self, params={}):
        super(EventQuerySet, self).__init__(params)




    def get_all_news_list(self):
        fields = ('id', 'title', 'pubtime', 'source', 'area')


        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains' : getattr(self, 'search[value]', None)
        }

        args = dict([k,v] for k, v in cond.iteritems() if v)
        # if (starttime != "null" and starttime is not None) or \
        #     (endtime !="null" and endtime is not None):
        #     args['pubtime__range'] = (starttime,endtime)

            
        queryset = Event.objects.filter(**args).values(*fields)

        return queryset