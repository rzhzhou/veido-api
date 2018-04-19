from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Industry, CCCIndustry, LicenseIndustry, AliasIndustry
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class IndustryData(Abstract):  

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


class Select2IndustryData(Abstract):  

    def __init__(self, params):
        super(Select2IndustryData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level'),
            'parent': getattr(self, 'parent', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)
        
        queryset = Industry.objects.filter(**args).values(*fields)

        return queryset.filter(Q(id__istartswith=text) | Q(name__istartswith=text)) if text else queryset


class Select2AliasIndustryData(Abstract):  

    def __init__(self, params):
        super(Select2AliasIndustryData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'name',)

        text = getattr(self, 'text', None)

        queryset = AliasIndustry.objects.all().values(*fields)

        return queryset.filter(Q(id__istartswith=text) | Q(name__istartswith=text)) if text else queryset


class Select2CCCIndustryData(Abstract):  

    def __init__(self, params):
        super(Select2CCCIndustryData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'name',)

        text = getattr(self, 'text', None)

        queryset = AliasIndustry.objects.all().values(*fields)

        return queryset.filter(Q(id__istartswith=text) | Q(name__istartswith=text)) if text else queryset



class Select2LicenseIndustryData(Abstract):  

    def __init__(self, params):
        super(Select2LicenseIndustryData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'name',)

        text = getattr(self, 'text', None)

        queryset = AliasIndustry.objects.all().values(*fields)

        return queryset.filter(Q(id__istartswith=text) | Q(name__istartswith=text)) if text else queryset


class AliasIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(AliasIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        name = getattr(self, 'name', '')
        industry_id = getattr(self, 'industry_id', '')
        ccc_id = getattr(self, 'ccc_id', 0)
        license_id = getattr(self, 'license_id', 0)

        if not name or not industry_id:
            return 400

        if not AliasIndustry.objects.filter(name=name, industry_id=industry_id).exists():
            AliasIndustry(
                name=name,
                industry_id=industry_id,
                ccc_id=ccc_id,
                license_id=license_id,
            ).save()

        return 200


class CCCIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(CCCIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        number = getattr(self, 'number', '')
        name = getattr(self, 'name', '')
        desc = getattr(self, 'desc', '')
        level = getattr(self, 'level', 1)
        parent = getattr(self, 'parent', None)

        if not number or not name:
            return 400

        if not CCCIndustry.objects.filter(id=number).exists():
            CCCIndustry(
                id=number,
                name=name,
                level=level,
                desc=desc,
                parent=CCCIndustry.objects.get(id=parent),
            ).save()

        return 200


class LicenseIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(LicenseIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        number = getattr(self, 'number', '')
        name = getattr(self, 'name', '')
        desc = getattr(self, 'desc', '')
        level = getattr(self, 'level', 1)
        parent = getattr(self, 'parent', None)

        if not number or not name:
            return 400

        if not LicenseIndustry.objects.filter(id=number).exists():
            LicenseIndustry(
                id=number,
                name=name,
                level=level,
                desc=desc,
                parent=LicenseIndustry.objects.get(id=parent),
            ).save()

        return 200
