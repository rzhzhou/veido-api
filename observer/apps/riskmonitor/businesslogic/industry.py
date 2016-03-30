# -*- coding: utf-8 -*-
from datetime import datetime

from observer.apps.riskmonitor.businesslogic.abstract import Abstract
from observer.apps.riskmonitor.businesslogic.statistic import Statistic


class IndustryTrack(Abstract):

    def __init__(self, params={}):
        for k, v in params.iteritems():
            setattr(self, k, v)

    def trend_chart(self):
        news_trend = Statistic(industry=self.industry, start=self.start, enterprise=self.enterprise,
                                product=self.product, source=self.source,
                               end=self.end).industry_chart()
        trend = {
            'labels': news_trend['date'],
            'data': news_trend['data']
        }
        return trend

    def compare_chart(self):
        compare = self.compare(self.start, self.end, self.industry)
        bar = {
            'name': [u'同比', u'环比'],
            'show': 'true',
            'lables': [compare['date']],
            'data': [compare['data']]
        }
        return bar

    def news_data(self):
        start = self.start
        end = self.end
        industry = '%%' if self.industry == None or self.industry == None else self.industry
        enterprise = '%%' if self.enterprise == None or self.enterprise == None else self.enterprise
        source = '%%' if self.source == None or self.source == None else self.source
        product = '%%' if self.product == None or self.product == None else self.product

        source_data = self.source_data(industry, enterprise,
                                       product, source,
                                       start, end, self.page)
        data = {
            'title': [u'序号', u'标题', u'来源', u'发表时间'],
            'items': source_data['items'],
            'total': source_data['total']
        }
        return data

    def get_chart(self):
        trends = self.trend_chart()
        bar = self.compare_chart()
        data = {
            'trend': trends,
            'bar': bar
        }
        return data
