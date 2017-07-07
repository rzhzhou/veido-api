# -*- coding: utf-8 -*-
from django.db.models import Count, Q

from observer.apps.origin.models import Inspection
from observer.apps.origin.models import Area
from observer.apps.seer.models import AreaIndustry
from observer.apps.seer.service.abstract import Abstract


class EnterpriseRank(Abstract):

    def __init__(self, params={}):
        super(EnterpriseRank, self).__init__(params)

    def get_enterprises(self):
        fields = ('enterprise_unqualified__id', 'enterprise_unqualified__name',
                  'enterprise_unqualified__area__name', 'enterprise_unqualified__product_name',
                  'enterprise_unqualified__issues')

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'enterprise_unqualified__area__id__in': Area.objects.filter(
                Q(parent__name=self.focus) |
                Q(name=self.focus)
            ).values_list('id', flat=True)
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = Inspection.objects.filter(
            **args).values_list(*fields).distinct().order_by('enterprise_unqualified__id')

        return queryset
