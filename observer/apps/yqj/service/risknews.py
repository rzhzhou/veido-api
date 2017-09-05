# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.origin.models import IndustryScore
from observer.apps.yqj.models import Article, Risk
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class RiskNewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(RiskNewsQuerySet, self).__init__(params)


    def get_all_news_list(self, starttime=None, endtime=None):
        fields = ('id', 'title', 'pubtime', 'source')

        args = {
            'pubtime__gte': self.starttime,
            'pubtime__lt': self.endtime,
        }

            
        queryset = Risk.objects.filter(**args).values(*fields)

        return queryset
        