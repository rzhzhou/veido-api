# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import pytz
from django.db.models import Count
from django.utils import timezone

from observer.apps.corpus.models import Corpus
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.models import (Area, RiskNews, ScoreEnterprise,
                                              ScoreIndustry, ScoreProduct)


class Dashboard(Abstract):

    def __init__(self, params={}):
        super(Dashboard, self).__init__(params)

    def get_time(self):
        start = datetime.strftime('%Y-%m-%d')
        end = datetime.strftime('%Y-%m-%d')
        data = {
            'time': start + '~' + end
        }

    def risk_status(self):
        return 'A'

    def risk_sum(self):
        i_count = ScoreIndustry.objects.filter(
            pubtime__range=(self.start, self.end), score__gte=60).count()
        e_count = ScoreEnterprise.objects.filter(
            pubtime__range=(self.start, self.end), score__gte=60).count()
        p_count = 6

        return [i_count, e_count, p_count]

    def get_industry(self):
        return self.risk_industry()[:3]

    def get_enterprise(self):
        type = 'abstract'
        return self.risk_enterprise(self.start, self.end, type)

    def risk_keywords(self):
        keywords = Corpus.objects.all()
        if keywords.exists():
            keywords = keywords[0].riskword.split()[0:3]
        else:
            keywords = []

        return keywords

    def risk_map(self):
        return Area.objects.filter(level=2).annotate(risk_news_count=Count('rarea'))

    def risk_data(self):
        days = (self.end - self.start).days
        date = [(self.start + timedelta(days=x)) for x in xrange(days)]
        date_range = [(i, (i + timedelta(days=1))) for i in date]

        result = self.cal_news_nums(date_range)

        return result[1]

    def risk_level(self):
        return ['A', 'B', 'A', 'A', 'C', 'A', 'B']

    def get_all(self):
        data = {
            'status': self.risk_status(),
            'industries': self.get_industry(),
            'enterprises': self.get_enterprise(),
            'keywords': self.risk_keywords(),
            'map': self.risk_map(),
            'risk_data': self.risk_data(),
            'rank_data': self.risk_level(),
            'risk_count': self.risk_sum()
        }
        return data
