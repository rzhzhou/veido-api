import openpyxl
from io import BytesIO

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from observer.apps.hqi.models import Indicator,IndicatorDataParent, Area,IndicatorScore
from observer.base.service.abstract import Abstract
from observer.base.models import Area
from observer.base.service.base import (areas, indicatores )
from observer.utils.date_format import (date_format, str_to_date, get_months)
from django.contrib.auth.models import Group, User
from observer.utils.excel import (read_by_openpyxl, write_by_openpyxl, )


class IndicatorChart(Abstract):

    def __init__(self, params={}):
        super(IndicatorChart, self).__init__(params)

    def get_all(self):
        fields = ('id','parent_id__parent_id__name','parent_id__name','name')

        cond = {

        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Indicator.objects.using('hqi').filter(**args).exclude(level=-1).exclude(level=1).exclude(level=2)

        return queryset.values(*fields).order_by('index')


class IndicatorRanking(Abstract):

    def __init__(self, params={}):
        super(IndicatorRanking, self).__init__(params)

    def get_all(self, cid):
        fields = ('id','value','area_id','year','indicator_id__name','indicator_id')
        indicator_id=cid
        cond = {
        	'year': getattr(self, 'year', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = IndicatorScore.objects.using('hqi').filter(indicator_id=indicator_id).filter(**args)
        return queryset.values(*fields).order_by('-year','-value')

