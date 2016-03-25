# -*- coding: utf-8 -*-
import pytz
import time
from datetime import datetime, timedelta

from observer.apps.riskmonitor.businesslogic.abstract import(
    Abstract, )


class Statistic(Abstract):

    def __init__(self, start=None, end=None, industry=None, enterprise=None,
                 source=None, product=None, page=1):
        self.start = start
        self.end = end
        self.industry = industry
        self.enterprise = enterprise
        self.source = source
        self.product = product
        self.page = page

    def industry_chart(self):
        days = (self.end - self.start).days
        start = self.start

        def all_result(interval):
            industry = '%%' if self.industry == 0 or self.industry == None else self.industry
            enterprise = '%%' if self.enterprise == 0 or self.enterprise == None else self.enterprise
            source = '%%' if self.source == 0 or self.source == None else self.source
            product = '%%' if self.product == 0 or self.product == None else self.product

            scale = days / interval + days % interval
            list_range = [(i + 1) * interval for i in xrange(scale)]
            date = [(start + timedelta(days=(x - 1))) for x in list_range]
            date_range = [(i.strftime('%Y-%m-%d %H:%M:%S'),
                           (i + timedelta(days=interval)).strftime(
                '%Y-%m-%d %H:%M:%S')) for i in date]

            result = self.news_nums(date_range, industry,
                                    enterprise, source, product)

            date = self.utc_to_local_time(date)

            result['date'] = date
            return result

        if days > 0 and days <= 7:
            result = all_result(1)
            result['date'] = [i.strftime("%m-%d") for i in result['date']]
        elif days > 7 and days <= 20:
            result = all_result(2)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=1)).strftime("%m-%d") for i in result['date']]
        elif days > 20 and days <= 40:
            result = all_result(4)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=3)).strftime("%m-%d") for i in result['date']]
        elif days > 40 and days <= 60:
            result = all_result(7)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=6)).strftime("%m-%d") for i in result['date']]
        elif days > 60 and days <= 80:
            result = all_result(10)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=9)).strftime("%m-%d") for i in result['date']]
        elif days > 80 and days <= 100:
            result = all_result(15)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=14)).strftime("%m-%d") for i in result['date']]
        elif days > 100 and days <= 120:
            result = all_result(20)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=19)).strftime("%m-%d") for i in result['date']]
        elif days > 120 and days <= 365:
            result = all_result(30)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=29)).strftime("%m-%d") for i in result['date']]
        else:
            result = all_result(365)
            result['date'] = [i.strftime(
                "%m-%d") + '~' +(i + timedelta(days=364)).strftime("%m-%d") for i in result['date']]
        return result

    def keywords_chart(self):
        bar = {
            "name": [u"关键字"],
            "show": "false",
            "labels": [u"辐射大", u"爆炸", u"频闪", u"甲醛", u"有毒",
                       u"防腐剂", u"死亡", u"人工色素", u"致癌", u"重金属"],
            "data": [["180", "160", "140", "130", "120", "110", "100",
                      "90", "80", "70"]]
        }
        return bar

    def get_chart(self):
        indu_sta = self.industry_chart()
        keywords_sta = self.keywords_chart()
        sources = self.sources()

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
        }
        return data

    def get_data(self):
        start = self.start
        end = self.end
        industry = '%%' if self.industry == 0 or self.industry == None else self.industry
        enterprise = '%%' if self.enterprise == 0 or self.enterprise == None else self.enterprise
        source = '%%' if self.source == 0 or self.source == None else self.source
        product = '%%' if self.product == 0 or self.product == None else self.product
        news_data = self.source_data(industry, enterprise, product,
                                     source, start, end, self.page)
        data = {
            'title': [u'序号', u'标题', u'来源', u'发表时间'],
            'items': news_data['items'],
            'total': news_data['total']
        }
        return data

    def get_all(self):
        chart_data = self.get_chart()
        data = self.get_data()
        chart_data['list'] = data
        return chart_data
