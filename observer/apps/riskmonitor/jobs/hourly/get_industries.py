# -*- coding: utf-8 -*-
import os
from datetime import date, datetime, timedelta

from django_extensions.management.jobs import HourlyJob

from observer.apps.riskmonitor.service.industry import IndustryTrack
from observer.apps.riskmonitor.models import Cache
from observer.utils.date.convert import utc_to_local_time


class Job(HourlyJob):
    help = "Get Level 3 Industries job."

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.days = 30
        self.query_params = {
            'name': None,
            'level': 3,
            'parent': None,
            'start': utc_to_local_time(self.today - timedelta(days=self.days)),
            'end': utc_to_local_time(self.today),
            'area': u'全国',
            'user_id': 9  # changzhou
        }

    @property
    def cache_name(self):
        func = os.path.basename(__file__)[:-3]
        level = self.query_params['level']
        days = self.days
        area = self.query_params['area']
        user_id = self.query_params['user_id']
        return u'%s.%s.%s.%s.%s' % (func, level, days, area, user_id)

    def get_cache(self):
        return Cache.objects.filter(k=self.cache_name)

    def execute(self):
        queryset = self.get_cache()
        if queryset:
            cache = queryset[0]
            cache.v = IndustryTrack(params=self.query_params).get_industries()
        else:
            cache = Cache(
                k=self.cache_name,
                v=IndustryTrack(params=self.query_params).get_industries()
            )
        cache.save()
