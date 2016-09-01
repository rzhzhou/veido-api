# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Count, Q

from observer.apps.riskmonitor.models import (Area, Product, RiskNews,
                                              ScoreEnterprise, ScoreIndustry,
                                              ScoreProduct)
from observer.apps.riskmonitor.service.analytics import AnalyticsCal


class Dashboard(AnalyticsCal):

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
            user__id=self.user_id
        ).values_list('industry').distinct().count()
        e_count = ScoreEnterprise.objects.filter(
            pubtime__gte=self.start,
            pubtime__lt=self.end,
            score__lt=90,
            user__id=self.user_id
        ).values_list('enterprise').distinct().count()

        p_count = Product.objects.count()

        return [i_count, e_count, p_count]

    def risk_keywords(self):
        return self.keywords_chart(num=3)

    @property
    def map(self):
        provinces = Area.objects.filter(level=2).values('id', 'name')
        risknews_area = zip(
            *list(
                RiskNews.objects.filter(
                    pubtime__gte=self.start,
                    pubtime__lt=self.end
                ).exclude(
                    area=None
                ).values_list(
                    'area__id',
                    'area__parent__id'
                )
            )
        )  # area__id = risknews_area[0], area__parent__id = risknews_area[1]

        for province in provinces:
            cities_id = list(
                Area.objects.filter(
                    parent__id=province['id']
                ).values_list(
                    'id',
                    flat=True
                )
            )

            areas_id = cities_id + [province['id']]

            province['count'] = sum([
                sum(
                    map(
                        lambda x: risknews_area[0].count(x),
                        areas_id
                    )
                ),
                sum(
                    map(
                        # area__parent__id__in=cities_id
                        lambda x: risknews_area[1].count(x),
                        cities_id
                    )
                )
            ])

        return provinces

    def risk_data(self):
        self.days = (self.end - self.start).days

        cal_date_func = lambda x: (
            self.start + timedelta(days=x),
            self.start + timedelta(days=x + 1)
        )

        date_range = map(cal_date_func, xrange(self.days))

        result = self.cal_news_nums(date_range, 'day')

        date = map(lambda x: x[1].strftime('%m-%d'), date_range)

        return (date, result[1])

    def risk_level(self):
        self.days = (self.end - self.start).days

        cal_date_func = lambda x: (
            self.start + timedelta(days=x),
            self.start + timedelta(days=x + 1)
        )

        date_range = map(cal_date_func, xrange(self.days))

        result = self.cal_news_nums(date_range, 'day')

        level = []
        for number in result[1]:
            if number < 333:
                level.append(0)
            elif number < 666:
                level.append(1)
            else:
                level.append(2)

        date = map(lambda x: x[1].strftime('%m-%d'), date_range)

        return (date, zip(date, level))

    def risk_product(self):
        products = self.get_industries()
        if len(products) >= 5:
            products = reversed(products[:5])
            return zip(*products)
        else:
            return ((), (), ())

    def get_all(self):
        data = {
            'status': self.risk_status(),
            'industries': self.get_industries()[:3],
            'keywords': self.risk_keywords(),
            'map': self.map,
            'risk_data': self.risk_data(),
            'risk_level': self.risk_level(),
            'risk_count': self.risk_number(),
            'risk_product': self.risk_product(),
            'summaries_score': self.get_overall_overview_score(),
        }
        return data
