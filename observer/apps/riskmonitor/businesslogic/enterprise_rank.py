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
        self.ente_rank()

