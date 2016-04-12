# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, timedelta

from django.conf import settings
from observer.utils.connector.mongo import MongodbQuerApi


class CrawlerTask(object):

    def __init__(self, uuid, industry, riskwords, invalidwords, collection, stype):
        self.uuid = uuid
        self.industry = industry
        self.riskwords = riskwords
        self.invalidwords = invalidwords
        self.collection = collection
        self.stype = stype
        self.source = {
            'baidu': ('"%s" +%s -(%s)', 21600, 'zjld.baidu.newstitle',),
            # 'weibo': ('%s %s', 21600, 'zjld.weibo.newstitle',),
            # 'sogou': ('+%s+%s', 21600, 'zjld.sogou.keywords',),
            # 'sogou': ('"%s" +%s -(%s)', 21600, 'zjld.sogou.newstitle',)
        }

    def build(self):
        for source, sdata in self.source.items():
            for riskword in self.riskwords:
                data = {
                    'key': sdata[0] % (self.industry, riskword, " | ".join(self.invalidwords)),
                    'interval': sdata[1],
                    'type': sdata[2],
                    'source': source,
                }

                self.insert(data)

    def insert(self, data):
        tz = pytz.timezone(settings.TIME_ZONE)
        conf = {
            "id": str(self.uuid),
            "type": data.get('type', ''),
            "status": data.get('status', 0),
            "priority": data.get('priority', 3),
            "interval": data.get('interval', 7200),
            "update_time": datetime.utcnow(),
            "lastrun": datetime.utcfromtimestamp(0),
            "nextrun": datetime.utcnow(),
            "crtetime": datetime.utcnow(),
            "timeout": 3600,
            "key": data.get('key'),
            "data": {
                "last_info": {
                    "pubtime": tz.localize(datetime(2015, 1, 1))
                },
                "industry": self.industry,
                "source_type": self.stype,
                "source": data.get('source', '')
            }
        }

        MongodbQuerApi(self.collection).save(conf)

    def update(self, uuid):
        cond = {
            'id': self.uuid
        }
        MongodbQuerApi(self.collection).delete(cond)
        self.build()

    def remove(self, uuid):
        cond = {
            'id': self.uuid
        }
        MongodbQuerApi(self.collection).delete(cond)
