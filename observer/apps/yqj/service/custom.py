# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.origin.models import IndustryScore
from observer.apps.yqj.models import CustomKeyword, Custom
from observer.apps.seer.models import Area
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time

class CustomQuerySet(Abstract):

    def __init__(self, params={}):
        super(CustomQuerySet, self).__init__(params)

    def get_all_news_list(self, starttime=None, endtime=None, custom_id=None):
        fields = ('id', 'title', 'pubtime', 'publisher', 'url')

        args={
            'pubtime__gte': self.starttime,
            'pubtime__lt': self.endtime,
        }

        # queryset = CustomKeyword.objects.get(pk =custom_id).custom.articles.filter(**args).values(*fields)
        # print queryset.query
        queryset = Custom.objects.get(customkeyword__id = custom_id).articles.filter(**args).values(*fields)

        return queryset
        