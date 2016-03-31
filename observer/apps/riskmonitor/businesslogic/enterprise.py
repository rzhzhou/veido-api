# -*- coding: utf-8 -*-
from observer.apps.riskmonitor.businesslogic.abstract import Abstract


class EnterpriseRank(Abstract):

    def __init__(self, params={}):
        for k, v in params.iteritems():
            setattr(self, k, v)

    def ente_rank(self):
        start = self.start
        end = self.end
        result = self.enterprise_rank(
            start=start, end=end,
            industry=self.industry if self.industry else '%%', page=self.page)
        return result

    def get_all(self):
        items = self.ente_rank()
        data = {
            'title': [u'排名', u'企业名称', u'风险信息总数', u'等级'],
            'items': items['data'],
            'total': items['total']
        }
        return data
