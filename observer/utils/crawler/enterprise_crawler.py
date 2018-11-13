import requests

from fuzzywuzzy import fuzz, process

import jieba
import jieba.posseg as pseg
from lxml import etree

from observer.utils.str_format import str_to_md5str
from observer.base.models import (Inspection, Area, Enterprise, InspectionEnterprise)

jieba.load_userdict('observer/utils/dictionary.txt')


def crawler(edit_ids, urls, product_names):
    for (ids, url, product_name) in zip(edit_ids.split(","), urls.split(","), product_names.split(",")):
        guid = str_to_md5str('{0}{1}'.format(url, product_name))

        print('正在爬取...：', product_name)

        Inspection.objects.filter(id=ids).update(status=2)

        # 爬取不合格企业
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)

        table_xpath = '//table'
        table = html.xpath(table_xpath)
        table.pop()
        table.pop()

        if len(table) == 0:
            pass
        else:
            for t in range(len(table)):
                title_xpath = '//table[%d]/thead/tr[1]/td' %(t+1)
                title = html.xpath(title_xpath)

                if len(title) == 0:
                    title_xpath = '//table[%d]/tbody/tr[1]/td' %(t+1)
                    title = html.xpath(title_xpath)

                    if len(title) == 1:
                        title_xpath = '//table[%d]/tbody/tr[2]/td' %(t+1)
                        title = html.xpath(title_xpath)

                elif len(title) == 1:
                    title_xpath = '//table[%d]/thead/tr[2]/td' %(t+1)
                    title = html.xpath(title_xpath)

                thead = []
                for i in title:
                    thead.append(i.xpath('string(.)').strip())

                e_col, u_col = [], []
                enterprise_fields = ['生产企业名称', '标称生产者', '标称生产单位', '标称生产企业名称', '标称生产企业名称',
                '企业名称', '生产单位', '标示生产单位', '生产企业(标称)', '（标称）生产单位名称', '标称生产企业', '标称生产厂家',
                '受检单位名称','被抽查单位','样品标称名称']

                unitem_fields = ['主要不合格项目', '不合格项目', '不合格项目║检验结果║标准值', '主要不合格项目或主要问题',
                 '主要不合格项（项目名称：标准值/实测值）', '不合格项目实测值', '不符合项目','不符合标准规定项']

                for i, unenterprise in enumerate(thead):
                    results = process.extract(unenterprise, enterprise_fields, limit=15)
                    for a in results:
                        if a[1] >= 99:
                            e_col.append(i+1)
                            break
                if e_col == []:
                    e_col.append('100')

                for i, unitem in enumerate(thead):
                    results = process.extract(unitem, unitem_fields, limit=8)
                    for a in results:
                        if a[1] >= 99:
                            u_col.append(i+1)
                            break
                if u_col == []:
                    u_col.append('100')

                unenterprise_xpath = '//table[%d]/tbody/tr/td[%s]' %(t+1, e_col[0])
                unitem_xpath = '//table[%d]/tbody/tr/td[%s]' %(t+1, u_col[0])

                unenterprise = html.xpath(unenterprise_xpath)
                unitem = html.xpath(unitem_xpath)

                data = []
                invalid_words = ['', '/', '无', '—', '---', '主要不合格项目', '不合格项目',
                '不合格项目║检验结果║标准值', '主要不合格项目或主要问题', '主要不合格项（项目名称：标准值/实测值）',
                '不合格项目实测值', '不符合项目', '不符合标准规定项', '未发现不合格项目']
                new_words = ''

                for i, j in zip(unenterprise, unitem):
                    m = 0
                    n = 0
                    if i.xpath('string(.)').strip().find('市') != -1:
                        new_words = i.xpath('string(.)').strip().replace('市', '')
                    elif i.xpath('string(.)').strip().find('省') != -1:
                        new_words = i.xpath('string(.)').strip().replace('省', '')
                    elif i.xpath('string(.)').strip().find('县') != -1:
                        new_words = i.xpath('string(.)').strip().replace('县', '')
                    else:
                        new_words = i.xpath('string(.)').strip()

                    areas = pseg.cut(new_words)
                    for area, flag in areas:
                        if flag == 'findarea' and j.xpath('string(.)').strip() not in invalid_words:
                            m += 1
                            if m >= 2:
                                continue
                            data.append((guid, i.xpath('string(.)').strip(), j.xpath('string(.)').strip(), area))

                            area_id = Area.objects.filter(name=area)[0].id

                            # 爬取的企业信息插入到不合格企业审核表 >status: 0
                            Enterprise(
                                name=new_words,
                                unitem=j.xpath('string(.)').strip(),
                                area_id=area_id,
                                status=0,
                            ).save()

                            enterprise_id = Enterprise.objects.filter(
                            name=new_words, area_id=area_id)[0].id
                            inspection_enterprise = InspectionEnterprise.objects.filter(
                                inspection_id=guid, enterprise_id=enterprise_id)
                            if not inspection_enterprise.exists():
                                InspectionEnterprise(
                                    inspection_id=guid,
                                    enterprise_id=enterprise_id,
                                ).save()

                    if m == 0 and j.xpath('string(.)').strip() not in invalid_words:
                        area = '全国'
                        n += 1
                        if n >= 2:
                            continue
                        data.append((guid, i.xpath('string(.)').strip(), j.xpath('string(.)').strip(), area))

                        area_id = Area.objects.filter(name=area)[0].id

                        Enterprise(
                            name=new_words,
                            unitem=j.xpath('string(.)').strip(),
                            area_id=area_id,
                            status=0,
                        ).save()

                        enterprise_id = Enterprise.objects.filter(
                        name=new_words, area_id=area_id)[0].id
                        inspection_enterprise = InspectionEnterprise.objects.filter(
                            inspection_id=guid, enterprise_id=enterprise_id)
                        if not inspection_enterprise.exists():
                            InspectionEnterprise(
                                inspection_id=guid,
                                enterprise_id=enterprise_id,
                            ).save()

                    m = 0
                    n = 0
