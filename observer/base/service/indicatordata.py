from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from observer.apps.hqi.models import Indicator,IndicatorDataParent, Area
from observer.base.service.abstract import Abstract
from observer.base.models import Area
from observer.base.service.base import (areas, indicatores )



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

        return queryset.values(*fields).order_by('indicator_id')

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
                    value = str(sv(i, model['值'], sheet)).strip()
                    if value == 'None':
                        continue

                    #年份
                    year = str(sv(i, model['年份'], sheet)).strip()
                    if year == 'None':
                        continue

                    # pubtime = str(date_format(sv(i, model['发布时间'], sheet))).strip()
                    # if pubtime == 'None':
                    #     pubtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                    # 地域
                    area = str(sv(i, model['地域'], sheet)).strip()
                    if area == 'None':
                        continue
                    else:
                        areas = area.split()
                        a_ids = Area.objects.filter(name__in=areas).values_list('id', flat=True)

                        if len(areas) != len(a_ids):
                            return {
                                'status': 0,
                                'message': '操作失败！请检查第 %s 行 "地域"！' % (i + 1, )
                            }

                        area = Area.objects.filter(id__in=a_ids)

                    # 指标类别
                    indicator = str(sv(i, model['指标'], sheet)).strip()
                    if indicator == 'None':
                        continue
                    else:
                        indicatores = indicator.split()
                        c_ids = Indicator.objects.filter(name__in=indicatores).values_list('id', flat=True)

                        if len(indicatores) != len(c_ids):
                            return {
                                'status': 0,
                                'message': '操作失败！请检查第 %s 行 "指标"！' % (i + 1, )
                            }

                        indicator = Indicator.objects.filter(id__in=c_ids)


                    total += 1

                    唯一性
                    old_article = Article.objects.filter(url=url)

                    if old_article.exists():
                        old_article = old_article[0]
                        old_article.title = title
                        old_article.url = url
                        old_article.pubtime = pubtime
                        old_article.source = source
                        old_article.score = score
                        old_article.industry_id = industry_id
                        if not old_article.corpus_id:
                            old_article.corpus_id = monitorWord
                        old_article.save()
                        old_article.areas.clear()
                        old_article.indicatores.clear()
                        old_article.areas.add(*area)
                        old_article.indicatores.add(*category)
                        old_article.save()

                        dupli += 1
                        continue

                    indicatordata = IndicatorDataParent(
                    	value=value,
                    	year=year,
                    	area=area,
                    	Indicator=indicator,

                    )
                    indicatordata.save()
                    indicatordata.areas.add(*area)
                    indicatordata.indicatores.add(*category)
                    indicatordata.save()

                except Exception as e:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }

        return {
                    'status': 1,
                    'message': '操作成功！共处理%s条数据，新增数据%s条，更新数据%s条！' % (total, total - dupli, dupli, )
                }
