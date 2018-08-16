# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, timedelta

from django.conf import settings

from observer.base.models import Task
from observer.utils.date_format import datetime_to_timestamp


class CrawlerTask(object):

    def __init__(self, industry, riskword):
        self.industry = industry
        self.riskword = riskword
        self.source = {
            'baidu': '"%s" +%s',
            # 'weibo': ('%s %s', 21600, 'zjld.weibo.newstitle',),
            # 'sogou': ('+%s+%s', 21600, 'zjld.sogou.keywords',),
            # 'sogou': ('"%s" +%s -(%s)', 21600, 'zjld.sogou.newstitle',)
        }

    def build(self):
        for k, v in self.source.items():
            data = {
                'syntax': v % (self.industry, self.riskword),
                'source': k,
            }

            self.insert(data)

    def insert(self, data):
        tz = pytz.timezone(settings.TIME_ZONE)
        params = {
            'app': 'seer',
            'sub_app': '',
            'file': 'baidu',
            'rank': 1,
            'url': data.get('syntax'),
            'data': {
                "last_pubtime": datetime_to_timestamp(datetime(2015, 1, 1)),
                "industry": self.industry,
                "source": data.get('source'),
                'source_type': u'行业监测',
            },
            'priority': 0,
            'interval': 3600,
            'timeout': 3600,
            'last_run': datetime.min.replace(tzinfo=pytz.utc),
            'next_run': datetime.utcnow().replace(tzinfo=pytz.utc),
            'status': 0
        }

        task = Task(**params)
        task.save(using='crawler')

    def remove(self):
        for k, v in self.source.items():
            data = {
                'syntax': v % (self.industry, self.riskword),
                'source': k,
            }
            Task.objects.using('crawler').filter(url=data.get('syntax')).delete()
