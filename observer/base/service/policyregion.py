import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from observer.apps.hqi.models import Policy,PolicyData, Area
from observer.base.service.abstract import Abstract

# 区域
class PolicyAreaData(Abstract):

    def __init__(self, params={}):
        super(PolicyAreaData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'area__id','total','year')

        pid= PolicyData.objects.using('hqi').filter(policy_class=1).values_list('id', flat=True)
        for x in pid:
            policydatas = PolicyData.objects.using('hqi').get(id=x)
            tatals= PolicyData.objects.using('hqi').filter(id=x).values('id','policys__name').count()
            policydatas.total=tatals
            policydatas.save()


        cond = {
            'id': getattr(self, 'id', None),
            'area': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = PolicyData.objects.using('hqi').filter(policy_class=1)
        queryset = queryset.filter(**args)

        return queryset.values(*fields).order_by('-year')


class PolicyAreaTotalData(Abstract):

    def __init__(self, params={}):
        super(PolicyAreaTotalData, self).__init__(params)

    def get_all(self, pid):
        fields = ('id', 'policys__name')
        queryset = PolicyData.objects.using('hqi').filter(policy_class=1).filter(id=pid)

        return queryset.values(*fields).order_by('-year')


class PolicyAreaAdd(Abstract):

    def __init__(self, user, params={}):
        super(PolicyAreaAdd, self).__init__(params)
        self.user = user

    def add(self):
        year = getattr(self, 'year', '')
        areas = getattr(self, 'areas', '')
        policyname = getattr(self, 'policyname', '')

        if not year:
            year = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not Policy.objects.using('hqi').filter(name=policyname).exists():
            policy = Policy(
                name = policyname,
            )
            policy.save(using='hqi')




        if not PolicyData.objects.using('hqi').filter(policy_class=1).filter(area_id=areas).exists():
            policydata = PolicyData(
                policy_class = 1,
                year = year,
                area_id = areas,
            )
            policydata.save(using='hqi')
        else:
            policydataids=PolicyData.objects.using('hqi').filter(policy_class=1,area_id=areas).values_list('id',flat=True)[0]
            policydata = PolicyData.objects.using('hqi').get(id=policydataids)
            policydata.year = year
            policydata.save()


        policy_id = Policy.objects.using('hqi').filter(name=policyname).values_list('id', flat=True)
        policys = Policy.objects.using('hqi').filter(id__in=policy_id)
        policydata.policys.add(*policys)

        policydata.save(using='hqi')


        return 200

# 民营
class PolicyPrivateData(Abstract):

    def __init__(self, params={}):
        super(PolicyPrivateData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'area__id','total','year')

        pid= PolicyData.objects.using('hqi').filter(policy_class=2).values_list('id', flat=True)
        for x in pid:
            policydatas = PolicyData.objects.using('hqi').get(id=x)
            tatals= PolicyData.objects.using('hqi').filter(id=x).values('id','policys__name').count()
            policydatas.total=tatals
            policydatas.save()


        cond = {
            'id': getattr(self, 'id', None),
            'area': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = PolicyData.objects.using('hqi').filter(policy_class=2)
        queryset = queryset.filter(**args)

        return queryset.values(*fields).order_by('-year')


class PolicPrivatelTotalData(Abstract):

    def __init__(self, params={}):
        super(PolicPrivatelTotalData, self).__init__(params)

    def get_all(self, pid):
        fields = ('id', 'policys__name')
        queryset = PolicyData.objects.using('hqi').filter(policy_class=2).filter(id=pid)

        return queryset.values(*fields).order_by('-year')


class PolicPrivatelAdd(Abstract):

    def __init__(self, user, params={}):
        super(PolicPrivatelAdd, self).__init__(params)
        self.user = user

    def add(self):
        year = getattr(self, 'year', '')
        areas = getattr(self, 'areas', '')
        policyname = getattr(self, 'policyname', '')

        if not year:
            year = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not Policy.objects.using('hqi').filter(name=policyname).exists():
            policy = Policy(
                name = policyname,
            )
            policy.save(using='hqi')




        if not PolicyData.objects.using('hqi').filter(policy_class=2).filter(area_id=areas).exists():
            policydata = PolicyData(
                policy_class = 2,
                year = year,
                area_id = areas,
            )
            policydata.save(using='hqi')
        else:
            policydataids=PolicyData.objects.using('hqi').filter(policy_class=2,area_id=areas).values_list('id',flat=True)[0]
            policydata = PolicyData.objects.using('hqi').get(id=policydataids)
            policydata.year = year
            policydata.save()


        policy_id = Policy.objects.using('hqi').filter(name=policyname).values_list('id', flat=True)
        policys = Policy.objects.using('hqi').filter(id__in=policy_id)
        policydata.policys.add(*policys)

        policydata.save(using='hqi')


        return 200

# 产业
class PolicyIndustryData(Abstract):

    def __init__(self, params={}):
        super(PolicyIndustryData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'area__id','industry_class','total','year')

        pid= PolicyData.objects.using('hqi').filter(policy_class=3).values_list('id', flat=True)
        for x in pid:
            policydatas = PolicyData.objects.using('hqi').get(id=x)
            tatals= PolicyData.objects.using('hqi').filter(id=x).values('id','policys__name').count()
            policydatas.total=tatals
            policydatas.save()


        cond = {
            'id': getattr(self, 'id', None),
            'area': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = PolicyData.objects.using('hqi').filter(policy_class=3)
        queryset = queryset.filter(**args)

        return queryset.values(*fields).order_by('-year')


class PolicyIndustryTotalData(Abstract):

    def __init__(self, params={}):
        super(PolicyIndustryTotalData, self).__init__(params)

    def get_all(self, pid):
        fields = ('id', 'policys__name')
        queryset = PolicyData.objects.using('hqi').filter(policy_class=3).filter(id=pid)

        return queryset.values(*fields).order_by('-year')


class PolicyIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(PolicyIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        year = getattr(self, 'year', '')
        areas = getattr(self, 'areas', '')
        industrys = getattr(self,'industrys', '')
        policyname = getattr(self, 'policyname', '')

        if not year:
            year = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not Policy.objects.using('hqi').filter(name=policyname).exists():
            policy = Policy(
                name = policyname,
            )
            policy.save(using='hqi')




        if not PolicyData.objects.using('hqi').filter(policy_class=3).filter(area_id=areas).exists():
            policydata = PolicyData(
                policy_class = 3,
                year = year,
                industry_class = industrys,
                area_id = areas,
            )
            policydata.save(using='hqi')
        else:
            policydataids=PolicyData.objects.using('hqi').filter(policy_class=3,area_id=areas).values_list('id',flat=True)[0]
            policydata = PolicyData.objects.using('hqi').get(id=policydataids)
            policydata.year = year
            policydata.save()


        policy_id = Policy.objects.using('hqi').filter(name=policyname).values_list('id', flat=True)
        policys = Policy.objects.using('hqi').filter(id__in=policy_id)
        policydata.policys.add(*policys)

        policydata.save(using='hqi')


        return 200



