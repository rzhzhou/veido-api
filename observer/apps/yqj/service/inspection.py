from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.yqj.models import Inspection
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class InspectionQuerySet(Abstract):

    def __init__(self, params={}):
        super(InspectionQuerySet, self).__init__(params)


    def get_all_news_list(self, starttime=None, endtime=None):
        fields = ('inspection__id', 'inspection__title', 'inspection__product',
         'qualitied', 'inspection__source', 'inspection__pubtime', 'inspection__url')


        cond = {
            'inspection__pubtime__gte': getattr(self, 'starttime', None),
            'inspection__pubtime__lt': getattr(self, 'endtime', None),
            'inspection__title__contains' : getattr(self, 'search[value]', None)
        }

        args =dict([k,v] for k, v in cond.items() if v)
        queryset = Inspection.objects.filter(**args).values(*fields)
        return queryset
