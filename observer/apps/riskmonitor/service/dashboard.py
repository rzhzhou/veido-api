# -*- coding: utf-8 -*-
import random

from datetime import datetime, timedelta

from django.db.models import Count, Q

from observer.apps.riskmonitor.models import (Area, Product, RiskNews,
                                              ScoreEnterprise, ScoreIndustry,
                                              ScoreProduct)
from observer.apps.riskmonitor.service.analytics import AnalyticsCal


class Dashboard(AnalyticsCal):

    def __init__(self, params={}):
        super(Dashboard, self).__init__(params)

    @property
    def map(self):
        provinces = list(Area.objects.filter(level=2).values('id', 'name'))
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

    @property
    def risk_level(self):
        self.days = (self.end - self.start).days

        cal_date_func = lambda x: (
            self.start + timedelta(days=x),
            self.start + timedelta(days=x + 1)
        )

        date_range = map(cal_date_func, xrange(self.days))

        date_range_len = len(date_range)
        if date_range_len <= 10:
            area_days = date_range[date_range_len - 6::]
            date = map(lambda x: x[1].strftime('%m-%d'), area_days)
        elif date_range_len <= 30:
            area_days = date_range[::5]
            date = map(lambda x: x[1].strftime('%m-%d'), area_days)
        elif date_range_len <= 190:
            area_days = date_range[::31]
            date = map(lambda x: x[1].strftime('20%y-%m'), area_days)
        elif date_range_len <= 370:
            area_days = date_range[::61]
            date = map(lambda x: x[1].strftime('20%y-%m'), area_days)

        area_score = []
        for index in area_days:

            pubtime = index[0].strftime('%Y-%m-%d')

            try:
                total_score = self.get_overall_overview_score(pubtime=pubtime)[
                    0]
            except:
                total_score = random.randint(60, 100)

            area_score.append(total_score)
        return (date, zip(date, area_score))

    @property
    def risk_product(self):
        products = self.get_industries()

        if len(products) >= 5:
            products = reversed(products[:5])
            return zip(*products)
        else:
            return ((), (), ())

    @property
    def risk_product_trend(self):
        pass

    def get_all(self):
        data = {
            'map': self.map,
            'risk': self.industry_chart(),
            'risk_level': self.risk_level,
            'risk_product': self.risk_product,
            'risk_product_trend': self.risk_product_trend,
            'summaries_score': self.get_overall_overview_score(),
        }
        return data
