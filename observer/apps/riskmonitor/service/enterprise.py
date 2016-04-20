# -*- coding: utf-8 -*-
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.models import (ScoreEnterprise, UserIndustry)


class EnterpriseRank(Abstract):

    def __init__(self, params={}):
        super(EnterpriseRank, self).__init__(params)

    def enterprise_rank(self):
        fields = ('enterprise__id', 'enterprise__name', 'score')

        try:
            self.industry = UserIndustry.objects.get(
                id=self.industry).industry.id
        except UserIndustry.DoesNotExist:
            self.industry = None

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': self.industry,
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = ScoreEnterprise.objects.filter(
            **args).order_by('score').values(*fields)

        return queryset
