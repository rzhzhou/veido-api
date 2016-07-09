# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, timedelta

from django.conf import settings

from observer.apps.crawler.models import Task


class CrawlerTask(object):

    def __init__(self, uuid, industry, riskwords, invalidwords):
        self.uuid = str(uuid)
        self.industry = industry
        self.riskwords = riskwords
        self.invalidwords = invalidwords
        self.source = {
            'baidu': '"%s" +%s -(%s)',
            # 'weibo': ('%s %s', 21600, 'zjld.weibo.newstitle',),
            # 'sogou': ('+%s+%s', 21600, 'zjld.sogou.keywords',),
            # 'sogou': ('"%s" +%s -(%s)', 21600, 'zjld.sogou.newstitle',)
        }

    def build(self):
        for k, v in self.source.items():
            for riskword in self.riskwords:
                data = {
                    'url': v % (self.industry, riskword, " | ".join(self.invalidwords)),
                    'source': k,
                }

                self.insert(data)

    def insert(self, data):
        tz = pytz.timezone(settings.TIME_ZONE)
        params = {
            'app': 'seer',
            'module': '',
            'crawlerimpl': 'baidu',
            'rank': 1,
            'url': data.get('url'),
            'data': {
                "last_info": {
                    "pubtime": tz.localize(datetime(2015, 1, 1))
                },
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

    def update(self, corpus):
        self.remove(corpus)
        self.build()

    def remove(self, corpus):
        for v in self.source.itervalues():
            for riskword in corpus.riskword.split():
                url = v % (corpus.industry, riskword,
                           " | ".join(corpus.invalidword.split()))
                Task.objects.using('crawler').filter(url=url).delete()
