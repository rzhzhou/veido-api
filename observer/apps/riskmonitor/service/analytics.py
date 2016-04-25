# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import pytz

from observer.apps.riskmonitor.service.industry import IndustryTrack


class AnalyticsCal(IndustryTrack):

    def __init__(self, params={}):
        super(AnalyticsCal, self).__init__(params)

    def industry_chart(self):
        return self.trend_chart()

    def keywords_chart(self):
        bar = {
            'name': [u'关键字'],
            'show': 'false',
            'labels': [u'辐射大', u'爆炸', u'频闪', u'甲醛', u'有毒',
                       u'防腐剂', u'死亡', u'人工色素', u'致癌', u'重金属'],
            'data': [['180', '160', '140', '130', '120', '110', '100',
                      '90', '80', '70']]
        }
        return bar

    def get_chart(self):
        data = {
            'trend': self.industry_chart(),
            'bar': self.keywords_chart(),
            'source': self.sources()
        }
        return data

    def get_all(self):
        chart_data = self.get_chart()
        chart_data['list'] = self.get_news_list()

        return chart_data
