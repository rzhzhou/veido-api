from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F, Q

from observer.base.models import (AliasIndustry, CCCIndustry, ConsumerIndustry,CPCIndustry,
                                  Industry, LicenceIndustry, MajorIndustry)
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

    def get_level(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level', None),
            'parent': getattr(self, 'parent', None),
            'name__icontains': getattr(self, 'text', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = CCCIndustry.objects.filter(**args).values(*fields)

        return queryset

    def get_all(self):
        fields = (
            'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
            'parent__id', 'parent__name', 'parent__desc',
            'id', 'name', 'desc',
        )

        cond = {
            'parent__parent': getattr(self, 'l1', None),
            'parent': getattr(self, 'l2', None),
            'level': 3,
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = CCCIndustry.objects.filter(
            **args).order_by('id').values(*fields)

        return queryset

    def get_by_id(self, cid):

        queryset = CCCIndustry.objects.all()

        return queryset.filter(
            level=3,
            parent__id__in=queryset.filter(
                level=2,
                parent__id=cid
            ).values_list('id', flat=True)
        )
# 产品总分类
class CpcIndustryData(Abstract):
    def __init__(self, params):
        super(CpcIndustryData, self).__init__(params)

    def get_level(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level', None),
            'parent': getattr(self, 'parent', None),
            'name__icontains': getattr(self, 'text', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = CPCIndustry.objects.filter(**args).values(*fields)

        return queryset.filter(Q(name__icontains=text)) if text else queryset

    def get_all(self):
        fields = (
            'id', 'name', 'desc', 'level',
        )

        cond = {
            'parent': getattr(self, 'parent', None),
            'level': getattr(self, 'level', None),
            'name__icontains': getattr(self, 'name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = CPCIndustry.objects.filter(
            **args).order_by('id').values(*fields)

        return queryset

    def get_by_id(self, cid):

        queryset = CPCIndustry.objects.all()

        return queryset.filter(
            level=5,
            parent__id__in=queryset.filter(
                level=4,
                parent__id=cid
            ).values_list('id', flat=True)
        )

class LicenceIndustryData(Abstract):

    def __init__(self, params):
        super(LicenceIndustryData, self).__init__(params)

    def get_level(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level', None),
            'parent': getattr(self, 'parent', None),
            'name__icontains': getattr(self, 'text', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = LicenceIndustry.objects.filter(**args).values(*fields)

        return queryset

    def get_all(self):
        fields = (
            'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
            'parent__id', 'parent__name', 'parent__desc',
            'id', 'name', 'desc',
        )

        cond = {
            'parent__parent': getattr(self, 'l1', None),
            'parent': getattr(self, 'l2', None),
            'level': 3,
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = LicenceIndustry.objects.filter(
            **args).order_by('id').values(*fields)

        return queryset

    def get_by_id(self, cid):

        queryset = LicenceIndustry.objects.all()

        return queryset.filter(
            level=3,
            parent__id__in=queryset.filter(
                level=2,
                parent__id=cid
            ).values_list('id', flat=True)
        )


class ConsumerIndustryData(Abstract):

    def __init__(self, params):
        super(ConsumerIndustryData, self).__init__(params)

    def get_level(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level'),
            'parent': getattr(self, 'parent', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = ConsumerIndustry.objects.filter(**args).values(*fields)

        return queryset.filter(Q(name__icontains=text)) if text else queryset

    def get_all(self):
        fields = (
            'parent__parent__parent__id', 'parent__parent__parent__name', 'parent__parent__parent__desc',
            'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
            'parent__id', 'parent__name', 'parent__desc',
            'id', 'name', 'desc',
        )

        cond = {
            'parent__parent__parent': getattr(self, 'l1', None),
            'parent__parent': getattr(self, 'l2', None),
            'parent': getattr(self, 'l3', None),
            'level': 4,
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = ConsumerIndustry.objects.filter(
            **args).order_by('id').values(*fields)

        return queryset


class MajorIndustryData(Abstract):

    def __init__(self, params):
        super(MajorIndustryData, self).__init__(params)

    def save(self, pk):
        objs = MajorIndustry.objects.filter(pk=pk)

        if objs:
            major = objs[0]
            major.ccc = CCCIndustry.objects.get(pk=getattr(
                self, 'ccc')) if getattr(self, 'ccc') else None
            major.licence = LicenceIndustry.objects.get(pk=getattr(
                self, 'licence')) if getattr(self, 'licence') else None
            major.save()
            return 1

        return 0

    def get_level(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level', None),
            'parent': getattr(self, 'parent', None),
            'name__icontains': getattr(self, 'text', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = MajorIndustry.objects.filter(**args).values(*fields)

        return queryset

    def get_all(self):
        fields = (
            'id', 'name', 'desc', 'level', 'licence', 'ccc',
        )

        cond = {
            'parent': getattr(self, 'parent', None),
            'level': getattr(self, 'level', None),
            'name__icontains': getattr(self, 'name', None),
            'licence__isnull': not bool(int(self.is_licence)) if getattr(self, 'is_licence') != '' else '',
            'ccc__isnull': not bool(int(self.is_ccc)) if getattr(self, 'is_ccc') != '' else '',
        }

        args = dict([k, v] for k, v in cond.items() if v != '')

        queryset = MajorIndustry.objects.filter(
            **args).order_by('id').values(*fields)

        return queryset

class Select2IndustryData(Abstract):

    def __init__(self, params):
        super(Select2IndustryData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name',)

        cond = {
            'level': getattr(self, 'level'),
            'parent': getattr(self, 'parent', None),
            'id__icontains': getattr(self, 'text', None),
            'name__icontains': getattr(self, 'text', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Industry.objects.filter(**args).values(*fields)

        return queryset


class Select2AliasIndustryData(Abstract):

    def __init__(self, params):
        super(Select2AliasIndustryData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'name',)

        text = getattr(self, 'text', None)

        queryset = AliasIndustry.objects.all().values(*fields)

        return queryset.filter(Q(id__icontains=text) | Q(name__icontains=text)) if text else queryset


class Select2CCCIndustryData(Abstract):

    def __init__(self, params):
        super(Select2CCCIndustryData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'name',)

        text = getattr(self, 'text', None)

        queryset = AliasIndustry.objects.all().values(*fields)

        return queryset.filter(Q(id__icontains=text) | Q(name__icontains=text)) if text else queryset


class Select2LicenceIndustryData(Abstract):

    def __init__(self, params):
        super(Select2LicenceIndustryData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'name',)

        text = getattr(self, 'text', None)

        queryset = AliasIndustry.objects.all().values(*fields)

        return queryset.filter(Q(id__icontains=text) | Q(name__icontains=text)) if text else queryset


class AliasIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(AliasIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        name = getattr(self, 'name', '')
        industry_id = getattr(self, 'industry_id', '')
        ccc_id = getattr(self, 'ccc_id', 0)
        licence_id = getattr(self, 'licence_id', 0)

        if not name or not industry_id:
            return 400

        if not AliasIndustry.objects.filter(name=name, industry_id=industry_id).exists():
            AliasIndustry(
                name=name,
                industry_id=industry_id,
                ccc_id=0 if not licence_id else licence_id,
                licence_id=0 if not licence_id else licence_id,
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


class LicenceIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(LicenceIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        number = getattr(self, 'number', '')
        name = getattr(self, 'name', '')
        desc = getattr(self, 'desc', '')
        level = getattr(self, 'level', 1)
        parent = getattr(self, 'parent', None)

        if not number or not name:
            return 400

        if not LicenceIndustry.objects.filter(id=number).exists():
            LicenceIndustry(
                id=number,
                name=name,
                level=level,
                desc=desc,
                parent=LicenceIndustry.objects.get(id=parent),
            ).save()

        return 200
