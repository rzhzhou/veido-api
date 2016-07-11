# -*- coding: utf-8 -*-
from django.db.models import Avg

from observer.apps.riskmonitor.models import Enterprise, ScoreEnterprise, UserIndustry
from observer.apps.riskmonitor.service.abstract import Abstract


class EnterpriseRank(Abstract):

    def __init__(self, params={}):
        super(EnterpriseRank, self).__init__(params)

    def get_enterprises(self):
        fields = ('enterprise__id', 'enterprise__name')

        args = self.set_args()

        # queryset = ScoreEnterprise.objects.filter(
        #     **args).values(*fields).annotate(Avg('score')).order_by('score__avg')
        queryset =  Enterprise.objects.filter(area__name=u'常州')

        return queryset
