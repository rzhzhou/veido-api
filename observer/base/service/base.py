from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Industry, CCCIndustry, LicenseIndustry
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class IndustryData(Abstract):  # 行业列表

    def __init__(self, params):
        super(IndustryData, self).__init__(params)

    def get_all(self):
        cond = {
            'parent__parent': getattr(self, 'l1', None),
            'parent': getattr(self, 'l2', None),
            'id': getattr(self, 'l3', None), 
            'level': 3,
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Industry.objects.filter(**args).order_by('id')

        return queryset


class CCCIndustryData(Abstract):

    def __init__(self, params):
        super(CCCIndustryData, self).__init__(params)

    def get_all(self):
        return None

    def get_by_id(self, cid):

        queryset = CCCIndustry.objects.all()

        return queryset.filter(
                    level=3, 
                    parent__id__in=queryset.filter(
                        level=2, 
                        parent__id=cid
                        ).values_list('id', flat=True)
                )


class LicenseIndustryData(Abstract):

    def __init__(self, params):
        super(LicenseIndustryData, self).__init__(params)

    def get_all(self):
        return None

    def get_by_id(self, cid):

        queryset = LicenseIndustry.objects.all()

        return queryset.filter(
                    level=3, 
                    parent__id__in=queryset.filter(
                        level=2, 
                        parent__id=cid
                        ).values_list('id', flat=True)
                )


class Select2IndustryData(Abstract):  # 获取行业名称

    def __init__(self, params):
        super(Select2IndustryData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name',)

        cond = {
            'id__istartswith': getattr(self, 'text', None),
            'name__istartswith': getattr(self, 'text', None),
            'level': getattr(self, 'level'),
            'parent': getattr(self, 'parent', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        
        queryset = Industry.objects.filter(**args).values(*fields)

        return queryset
