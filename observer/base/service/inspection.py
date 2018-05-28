import openpyxl
from io import BytesIO

from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import(Area, Inspection, Industry, 
                                Enterprise, InspectionEnterprise, 
                                AliasIndustry)
from observer.base.service.abstract import Abstract
from observer.base.service.base import (area, alias_industry, qualitied, 
                                        industry_number, enterprise_name, enterprise_area_name, 
                                        enterprise_unitem, )
from observer.utils.date_format import (date_format, str_to_date, get_months)
from observer.utils.str_format import str_to_md5str
from observer.utils.excel import (read_by_openpyxl, write_by_openpyxl, )



class InspectionData(Abstract):

    def __init__(self, params):
        super(InspectionData, self).__init__(params)

    def get_all(self):

        fields = ('guid', 'title', 'url', 'pubtime', 'source', 'qualitied', 'category', 'level', 'industry_id', 'area_id', )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'qualitied__gte': getattr(self, 'qualitied_gte', None),
            'qualitied__lt': getattr(self, 'qualitied_lt', None),
            'category__contains': getattr(self, 'category', None),
            'source__contains': getattr(self, 'source', None),
            'level': getattr(self, 'level', None),
            'industry_id': getattr(self, 'industry', None),
            'area_id': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Inspection.objects.exclude(status=-1).filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class InspectionDataAdd(Abstract):

    def __init__(self, user, params={}):
        super(InspectionDataAdd, self).__init__(params)
        self.user = user

    def add(self):
        # qualification rate
        qr = lambda x , y : float(1) if not x else float(x) / float(y)  

        title = getattr(self, 'title', '')
        url = getattr(self, 'url', '')
        pubtime = getattr(self, 'pubtime', '')
        source = getattr(self, 'source', '')

        inspect_patch = getattr(self, 'inspect_patch', 0)
        qualitied_patch = getattr(self, 'qualitied_patch', 0)
        unqualitied_patch = getattr(self, 'unqualitied_patch', 0)

        category = getattr(self, 'category', '')
        level = getattr(self, 'level', '')
        industry_id = getattr(self, 'industry_id', '')
        area_id = getattr(self, 'area_id', '')

        if not url or not pubtime or not source or not inspect_patch or not qualitied_patch or not category or not level or not industry_id or not area_id:
            return 400

        guid = str_to_md5str('{0}{1}'.format(url, industry_id))

        if Inspection.objects.filter(guid=guid).exists():
            return 202

        Inspection(
            guid=guid,
            title=title,
            url=url,
            pubtime=pubtime,
            source=source,
            qualitied=qr(qualitied_patch, inspect_patch),
            category=category,
            level=level,
            industry_id=industry_id,
            area_id=area_id,
            status=1,
        ).save()

        return 200


class InspectionDataEdit(Abstract): 

    def __init__(self, user, params={}):
        super(InspectionDataEdit, self).__init__(params)
        self.user = user

    def edit(self, aid):
        # qualification rate
        qr = lambda x , y : float(1) if not x else float(x) / float(y)  

        edit_id = aid
        title = getattr(self, 'title', '')
        url = getattr(self, 'url', '')
        pubtime = getattr(self, 'pubtime', '')
        source = getattr(self, 'source', '')
        
        inspect_patch = getattr(self, 'inspect_patch', 0)
        qualitied_patch = getattr(self, 'qualitied_patch', 0)
        unqualitied_patch = getattr(self, 'unqualitied_patch', 0)

        category = getattr(self, 'category', '')
        level = getattr(self, 'level', '')
        industry_id = getattr(self, 'industry_id', '')
        area_id = getattr(self, 'area_id', '')

        if not url or not pubtime or not source or not inspect_patch or not qualitied_patch or not category or not level or not industry_id or not area_id:
            return 400

        guid = str_to_md5str('{0}{1}'.format(url, industry_id))

        inspection = Inspection.objects.get(guid=edit_id)
        inspection.title = title
        inspection.url = url
        inspection.pubtime = pubtime
        inspection.source = source
        inspection.qualitied = qr(inspect_patch, qualitied_patch)
        inspection.category = category
        inspection.level = level
        inspection.industry_id = industry_id
        inspection.area_id = area_id
        inspection.save()

        if guid != edit_id:
            Inspection.objects.filter(guid=guid).delete()

        return 200


