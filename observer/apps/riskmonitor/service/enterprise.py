# -*- coding: utf-8 -*-
from django.db.models import Count

from observer.apps.riskmonitor.models import RiskNews, ScoreEnterprise, UserIndustry
from observer.apps.riskmonitor.service.abstract import Abstract


class EnterpriseRank(Abstract):

    def __init__(self, params={}):
        super(EnterpriseRank, self).__init__(params)

    def get_enterprises(self):
        fields = ('enterprise__id', 'enterprise__name', 'enterprise__area__name')

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'enterprise__area__name': self.focus
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = RiskNews.objects.filter(
            **args).values_list(*fields).distinct().order_by('enterprise__id')

        return queryset
