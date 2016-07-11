# -*- coding: utf-8 -*-
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from observer.apps.origin.models import Inspection
from observer.apps.riskmonitor.models import (
    RiskNews, ScoreIndustry, UserIndustry, Industry, ManageIndex, SocietyIndex, ConsumeIndex)
from observer.apps.riskmonitor.service.news import NewsQuerySet


class IndustryTrack(NewsQuerySet):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)

    def trend_chart(self):
        self.days = (self.end - self.start).days

        # less than equal 4 months (122 = 31 + 31 + 30 + 30)
        if self.days > 0 and self.days <= 122:
            result = self.cal_date_range('day')
            result['categories'] = [i.strftime('%m-%d') for i in result['categories']]

        elif self.days > 122:  # great than 4 months
            result = self.cal_date_range('month')
            result['categories'] = [i.strftime('%Y-%m') for i in result['categories']]

        return result

    def compare_chart(self):
        return self.compare(self.start, self.end, self.industry)

    def get_chart(self):
        return (self.trend_chart(), self.compare_chart())

    def get_dimension(self):
        c_dimension = get_object_or_404(
            ConsumeIndex, industry__id=self.industry)
        s_dimension = get_object_or_404(
            SocietyIndex, industry__id=self.industry)
        m_dimension = get_object_or_404(
            ManageIndex, industry__id=self.industry)

        return (c_dimension, s_dimension, m_dimension)

    def get_source(self):
        risknews = RiskNews.objects.filter(industry__id=self.industry)
        inspections = Inspection.objects.filter(industry__id=self.industry)

        return (risknews, inspections)

    def get_all(self):
        data = {
            'indicators': self.get_dimension(),
            'source': self.get_source(),
            'trend': self.trend_chart()
        }
        return data

    def get_industries(self):
        industries = []

        cond = {
            'user__id': self.user_id,
            'industry__name': self.name,
            'industry__level': self.level,
            'industry__parent__id': self.parent
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        user_industries = UserIndustry.objects.filter(**args)

        for u in user_industries:
            queryset = ScoreIndustry.objects.filter(
                pubtime__gte=self.start,
                pubtime__lt=self.end,
                industry=u.industry.id
            )

            score = queryset.aggregate(Avg('score'))[
                'score__avg'] if queryset else 100

            industries.append((u.industry.id, u.name, u.industry.level, round(score)))

        return sorted(industries, key=lambda industry: industry[2])
