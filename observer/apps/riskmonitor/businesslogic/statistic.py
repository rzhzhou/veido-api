# -*- coding: utf-8 -*-
import pytz
import time
from datetime import datetime, timedelta

from observer.apps.riskmonitor.businesslogic.abstract import(
    Abstract, )


class Statistic(Abstract):

    def __init__(self, start=None, end=None, industry='%%', enterprise='%%',
                 source='%%', product='%%', page=1):
        self.start = start
        self.end = end
        self.industry = industry
        self.enterprise = enterprise
        self.source = source
        self.product = product
        self.page = page

    def industry_statistic(self):
        days = (self.end - self.start).days

        start = self.start.astimezone(pytz.utc)
        start = time.strftime('%Y-%m-%d %X', start.timetuple())
        start = datetime.strptime(start, '%Y-%m-%d %X')

        def date_range(interval):
            scale = days / interval + days % interval
            list_range = [(i + 1) * interval for i in xrange(scale)]
            date = [(start + timedelta(days=x)) for x in list_range]
            date_range = [(i, i + timedelta(days=interval)) for i in date]
            return {'date_range': date_range, 'date': date}

        if days > 0 and days <= 7:
            date_range = date_range(1)
        elif days > 7 and days <= 20:
            date_range = date_range(2)
        elif days > 20 and days <= 40:
            date_range = date_range(4)
        elif days > 40 and days <= 60:
            date_range = date_range(7)
        elif days > 60 and days <= 80:
            date_range = date_range(10)
        elif days > 80 and days <= 100:
            date_range = date_range(15)
        elif days > 100 and days <= 120:
            date_range = date_range(20)
        elif days > 120 and days <= 365:
            date_range =date_range(30)
        else:
            date_range = date_range(365)

        result = self.news_nums(date_range['date_range'], self.industry,
                                self.enterprise, self.source, self.product)
        date = map(lambda x: x.strftime("%m-%d"), date_range['date'])
        result['date'] = date
        return result

    def keywords(self):
        bar = {
            "name": [u"关键字"],
            "show": "false",
            "labels": [u"辐射大", u"爆炸", u"频闪", u"甲醛", u"有毒",
                       u"防腐剂", u"死亡", u"人工色素", u"致癌", u"重金属"],
            "data": [["180", "160", "140", "130", "120", "110", "100",
                      "90", "80", "70"]]
        }
        return bar

    def get_all(self):
        indu_sta = self.industry_statistic()
        keywords_sta = self.keywords()
        sources = self.sources()
        industry = None if self.industry == '%%' else self.industry
        enterprise = None if self.enterprise == '%%' else self.enterprise
        source = None if self.source == '%%' else self.source
        product = None if self.product == '%%' else self.product
        news_data = self.source_data(industry, enterprise, product,
                                     source, self.start, self.end, self.page)
        data = {
            'trend': {
                'labels': indu_sta['date'],
                'data': indu_sta['data']
            },
            'bar': keywords_sta,
            'source': {
                'labels': sources['labels'],
                'data': sources['data']
            },
            'list': {
                'title': [u'序号', u'标题', u'来源', u'发表时间'],
                'items': news_data['items']
            },
            'total': news_data['total']
        }
        return data
