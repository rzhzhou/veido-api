# -*- coding: utf-8 -*-
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.models import (RiskNews, UserIndustry)


class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_news_list(self):
        fields = ('id', 'title', 'pubtime', 'publisher__publisher')

        try:
            self.industry = UserIndustry.objects.get(id=self.industry).industry.id
        except UserIndustry.DoesNotExist:
            self.industry = None

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': self.industry,
            'enterprise__id': self.enterprise,
            'publisher__id': self.source
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset
