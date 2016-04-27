# -*- coding: utf-8 -*-
from django.db.models import Count

from observer.apps.riskmonitor.service.industry import IndustryTrack

from observer.apps.riskmonitor.models import RiskNews, UserIndustry, Enterprise, Product


class AnalyticsCal(IndustryTrack):

    def __init__(self, params={}):
        super(AnalyticsCal, self).__init__(params)

    def get_filters(self):
        args = self.set_args()

        industries = UserIndustry.objects.filter(
            user__id=self.user_id).values('id', 'name')

        enterprises = []

        products = []

        publishers = RiskNews.objects.filter(
            **args).values('publisher__id', 'publisher__publisher')

        return (industries, enterprises, products, publishers)

    def industry_chart(self):
        return self.trend_chart()

    def keywords_chart(self, num):
        args = self.set_args()

        queryset = RiskNews.objects.filter(**args).values_list('risk_keyword__name').annotate(
            Count('risk_keyword__name')).order_by('-risk_keyword__name__count')[:num]

        if not queryset:
            return [[], []]

        return zip(*queryset)

    def get_chart(self):
        data = {
            'trend': self.industry_chart(),
            'bar': self.keywords_chart(num=10),
            'source': self.sources()
        }
        return data

    def get_all(self):
        chart_data = self.get_chart()
        chart_data['list'] = self.get_news_list()

        return chart_data
