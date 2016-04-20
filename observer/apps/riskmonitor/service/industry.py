# -*- coding: utf-8 -*-
from datetime import datetime

from observer.apps.riskmonitor.service.news import NewsQuerySet
from observer.apps.riskmonitor.service.analytics import AnalyticsCal
from observer.apps.riskmonitor.models import (RiskNews, UserIndustry)


class IndustryTrack(AnalyticsCal):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)

    def trend_chart(self):
        return self.industry_chart()

    def compare_chart(self):
        return self.compare(self.start, self.end, self.industry)

    def get_chart(self):
        return (self.trend_chart(), self.compare_chart())
