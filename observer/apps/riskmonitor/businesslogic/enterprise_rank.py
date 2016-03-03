# -*- coding: utf-8 -*-
from observer.apps.riskmonitor.businesslogic.abstract import(
    Abstract, )


class EnterpriseRank(Abstract):

    def __init__(self, start=None, end=None, industry=None):
        self.start = start
        self.end = end
        self.industry = industry

    def ente_rank(self):
        result = self.enterprise_rank(self.start, self.end, self.industry)
        return result

    def get_all(self):
        items = self.ente_rank()
        data = {
            'list': {
                'title': [u'排名', u'企业排名', u'风险信息总数', u'等级'],
                'items': items['data'],
                'total': items['total']
            }
        }
        return data
