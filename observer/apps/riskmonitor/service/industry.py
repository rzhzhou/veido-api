# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Avg

from observer.apps.riskmonitor.service.news import NewsQuerySet
from observer.apps.riskmonitor.service.analytics import AnalyticsCal
from observer.apps.riskmonitor.models import (
    RiskNews, ScoreIndustry, UserIndustry)


class IndustryTrack(AnalyticsCal):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)

    def trend_chart(self):
        return self.industry_chart()

    def compare_chart(self):
        return self.compare(self.start, self.end, self.industry)

    def get_chart(self):
        return (self.trend_chart(), self.compare_chart())

    def get_industries(self):
        industries = []

        user_industries = UserIndustry.objects.filter(user__id=self.user_id)

        for u in user_industries:
            queryset = ScoreIndustry.objects.filter(
                pubtime__gte=self.start,
                pubtime__lt=self.end,
                industry=u.industry.id
            )

            score = queryset.aggregate(Avg('score'))[
                'score__avg'] if queryset else 100

            industries.append((u.industry.id, u.name, round(score)))

        return sorted(industries, key=lambda industry: industry[2])
