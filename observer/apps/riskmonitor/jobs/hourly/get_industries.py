# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from django_extensions.management.jobs import HourlyJob

from observer.apps.riskmonitor.service.industry import IndustryTrack
from observer.apps.riskmonitor.models import Cache, CacheConf
from observer.utils.date.convert import utc_to_local_time


class Job(HourlyJob):
    help = "Get Level 3 Industries job."

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.cache_conf_name = self.__module__.split('.')[-1]

    def generate_query_params(self, cache_conf):
        cache_conf.params = eval(cache_conf.params)

        query_params = {
            'cache_conf_name': cache_conf.name,
            'days': cache_conf.days,
            'level': cache_conf.params['level'],
            'area': cache_conf.params['area'],
            'user_id': cache_conf.params['user_id'],
            'name': None,
            'parent': None,
            'start': utc_to_local_time(self.today - timedelta(days=cache_conf.days)),
            'end': utc_to_local_time(self.today)
        }

        return query_params

    def generate_cache_name(self, query_params):
        name = query_params['cache_conf_name']
        days = query_params['days']
        level = query_params['level']
        area = query_params['area']
        user = query_params['user_id']
        return u'%s.%s.%s.%s.%s' % (name, days, level, area, user)

    @property
    def cache_confs(self):
        return CacheConf.objects.filter(name=self.cache_conf_name)

    def execute(self):
        for cache_conf in self.cache_confs:
            query_params = self.generate_query_params(cache_conf)
            cache_name = self.generate_cache_name(query_params)

            Cache.objects.update_or_create(
                k=cache_name,
                v=IndustryTrack(params=query_params).get_industries()
            )
