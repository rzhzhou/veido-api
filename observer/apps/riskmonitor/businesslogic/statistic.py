# -*- coding: utf-8 -*-
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
        result = self.news_nums(self.start, self.end, self.industry,
                                self.enterprise, self.source, self.product)
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
