from observer.utils.str_format import (str_to_md5str, )
from observer.utils.excel import (read, )
from observer.utils.logger import Logger
from observer.base.models import *


# init logging
logger = Logger(ln='test')
msg = """Scripts: <scripts/test.py>"""


def main():
    # qualification rate
    qr = lambda x , y : float(1) if not x else float(x) / float(y)  

    title = {'标题': 0 ,
            '链接': 0 ,
            '发布日期': 0 ,
            '抽查类别': 0 ,
            '抽查等级': 0 ,
            '抽检单位': 0 ,
            '地域': 0 ,
            '行业编号': 0 ,
            '产品名称': 0 ,
            '不合格企业': 0 ,
            '不合格企业地域': 0 ,
            '不合格项': 0 ,
            '抽查批次': 0 ,
            '合格批次': 0 ,
            '不合格批次': 0 }
    data = read(filename='/mnt/f/inspection.xlsx', title=title)
    for i, d in enumerate(data):
        title = d['标题']
        url = d['链接']
        pubtime = d['发布日期']
        category = d['抽查类别']
        level = d['抽查等级']
        soruce = d['抽检单位']
        area_name = d['地域']
        industry_number = d['行业编号']
        product_name = d['产品名称']
        enterprise_name = d['不合格企业']
        enterprise_area = d['不合格企业地域']
        unitem = d['不合格项']
        inspect_patch = d['抽查批次']
        qualitied_patch = d['合格批次']
        unqualitied_patch = d['不合格批次']

        # 处理行业
        try:
            Industry.objects.get(id=industry_number)
        except Exception as e:
            return {
                    'status': 0, 
                    'message': '操作失败！行业编号不存在，错误信息：%s！' % e
                }

        if not AliasIndustry.objects.filter(name=product_name, industry_id=industry_number).exists():
            AliasIndustry(
                name=product_name,
                industry_id=industry_number,
                ccc_id=0,
                license_id=0,
            ).save()

        industry_id = AliasIndustry.objects.filter(name=product_name, industry_id=industry_number).values('id')[0]

        # 处理抽检地域
        area = Area.objects.filter(name=area_name)
        if not area.exists():
            return {
                        'status': 0, 
                        'message': '操作失败！Excel第%s行，地域（%s）不存在！' % (i, area_name, )
                    }

        guid = str_to_md5str('{0}{1}'.format(url, industry_id))

        # 处理企业
        if enterprise_name:
            enterprises = enterprise.split(' ')
            areas = enterprise_area.split(' ')
            for ei, e in enumerate(enterprises):
                areaname = areas[ei]
                enterprise_area = Area.objects.filter(name=areaname)
                if not enterprise_area.exists():
                    return {
                        'status': 0, 
                        'message': '操作失败！Excel第%s行，企业地域（%s）不存在！' % (i, areaname, )
                    }
                enterprise_area_id =enterprise_area.values('id')[0]
                enterprise = Enterprise.objects.filter(name=e, area_id=enterprise_area_id)
                if not enterprise.exists():
                    Enterprise(
                        name=e, 
                        area_id=enterprise_area_id,
                    ).save()

                # 处理抽检企业关联
                enterprise_id = Enterprise.objects.filter(name=e, area_id=enterprise_area_id).values('id')[0]
                inspection_enterprise = InspectionEnterprise.objects.filter(inspection_id=guid, enterprise_id=enterprise_id)            
                if not inspection_enterprise.exists():
                    InspectionEnterprise(
                        inspection_id=guid,
                        enterprise_id=enterprise_id,
                    ).save()
 
        # 处理抽检信息
        inspection = Inspection.objects.filter(guid=guid)
        if not inspection.exists():
            Inspection(
                guid=guid,
                title=title,
                url=url,
                pubtime=pubtime,
                source=source,
                unitem=unitem,
                qualitied=qr(inspect_patch, qualitied_patch),
                category=category,
                level=level,
                industry_id=industry_id,
                area_id=area.values('id')[0],
                status=1,
            ).save()
        else:
            pass


def run():
    main()