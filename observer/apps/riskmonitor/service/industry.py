# -*- coding: utf-8 -*-
from django.db.models import Avg

from observer.apps.riskmonitor.models import (RiskNews, ScoreIndustry,
                                              UserIndustry)
from observer.apps.riskmonitor.service.news import NewsQuerySet


class IndustryTrack(NewsQuerySet):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)

    def trend_chart(self):
        self.days = (self.end - self.start).days

        # less than equal 4 months (122 = 31 + 31 + 30 + 30)
        if self.days > 0 and self.days <= 122:
            result = self.cal_date_range('day')
            result['date'] = [i.strftime('%m-%d') for i in result['date']]

        elif self.days > 122:  # great than 4 months
            result = self.cal_date_range('month')
            result['date'] = [i.strftime('%Y-%m') for i in result['date']]

        return result

    def compare_chart(self):
        return self.compare(self.start, self.end, self.industry)

    def get_chart(self):
        return (self.trend_chart(), self.compare_chart())

    def get_industries(self):
        thead = [u'排名', u'产品类别', u'风险等级', u'产品状态']
        level = 3
        if int(self.level) == 2:
            thead = [u'排名', u'二级行业', u'风险等级', u'行业状态']
            level = 2
        elif int(self.level) == 1:
            thead = [u'排名', u'一级行业', u'风险等级', u'行业状态']
            level = 1

        industries = []

        user_industries = UserIndustry.objects.filter(user__id=self.user_id,
            industry__level=self.level)

        for u in user_industries:
            queryset = ScoreIndustry.objects.filter(
                pubtime__gte=self.start,
                pubtime__lt=self.end,
                industry=u.industry.id
            )

            score = queryset.aggregate(Avg('score'))[
                'score__avg'] if queryset else 100

            industries.append((u.id, u.name, round(score)))

        return [thead, level, sorted(industries, key=lambda industry: industry[2])]
