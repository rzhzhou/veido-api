# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import pytz
from django.db.models import Count
from django.utils import timezone

from observer.apps.corpus.models import Corpus
from observer.apps.riskmonitor.businesslogic.abstract import Abstract
from observer.apps.riskmonitor.models import (Area, RiskNews, ScoreEnterprise,
                                              ScoreIndustry, ScoreProduct)


class HomeData(Abstract):

    def __init__(self, start, end, user_id):
        self.start = start
        self.end = end
        self.user_id = user_id

    def get_time(self):
        start = datetime.strftime('%Y-%m-%d')
        end = datetime.strftime('%Y-%m-%d')
        data = {
            'time': start + '~' + end
        }

    def risk_status(self):
        data = {
            'grade': 'A',
        }
        return data

    def risk_sum(self):
        indusum = ScoreIndustry.objects.filter(
            pubtime__range=(self.start, self.end), score__gte=60).count()
        entesum = ScoreEnterprise.objects.filter(
            pubtime__range=(self.start, self.end), score__gte=60).count()
        prodsum = 6

        data = {
            'industry': {
                'amount': indusum
            },
            'enterprise': {
                'amount': entesum
            },
            'product': {
                'amount': prodsum
            }
        }
        return data

    def industry(self):
        industrys = self.risk_industry(self.start, self.end, self.user_id)
        indunames = industrys if len(industrys) < 3 else industrys[:3]
        data = {
            'industryRank': {
                'items': [{'name': induname[0], 'level':induname[1]}
                          for induname in indunames]
            }
        }
        return data

    def enterprise(self):
        type = 'abstract'
        enteobjects = self.risk_enterprise(self.start, self.end, type)
        data = {
            'enterpriseRank': {
                'items': [{'name': enteobject[0].name,
                           'level':enteobject[1]} for enteobject in enteobjects]
            }
        }
        return data

    def risk_keywords(self):
        keywords = Corpus.objects.all()
        if keywords.exists():
            keywords = keywords[0].riskword.split(' ')[0:3]
        else:
            keywords = []
        data = {
            'keywordsRank': {
                'items': [{'name': keyword, 'level': 5} for keyword in keywords]
            }
        }
        return data

    def risk_map(self):
        """
        [
            {
                "name": "北京",
                "value": 0
            },
            {
                "name": "上海",
                "value": 0
            },
            {
                "name": "广州",
                "value": 0
            },
        ]
        """

        queryset = Area.objects.filter(level=2).annotate(
            risk_news_count=Count('rarea'))
        data = {'map': [{'name': q.name, 'value': q.risk_news_count}
                        for q in queryset]}
        return data

    def risk_data(self):
        end = self.end
        start = self.start

        days = (end - start).days
        date = [(start + timedelta(days=x)) for x in xrange(days)]
        date_range = [(i.strftime('%Y-%m-%d %H:%M:%S')
                        , (i + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'
                                                            )) for i in date]

        start = end - timedelta(days=7)
        weeks = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五',
                 u'星期六', u'星期日']
        nums = self.news_nums(date_range)

        data = {
            'riskData': {
                'data': nums['data'],
                'labels': [weeks[(self.start + timedelta(days=(i + 1))
                                  ).isoweekday() - 1] for i in range(7)]
            }
        }
        return data

    def risk_level(self):
        start = self.start
        end = self.end
        weeks = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五',
                 u'星期六', u'星期日']
        data = {
            'rankData': {
                'data': ['A', 'B', 'A', 'A', 'C', 'A', 'B'],
                'labels': [weeks[(start + timedelta(days=(i + 1))).isoweekday() - 1]
                           for i in range(7)]
            }
        }
        return data

    def get_all(self):
        industryRank = self.industry().items()
        enterpriseRank = self.enterprise().items()
        keywordsRank = self.risk_keywords().items()
        risk_map = self.risk_map().items()
        riskData = self.risk_data().items()
        rankData = self.risk_level().items()
        risk_count = self.risk_sum().items()
        status = self.risk_status().items()
        datas = dict(industryRank + enterpriseRank + keywordsRank + risk_map +
                     riskData + rankData + risk_count + status)
        return datas
