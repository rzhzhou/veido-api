import datetime
import openpyxl
from io import BytesIO

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from observer.apps.hqi.models import Policy, Area
from observer.base.service.abstract import Abstract
from observer.utils.excel import (read_by_openpyxl, write_by_openpyxl, )

# 区域
class PolicyAreaData(Abstract):

    def __init__(self, params={}):
        super(PolicyAreaData, self).__init__(params)

    def get_all(self):
        policydata = []
        cond = {
            'id': getattr(self, 'areas', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        areas = Area.objects.using('hqi').filter(policy__category='区域政策').filter(**args).annotate(num_policies=Count('policy'))
        for area in areas:
            if area.num_policies:
                a = {'id':area.name,
                    'area__id':area.id,
                    'areas__name':area.num_policies,
                    }
                policydata.append(a)
        print(policydata)
        return policydata


class PolicyAreaTotalData(Abstract):

    def __init__(self, params={}):
        super(PolicyAreaTotalData, self).__init__(params)

    def get_all(self, pid):
        fields = ('id', 'name')
        queryset = Policy.objects.using('hqi').filter(category='区域政策').filter(areas__id=pid)

        return queryset.values(*fields)


class PolicyAreaAdd(Abstract):

    def __init__(self, user, params={}):
        super(PolicyAreaAdd, self).__init__(params)
        self.user = user

    def add(self):
        areas = getattr(self, 'areas', '')
        policyname = getattr(self, 'policyname', '')

        if not Policy.objects.using('hqi').filter(category='区域政策').filter(name=policyname).exists():
            policy = Policy(
                category = '区域政策',
                industry = '',
                name = policyname,
            )
            policy.save(using='hqi')
        else:
            print('2')
            policies = Policy.objects.using('hqi').filter(category='区域政策').filter(name=policyname).values_list('id',flat=True)[0]
            policy = Policy.objects.using('hqi').get(id=policies)
            policy.industry = ''
            policy.save()

        area_id = Area.objects.using('hqi').filter(name=areas).values_list('id', flat=True)
        areas = Area.objects.using('hqi').filter(id__in=area_id)
        policy.areas.add(*areas)
        policy.save(using='hqi')



# 民营
class PolicyPrivateData(Abstract):

    def __init__(self, params={}):
        super(PolicyPrivateData, self).__init__(params)

    def get_all(self):
        policydata = []
        cond = {
            'id': getattr(self, 'areas', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        areas = Area.objects.using('hqi').filter(policy__category='民营政策').filter(**args).annotate(num_policies=Count('policy'))
        for area in areas:
            if area.num_policies:
                a = {'id':area.name,
                    'area__id':area.id,
                    'areas__name':area.num_policies,
                    }
                policydata.append(a)
        print(policydata)
        return policydata


class PolicPrivatelTotalData(Abstract):

    def __init__(self, params={}):
        super(PolicPrivatelTotalData, self).__init__(params)

    def get_all(self, pid):
        fields = ('id', 'name')
        queryset = Policy.objects.using('hqi').filter(category='民营政策').filter(areas__id=pid)

        return queryset.values(*fields)


class PolicPrivatelAdd(Abstract):

    def __init__(self, user, params={}):
        super(PolicPrivatelAdd, self).__init__(params)
        self.user = user

    def add(self):
        areas = getattr(self, 'areas', '')
        policyname = getattr(self, 'policyname', '')

        if not Policy.objects.using('hqi').filter(category='民营政策').filter(name=policyname).exists():
            policy = Policy(
                category = '民营政策',
                industry = '',
                name = policyname,
            )
            policy.save(using='hqi')
        else:
            print('2')
            policies = Policy.objects.using('hqi').filter(category='民营政策').filter(name=policyname).values_list('id',flat=True)[0]
            policy = Policy.objects.using('hqi').get(id=policies)
            policy.industry = ''
            policy.save()

        area_id = Area.objects.using('hqi').filter(name=areas).values_list('id', flat=True)
        areas = Area.objects.using('hqi').filter(id__in=area_id)
        policy.areas.add(*areas)
        policy.save(using='hqi')


# 产业
class PolicyIndustryData(Abstract):

    def __init__(self, params={}):
        super(PolicyIndustryData, self).__init__(params)

    def get_all(self):
        policydata = []
        policies = []
        cond = {
            'id': getattr(self, 'areas', None),
            'policy__industry': getattr(self, 'industry', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        areas = Area.objects.using('hqi').filter(policy__category='产业政策').annotate(num_policies=Count('policy'))
        for area in areas:
            if area.num_policies:
                for x in range(area.num_policies):
                    policiess = Policy.objects.using('hqi').filter(areas__id=area.id).filter(category='产业政策').values_list('industry',flat=True)[x]
                    policies.append(policiess)
        policy__industry = getattr(self, 'industry', None)

        for x in policies:
            if x !=policy__industry and policy__industry != '':
                continue
            areas = Area.objects.using('hqi').filter(**args).filter(policy__category='产业政策',policy__industry=x).annotate(num_policies=Count('policy'))
            for area in areas:
                if area.num_policies:
                    a = {
                        'id':area.name,
                        'industry': x,
                        'area__id':area.id,
                        'areas__name':area.num_policies,
                        }
                    if a not in policydata:
                        policydata.append(a)
                        print(a)
        return policydata


class PolicyIndustryTotalData(Abstract):

    def __init__(self, params={}):
        super(PolicyIndustryTotalData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name','industry')
        areas = getattr(self, 'area', '')
        industrys = getattr(self,'industry', '')
        queryset = Policy.objects.using('hqi').filter(category='产业政策',industry=industrys,areas__id=areas)

        return queryset.values(*fields)


class PolicyIndustryAdd(Abstract):

    def __init__(self, user, params={}):
        super(PolicyIndustryAdd, self).__init__(params)
        self.user = user

    def add(self):
        areas = getattr(self, 'areas', '')
        industrys = getattr(self,'industrys','')
        policyname = getattr(self, 'policyname', '')

        if not Policy.objects.using('hqi').filter(category='产业政策',industry=industrys).filter(name=policyname).exists():
            policy = Policy(
                category = '产业政策',
                industry = industrys,
                name = policyname,
            )
            policy.save(using='hqi')
        else:
            policies = Policy.objects.using('hqi').filter(category='产业政策',industry=industrys).filter(name=policyname).values_list('id',flat=True)[0]
            policy = Policy.objects.using('hqi').get(id=policies)
            policy.industry = industrys
            policy.save()

        policy.areas.add(areas)
        policy.save(using='hqi')


class PolicyDataUpload(Abstract):

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        #Model weight
        model = {'政策类别': 0, '政策': 0, '地域': 0}
        #sheet value
        sv = lambda x, y, z : z.cell(row=x, column=y).value
        #date format
        def date_format(df):
            try:
                return openpyxl.utils.datetime.from_excel(df)
            except Exception:
                try:
                    return str_to_date(df)
                except Exception:
                    return df

        try:
            xlsx_book = openpyxl.load_workbook(BytesIO(file_obj.read()), read_only=True)
            sheet = xlsx_book.active
            rows = sheet.rows
        except Exception as e:
            return {
                    'status': 0,
                    'message': '操作失败！请检查文件是否有误。详细错误信息：%s！' % e
                }

        total = 0
        dupli = 0

        for i, row in enumerate(rows):
            i += 1
            if i == 1:
                line = [cell.value for cell in row]
                for k in model.keys():
                    model[k] = line.index(k) + 1
            else:
                try:
                    # 政策类别
                    category = sv(i, model['政策类别'], sheet)
                    if category == 'None':
                        continue

                    # 政策
                    name = sv(i, model['政策'], sheet)
                    if name == 'None':
                        continue

                    try:
                        # 地域
                        area = sv(i, model['地域'], sheet)
                        if area == 'None':
                            continue
                        area_id = Area.objects.using('hqi').get(name = area).id


                    except Exception as e:
                        return {
                            'status': 0,
                            'message': '地域或指标不存在！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                        }


                    total += 1
                    print(category,name,area_id)
                    policy = Policy(
                        category = category,
                        name = name,
                    )
                    policy.save(using = 'hqi')
                    policy.areas.add(area_id)
                    policy.save(using = 'hqi')


                except Exception as e:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }
        return {
                    'status': 1,
                    'message': '操作成功！共处理%s条数据，新增数据%s条，更新数据%s条！' % (total, total - dupli, dupli, )
                }


class PolicyIndustryDataUpload(Abstract):

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        #Model weight
        model = {'政策类别': 0,'产业类别': 0, '政策': 0, '地域': 0}
        #sheet value
        sv = lambda x, y, z : z.cell(row=x, column=y).value
        #date format
        def date_format(df):
            try:
                return openpyxl.utils.datetime.from_excel(df)
            except Exception:
                try:
                    return str_to_date(df)
                except Exception:
                    return df

        try:
            xlsx_book = openpyxl.load_workbook(BytesIO(file_obj.read()), read_only=True)
            sheet = xlsx_book.active
            rows = sheet.rows
        except Exception as e:
            return {
                    'status': 0,
                    'message': '操作失败！请检查文件是否有误。详细错误信息：%s！' % e
                }

        total = 0
        dupli = 0

        for i, row in enumerate(rows):
            i += 1
            if i == 1:
                line = [cell.value for cell in row]
                for k in model.keys():
                    model[k] = line.index(k) + 1
            else:
                try:
                    # 政策类别
                    category = sv(i, model['政策类别'], sheet)
                    if category == 'None':
                        continue

                    # 产业类别
                    industry = sv(i, model['产业类别'], sheet)
                    if industry == 'None':
                        continue

                    name = sv(i, model['政策'], sheet)
                    if name == 'None':
                        continue

                    try:
                        # 地域
                        area = sv(i, model['地域'], sheet)
                        if area == 'None':
                            continue
                        area_id = Area.objects.using('hqi').get(name = area).id

                        # # 政策
                        # name = sv(i, model['政策'], sheet)

                        # indicator_id = Policy.objects.using('hqi').get(name = name).id

                    except Exception as e:
                        return {
                            'status': 0,
                            'message': '地域或指标不存在！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                        }


                    total += 1
                    print(category,name,area_id)
                    policy = Policy(
                        category = category,
                        industry = industry,
                        name = name,
                    )
                    policy.save(using = 'hqi')
                    policy.areas.add(area_id)
                    policy.save(using = 'hqi')


                except Exception as e:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }
        return {
                    'status': 1,
                    'message': '操作成功！共处理%s条数据，新增数据%s条，更新数据%s条！' % (total, total - dupli, dupli, )
                }