class InspectionDataDelete(Abstract): 

    def __init__(self, user):
        self.user = user

    def delete(self, aid):
        del_id = aid
        Inspection.objects.filter(guid=del_id).update(status=-1)
        
        return 200


class InspectionDataUpload(Abstract): 

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        # ModelWeight
        model = {'标题': 0, '链接': 0, '发布日期': 0, '抽查类别': 0, '抽查等级': 0, '抽检单位': 0, '地域': 0, '行业编号': 0, '产品名称': 0, '抽查批次': 0, '合格批次': 0, '不合格批次': 0 }
        # qualification rate
        qr = lambda x , y : float(1) if not x else float(x) / float(y)  
        # sheet values
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
                    title = sv(i, model['标题'], sheet)
                    url = sv(i, model['链接'], sheet)
    
                    if not url:
                        continue

                    pubtime = date_format(sv(i, model['发布日期'], sheet))
                    if not pubtime:
                        return {
                            'status': 0, 
                            'message': '操作失败！Excel %s 行时间格式有误！' % (i + 1, )
                        }
                        
                    category = sv(i, model['抽查类别'], sheet)
                    level = sv(i, model['抽查等级'], sheet)
                    source = sv(i, model['抽检单位'], sheet)
                    area_name = sv(i, model['地域'], sheet)
                    industry_number = sv(i, model['行业编号'], sheet)
                    product_name = sv(i, model['产品名称'], sheet)
                    inspect_patch = sv(i, model['抽查批次'], sheet)
                    qualitied_patch = sv(i, model['合格批次'], sheet)
                    unqualitied_patch = sv(i, model['不合格批次'], sheet)

                    total += 1

                    # 处理行业
                    try:
                        Industry.objects.get(id=industry_number)
                    except Exception as e:
                        return {
                                'status': 0, 
                                'message': '操作失败！Excel第%s行,行业编号不存在。详细错误信息：%s！' % (i, e, )
                            }

                    if not AliasIndustry.objects.filter(name=product_name, industry_id=industry_number).exists():
                        AliasIndustry(
                            name=product_name,
                            industry_id=industry_number,
                            ccc_id=0,
                            license_id=0,
                        ).save()

                    industry_id = AliasIndustry.objects.get(name=product_name, industry_id=industry_number).id

                    # 处理抽检地域
                    area = Area.objects.filter(name=area_name)
                    if not area.exists():
                        return {
                                    'status': 0, 
                                    'message': '操作失败！Excel第%s行，地域（%s）不存在！' % (i, area_name, )
                                }

                    guid = str_to_md5str('{0}{1}'.format(url, industry_id))

                    # 处理抽检信息
                    inspection = Inspection.objects.filter(guid=guid)
                    if not inspection.exists():
                        Inspection(
                            guid=guid,
                            title=title,
                            url=url,
                            pubtime=pubtime,
                            source=source,
                            qualitied=qr(qualitied_patch, inspect_patch),
                            category=category,
                            level=level,
                            industry_id=industry_id,
                            area_id=area[0].id,
                            status=1,
                        ).save()
                    else:
                        dupli += 1

                except Exception as e:
                    return {
                        'status': 0, 
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }

        return {
                    'status': 1, 
                    'message': '操作成功！共处理%s条数据，成功导入%s条数据，重复数据%s条！' % (total, total - dupli, dupli, )
                }
        

