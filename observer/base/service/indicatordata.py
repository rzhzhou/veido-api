import openpyxl
from io import BytesIO

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from observer.apps.hqi.models import Indicator,IndicatorDataParent, Area
from observer.base.service.abstract import Abstract
from observer.base.models import Area
from observer.base.service.base import (areas, indicatores )
from observer.utils.date_format import (date_format, str_to_date, get_months)
from django.contrib.auth.models import Group, User
from observer.utils.excel import (read_by_openpyxl, write_by_openpyxl, )


class IndicatorData(Abstract):

    def __init__(self, params={}):
        super(IndicatorData, self).__init__(params)

    def get_all(self):
        fields = ('id','indicator__parent_id__parent_id__name', 'indicator__parent_id__name','indicator__name', 'value' ,'indicator__unit','indicator__level' , 'area__id', 'year')

        cond = {
            'indicator__parent_id__parent_id__id':getattr(self,'Indicator_l1',None),
            'indicator__parent_id__id':getattr(self,'Indicator_l2',None),
            'indicator__id':getattr(self,'Indicator_l3',None),
            'indicator__name': getattr(self, 'indicator_name', None),
            'year': getattr(self, 'year', None),
            'area': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = IndicatorDataParent.objects.using('hqi').filter(**args).exclude(indicator__level=-1)

        return queryset.values(*fields)  # order_by('indicator_id')

    def get_level(self):
        fields = ('id', 'name')

        cond = {
            'level': getattr(self, 'level', None),
            'parent': getattr(self, 'parent', None),
            'name__icontains': getattr(self, 'name', None),
        }

        text = getattr(self, 'text', None)

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Indicator.objects.using('hqi').filter(**args).exclude(name='None').values(*fields)

        return queryset



class IndicatorDelete(Abstract):
    def __init__(self, user, params={}):
        super(IndicatorDelete, self).__init__(params)
        self.user = user

    def delete(self, cid):
        del_ids = cid
        print(del_ids)

        for id in del_ids.split(","):
            IndicatorDataParent.objects.using('hqi').filter(id=id).delete()


class IndicatorDataUpload(Abstract):

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        #Model weight
        model = {'值': 0, '年份': 0, '指标': 0, '地域': 0}
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
                    #值
                    value = sv(i, model['值'], sheet)
                    # if value == 'None':
                    #     continue

                    #年份
                    year = sv(i, model['年份'], sheet)
                    # if year == 'None':
                    #     continue

                    # pubtime = str(date_format(sv(i, model['发布时间'], sheet))).strip()
                    # if pubtime == 'None':
                    #     pubtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                    # 地域
                    # area = str(sv(i, model['地域'], sheet)).strip()
                    # if area == 'None':
                    #     continue
                    # else:
                    #     areas = area.split()
                    #     a_ids = Area.objects.filter(name__in=areas).values_list('id', flat=True)

                    #     if len(areas) != len(a_ids):
                    #         return {
                    #             'status': 0,
                    #             'message': '操作失败！请检查第 %s 行 "地域"！' % (i + 1, )
                    #         }

                    #     area = Area.objects.filter(id__in=a_ids)

                    area = sv(i, model['地域'], sheet)
                    # if area == 'None':
                    #     continue
                    area_id =Indicator.objects.using('hqi').get(name=area).id

                    # 指标类别
                    indicator = sv(i, model['指标'], sheet)
                    print('indicator', indicator)
                    # if indicator == 'None':
                    #     continue
                    # else:
                    #     indicatores = indicator.split()
                    #     c_ids = Indicator.objects.using('hqi').filter(name__in=indicatores).values_list('id', flat=True)

                    #     if len(indicatores) != len(c_ids):
                    #         return {
                    #             'status': 0,
                    #             'message': '操作失败！请检查第 %s 行 "指标"！' % (i + 1, )
                    #         }


                    indicator_id = Indicator.objects.using('hqi').get(name=indicator).id


                    total += 1

                    #唯一性
                    # old_indicator = IndicatorDataParent.objects.using('hqi').filter(year=year)

                    # if old_indicator.exists():
                    #     old_indicator = old_indicator[0]
                    #     old_indicator.value = value
                    #     old_indicator.year = year
                    #     old_indicator.indicator_id = indicator_id
                    #     old_indicator.area_id = area_id
                    #     # if not old_indicator.corpus_id:
                    #     #     old_indicator.corpus_id = monitorWord
                    #     old_indicator.save()
                    #     old_indicator.area.clear()
                    #     old_indicator.indicatores.clear()
                    #     old_indicator.area.add(*area)
                    #     old_indicator.indicatores.add(*indicator)
                    #     old_indicator.save()

                    #     dupli += 1
                    #     continue

                    indicatordata = IndicatorDataParent(
                    	value=value,
                    	year=year,
                    	area=area_id,
                    )
                    indicatordata.save()

                except Exception as e:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }



class IndicatorDataExport(Abstract):

    def __init__(self, user, params={}):
        self.user = user
        super(IndicatorDataExport, self).__init__(params)

    def export(self):
        filename = "indicator.xlsx"

        # process data
        data = [
            ['值', '年份', '地域', '指标'],
        ]
        fields = ('value', 'year', 'areas__name', 'indicator__name')
        cond = {
            # 'areas__id': getattr(self, 'areas', None),
            # 'status': getattr(self, 'status'),
            # 'pubtime__gte': getattr(self, 'starttime', None),
            # 'pubtime__lte': getattr(self, 'endtime', None),
        }
        # print(getattr(self, 'areas', None), getattr(self, 'status'),
        #     getattr(self, 'starttime', None),getattr(self, 'endtime', None))
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = IndicatorDataParent.objects.filter(**args).values(*fields)

        # 判断当前用户是否为武汉深度网科技有限公司成员，然后取出该用户管理的资料
        group_ids = Group.objects.filter(user=self.user).values_list('id', flat=True)
        if 4 in group_ids and 3 in group_ids:
            queryset = queryset.filter(user_id = self.user.id).values(*fields)

        for q in queryset:
            # industry__name = '无' if q['industry__name'] == 'None' else q['industry__name']
            # catogories = categories(q['id'], admin=True, flat=True)
            data.append([q['value'],
                         q['year'],
                         q['areas__name'],
                         q['indicator__name'],
                        ])

        # write file
        write_by_openpyxl(filename, data)

        return open(filename, 'rb')
