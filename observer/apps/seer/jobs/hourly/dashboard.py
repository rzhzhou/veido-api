# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django_extensions.management.jobs import HourlyJob

from observer.apps.seer.service.dashboard import Dashboard
from observer.apps.seer.models import Cache, CacheConf
from observer.utils.date.convert import utc_to_local_time, get_days, get_start_end


class Job(HourlyJob):
    help = "Get Dashboard job."

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.cache_conf_name = self.__module__.split('.')[-1]

    def generate_query_params(self, cache_conf):
        cache_conf.params = eval(cache_conf.params)
        days = cache_conf.days

        query_params = {
            'cache_conf_name': cache_conf.name,
            'days': cache_conf.days,
            'level': cache_conf.params['level'],
            'area': cache_conf.params['area'],
            'user_id': cache_conf.params['user_id'],
            'start': utc_to_local_time(self.today - timedelta(days=cache_conf.days)),
            'end': utc_to_local_time(self.today)
        }

        if days in [180, 360]:
            start_end = get_start_end(days)
            query_params['start'] = utc_to_local_time(start_end[0])
            query_params['end'] = utc_to_local_time(start_end[1])

        return query_params

    def generate_cache_name(self, query_params):
        name = query_params['cache_conf_name']
        start = query_params['start'].strftime('%Y-%m-%d')
        end = query_params['end'].strftime('%Y-%m-%d')
        level = query_params['level']
        user = query_params['user_id']
        area = query_params.get('area', u'常州')
        return u'%s.%s.%s.%s.%s.%s' % (name, start, end, level, user, area)

    @property
    def cache_confs(self):
        return CacheConf.objects.filter(name=self.cache_conf_name)

    def execute(self):
        for cache_conf in self.cache_confs:
            query_params = self.generate_query_params(cache_conf)
            cache_name = self.generate_cache_name(query_params)

            Cache.objects.update_or_create(
                k=cache_name,
                defaults={
                    'v': Dashboard(params=query_params).get_all()
                }
            )