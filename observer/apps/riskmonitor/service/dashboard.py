# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Count, Q

from observer.apps.riskmonitor.models import (Area, Product, RiskNews,
                                              ScoreEnterprise, ScoreIndustry,
                                              ScoreProduct)
from observer.apps.riskmonitor.service.enterprise import EnterpriseRank
from observer.apps.riskmonitor.service.analytics import AnalyticsCal


class Dashboard(AnalyticsCal, EnterpriseRank):

    def __init__(self, params={}):
        super(Dashboard, self).__init__(params)

    def get_time(self):
        start = datetime.strftime('%Y-%m-%d')
        end = datetime.strftime('%Y-%m-%d')
        data = {
            'time': start + '~' + end
        }

    def risk_status(self):
        return 'A'

    def risk_number(self):
        i_count = ScoreIndustry.objects.filter(
            pubtime__gte=self.start,
            pubtime__lt=self.end,
            score__lt=90,
            user__id= self.user_id
        ).values_list('industry').distinct().count()
        e_count = ScoreEnterprise.objects.filter(
            pubtime__gte=self.start,
            pubtime__lt=self.end,
            score__lt=90,
            user__id= self.user_id
        ).values_list('enterprise').distinct().count()

        p_count = Product.objects.count()

        return [i_count, e_count, p_count]

    def risk_keywords(self):
        return self.keywords_chart(num=3)

    def risk_map(self):
        queryset = Area.objects.filter(level=2).values('id', 'name')

        for q in queryset:
            areas_id = Area.objects.filter(
                parent__id=q['id']).values_list('id', flat=True)
            q['count'] = RiskNews.objects.filter(
                Q(pubtime__gte=self.start) &
                Q(pubtime__lt=self.end),
                Q(area__id=q['id']) |
                Q(area__id__in=areas_id) |
                Q(area__parent__id__in=areas_id)
            ).count()

        return queryset

    def risk_data(self):
        weeks = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']
        self.days = (self.end - self.start).days

        cal_date_func = lambda x: (
            self.start + timedelta(days=x),
            self.start + timedelta(days=x + 1)
        )

        date_range = map(cal_date_func, xrange(self.days))

        result = self.cal_news_nums(date_range, 'day')

        date = map(lambda x: x[1].strftime('%m-%d'), date_range)
        if self.days == 7:
            date = [weeks[(self.start + timedelta(days=(i + 1))).isoweekday() - 1]
                        for i in range(7)]


        return (result[1], date)

    def risk_level(self):
        return [0, 1, 0, 0, 2, 0, 1]

    def risk_product(self):
        products = self.get_industries()[0]
        if len(products) >= 5:
            products = products[:5]
        return zip(*products)

    def get_all(self):
        data = {
            'status': self.risk_status(),
            'industries': self.get_industries()[:3],
            'enterprises': self.get_enterprises()[:3],
            'keywords': self.risk_keywords(),
            'map': self.risk_map(),
            'risk_data': self.risk_data(),
            'rank_data': self.risk_level(),
            'risk_count': self.risk_number(),
            'risk_product': self.risk_product(),
        }
        return data
