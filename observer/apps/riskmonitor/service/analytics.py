# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import pytz

from observer.apps.riskmonitor.service.news import NewsQuerySet
from observer.utils.date.tz import utc_to_local_time


class AnalyticsCal(NewsQuerySet):

    def __init__(self, params={}):
        super(AnalyticsCal, self).__init__(params)

    def industry_chart(self):
        days = (self.end - self.start).days
        start = self.start

        def all_result(interval):
            scale = days / interval + days % interval
            list_range = [(i + 1) * interval for i in xrange(scale)]
            date = [(start + timedelta(days=(x - 1))) for x in list_range]
            date_range = [(i, (i + timedelta(days=interval))) for i in date]

            result = self.news_nums(date_range)

            data = {}
            for k, v in result.iteritems():
                data[utc_to_local_time(
                    datetime.strptime(k, '%Y-%m-%d %H:%M:%S'))] = v

            result = zip(*sorted(data.items(), key=lambda data: data[0]))

            return {
                'date': result[0],
                'data': result[1]
            }

        if days > 0 and days <= 7:
            result = all_result(1)
            result['date'] = [i.strftime("%m-%d") for i in result['date']]
        elif days > 7 and days <= 20:
            result = all_result(2)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=1)).strftime("%m-%d") for i in result['date']]
        elif days > 20 and days <= 40:
            result = all_result(4)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=3)).strftime("%m-%d") for i in result['date']]
        elif days > 40 and days <= 60:
            result = all_result(7)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=6)).strftime("%m-%d") for i in result['date']]
        elif days > 60 and days <= 80:
            result = all_result(10)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=9)).strftime("%m-%d") for i in result['date']]
        elif days > 80 and days <= 100:
            result = all_result(15)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=14)).strftime("%m-%d") for i in result['date']]
        elif days > 100 and days <= 120:
            result = all_result(20)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=19)).strftime("%m-%d") for i in result['date']]
        elif days > 120 and days <= 365:
            result = all_result(30)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=29)).strftime("%m-%d") for i in result['date']]
        else:
            result = all_result(365)
            result['date'] = [i.strftime(
                "%m-%d") + '~' + (i + timedelta(days=364)).strftime("%m-%d") for i in result['date']]
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
