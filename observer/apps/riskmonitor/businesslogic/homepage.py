# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.utils import timezone

from observer.apps.riskmonitor.models import(
    ScoreIndustry, ScoreEnterprise, ScoreProduct, )
from observer.apps.corpus.models import(
    Corpus, )
from observer.apps.riskmonitor.businesslogic.abstract import(
    Abstract, )


class HomeData(Abstract):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_time(self):
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
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
        type = 'abstract'
        indunames = self.risk_industry(self.start, self.end, type)
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
        keywords = keywords[0].riskword.split(' ')[0:3]
        data = {
            'keywordsRank': {
                'items': [{'name': keyword, 'level': 5} for keyword in keywords]
            }
        }
        return data

    def risk_data(self):
        end = self.end
        start = end - timedelta(days=7)
        weeks = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五',
                 u'星期六', u'星期日']
        nums = self.news_nums(start, end)
        data = {
            'riskData': {
                'data': nums['data'],
                'labels': [weeks[(end + timedelta(days=(i + 1))).isoweekday() - 1]
                           for i in range(7)]
            }
        }
        return data

    def risk_level(self):
        type = 'abstract'
        end = timezone.now()
        start = end - timedelta(days=7)
        weeks = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五',
                 u'星期六', u'星期日']
        data = {
            'rankData': {
                'data': ['A', 'B', 'A', 'A', 'C', 'A', 'B'],
                'labels': [weeks[(end + timedelta(days=(i + 1))).isoweekday() - 1]
                           for i in range(7)]
            }
        }
        return data

    def get_all(self):
        industryRank = self.industry().items()
        enterpriseRank = self.enterprise().items()
        keywordsRank = self.risk_keywords().items()
        riskData = self.risk_data().items()
        rankData = self.risk_level().items()
        risk_count = self.risk_sum().items()
        status = self.risk_status().items()
        # time = self.get_time().items()
        datas = dict(industryRank + enterpriseRank + keywordsRank +
                     riskData + rankData + risk_count + status)
        return datas
