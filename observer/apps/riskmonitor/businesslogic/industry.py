# -*- coding: utf-8 -*-
from observer.apps.riskmonitor.businesslogic.abstract import(
    Abstract, )
from observer.apps.riskmonitor.businesslogic.statistic import Statistic


class IndustryTrack(Abstract):

    def __init__(self, industry=None, enterprise=None, product=None, source=None,
                 start=None, end=None, page=1):
        self.start = start
        self.end = end
        self.industry = industry
        self.enterprise = enterprise
        self.product = product
        self.source = source
        self.page = page

    def trend_chart(self):
        news_trend = Statistic(industry=self.industry, start=self.start,
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
        source_data = self.source_data(self.industry, self.enterprise,
                                       self.product, self.source,
                                       self.start, self.end, self.page)
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