class InspectionDataUnEnterpriseUpload(Abstract): 

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        # ModelWeight
        model = {'链接': 0, '行业编号': 0, '产品名称': 0, '不合格企业': 0, '不合格企业地域': 0, '不合格项': 0 }
        # sheet values
        sv = lambda x, y, z : z.cell(row=x, column=y).value

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
                    url = sv(i, model['链接'], sheet)
    
                    if not url:
                        continue

                    industry_number = sv(i, model['行业编号'], sheet)
                    product_name = sv(i, model['产品名称'], sheet)
                    unenterprise = sv(i, model['不合格企业'], sheet)
                    unenterprise_area = sv(i, model['不合格企业地域'], sheet)
                    unitem = sv(i, model['不合格项'], sheet)

                    total += 1

                    # 处理行业
                    try:
                        Industry.objects.get(id=industry_number)
                    except Exception as e:
                        return {
                                'status': 0, 
                                'message': '操作失败！Excel第%s行,行业编号不存在。详细错误信息：%s！' % (i, e, )
                            }

                    if not AliasIndustry.objects.filter(name=product_name, industry_id=industry_number).exists():
                        AliasIndustry(
                            name=product_name,
                            industry_id=industry_number,
                            ccc_id=0,
                            license_id=0,
                        ).save()

                    industry_id = AliasIndustry.objects.get(name=product_name, industry_id=industry_number).id

                    # 处理抽检地域
                    area = Area.objects.filter(name=unenterprise_area)
                    if not area.exists():
                        return {
                                    'status': 0, 
                                    'message': '操作失败！Excel第%s行，地域（%s）不存在！' % (i, unenterprise_area, )
                                }

                    area_id =area[0].id

                    guid = str_to_md5str('{0}{1}'.format(url, industry_id))

                    # 处理不合格企业信息
                    enterprise = Enterprise.objects.filter(name=unenterprise, area_id=area_id)
                    if not enterprise.exists():
                        Enterprise(
                            name=unenterprise,
                            unitem=unitem,
                            area_id=area_id,
                        ).save()

                    enterprise_id = Enterprise.objects.filter(name=unenterprise, area_id=area_id)[0].id
                    inspection_enterprise = InspectionEnterprise.objects.filter(inspection_id=guid, enterprise_id=enterprise_id)
                    if not inspection_enterprise.exists():
                        InspectionEnterprise(
                            inspection_id=guid,
                            enterprise_id=enterprise_id,
                        ).save()
                    else:
                        dupli += 1

                except Exception as e:
                    return {
                        'status': 0, 
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }

        return {
                    'status': 1, 
                    'message': '操作成功！共处理%s条数据，成功导入%s条数据，重复数据%s条！' % (total, total - dupli, dupli, )
                }
        

class InspectionDataExport(Abstract): 

    def __init__(self, user):
        self.user = user

    def export(self):
        filename = "inspections.xlsx"

        # process data
        data = [
            ['GUID', '标题', '链接', '发布日期', '抽查类别', '抽查等级', '抽检单位', '地域', '行业编号', '产品名称', '不合格企业', '不合格企业地域', '不合格项', '合格率', ],
        ]
        months = get_months()[-1::][0]
        start = months[0].strftime('%Y-%m-%d')
        end = months[1].strftime('%Y-%m-%d')

        queryset = Inspection.objects.filter(pubtime__gte=start, pubtime__lt=end).values('guid', 'title', 'url', 'pubtime', 'category', 'level', 'source', 'area_id', 'industry_id', 'qualitied',)

        for q in queryset:
            data.append([
                q['guid'],
                q['title'],
                q['url'],
                date_format(q['pubtime'], '%Y-%m-%d'),
                q['category'],
                q['level'],
                q['source'],
                area(q['area_id'], flat=True),
                industry_number(q['industry_id']),
                alias_industry(q['industry_id'], flat=True),
                enterprise_name(q['guid'], flat=True),
                enterprise_area_name(q['guid'], flat=True),
                enterprise_unitem(q['guid'], flat=True),
                qualitied(q['qualitied']),
                ])

        # write file
        write_by_openpyxl(filename, data)

        return open(filename, 'rb')
