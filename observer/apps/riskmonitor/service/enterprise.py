# -*- coding: utf-8 -*-
from django.db.models import Avg

from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.models import (ScoreEnterprise, UserIndustry)


class EnterpriseRank(Abstract):

    def __init__(self, params={}):
        super(EnterpriseRank, self).__init__(params)

    def get_enterprises(self):
        fields = ('enterprise__id', 'enterprise__name')

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = ScoreEnterprise.objects.filter(
            **args).values(*fields).annotate(Avg('score')).order_by('score__avg')

        return queryset
