import requests

from fuzzywuzzy import fuzz, process

import jieba
import jieba.posseg as pseg
from lxml import etree

from observer.utils.str_format import str_to_md5str
from observer.base.models import Inspection, Area, Unitem, Enterprise


def crawler(edit_ids, urls, product_names):
    jieba.load_userdict('observer/utils/dictionary.txt')

    headers = {
        'User-Agent':'PostmanRuntime/7.22.0',
        'Accept':'*/*',
        'Cache-Control':'no-cache',
        'Postman-Token':'7c84853e-2a6e-40f3-8884-14b5192ed941',
        'Host':'www.cqn.com.cn',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'keep-alive',
    }

    for (id, url, product_name) in zip(edit_ids.split(","), urls.split(","), product_names.split(",")):

        if url.find('www.cqn.com.cn') == -1:
            pass
        else:
            print(id, '-', product_name, '已开始爬取')

            # 爬取不合格企业
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            html = etree.HTML(response.text)

            table_xpath_list = ['//div[@class="content"]/table', '//table']

            table = ''
            table_xpath = ''
            for i in table_xpath_list:
                table = html.xpath(i)
                table_xpath = i
                if len(table) != 0:
                    break

            for t in range(len(table)):
                print('正在爬取第%d张表' %(t+1))
                t_title_xpath = ''

                temp_xpath = '%s[%d]/thead' %(table_xpath, t+1)
                # thead
                if len(html.xpath(temp_xpath)) != 0:
                    t_head_head_xpath = '%s[%d]/thead/tr' %(table_xpath, t+1)
                    t_head_head = html.xpath(t_head_head_xpath)
                    for i in range(len(t_head_head)):
                        t_title_xpath = '%s[%d]/thead/tr[%d]/td' %(table_xpath, t+1, i+1)
                        if len(html.xpath(t_title_xpath)) > 1:
                            break

                # tbody
                else:
                    t_body_head_xpath = '%s[%d]/tbody/tr' %(table_xpath, t+1)
                    t_body_head = html.xpath(t_body_head_xpath)
                    for i in range(len(t_body_head)):
                        t_title_xpath = '%s[%d]/tbody/tr[%d]/td' %(table_xpath, t+1, i+1)
                        if len(html.xpath(t_title_xpath)) > 1:
                            break

                if t_title_xpath == '':
                    print('无')
                    pass
                else:
                    print('表头', t_title_xpath)
                    t_title = html.xpath(t_title_xpath)
                    thead = []
                    for i in t_title:
                        thead.append(i.xpath('string(.)').strip())

                    e_col, u_col = [], []
                    enterprise_fields = [
                                    '被抽查单位名称',
                                    '被抽样单位名称',
                                    '标称生产者',
                                    '标称生产单位',
                                    '标称生产企业名称',
                                    '企业名称',
                                    '生产单位',
                                    '标示生产单位',
                                    '生产企业(标称)',
                                    '生产企业（标称）',
                                    '（标称）生产单位名称',
                                    '标称生产企业',
                                    '标称生产厂家',
                                    '单位名称',
                                    '被抽检单位名称',
                                    '受检企业',
                                    '受检企业名称',
                                    '受检单位',
                                    '受检单位名称',
                                    '生产企业',
                                    '生产企业名称',
                                    '标称生产企业或供货单位名称',
                                    '标识生产企业名称',
                                    ]

                    unitem_fields = [
                                    '主要不合格项',
                                    '主要不合格项目',
                                    '不合格项目',
                                    '不合格项目║检验结果║标准值',
                                    '主要不合格项目或主要问题',
                                    '主要不合格项（项目名称：标准值/实测值）',
                                    '不合格项目实测值', '不符合项目',
                                    '合格状态',
                                    '不合格项目（标准值/实测值）',
                                    '不合格项',
                                    '不合格项及未抽样原因',
                                    ]

                    for i, enterprise in enumerate(thead):
                        results = process.extract(enterprise, enterprise_fields, limit=len(enterprise_fields))
                        for a in results:
                            if a[1] >= 99:
                                e_col.append(i+1)
                                break
                    if e_col == []:
                        e_col.append('100')

                    for i, unitem in enumerate(thead):
                        results = process.extract(unitem, unitem_fields, limit=len(unitem_fields))
                        for a in results:
                            if a[1] >= 99:
                                u_col.append(i+1)
                                break
                    if u_col == []:
                        u_col.append('100')

                    enterprise_xpath = '%s[%d]/tbody/tr/td[%s]' %(table_xpath, t+1, e_col[0])
                    unitem_xpath = '%s[%d]/tbody/tr/td[%s]' %(table_xpath, t+1, u_col[0])

                    enterprises = html.xpath(enterprise_xpath)
                    unitems = html.xpath(unitem_xpath)

                    print('企业名:', e_col, '不合格项:', u_col)

                    invalid_words = [
                                    '', '/', '无','-', '—', '---', '——', '----', '符合本次监督检查要求',
                                    ]

                    # 合格企业
                    if unitems == []:
                        unitems = ['-'] * len(enterprises)

                    for i, j in zip(enterprises, unitems):
                        m = 0
                        n = 0
                        enterprise_name = i.xpath('string(.)').strip()

                        if j == '-':
                            unitem_name = j
                        else:
                            unitem_name = j.xpath('string(.)').strip()

                        if enterprise_name.find('市') != -1:
                            processed = enterprise_name.replace('市', '')
                        elif enterprise_name.find('省') != -1:
                            processed = enterprise_name.replace('省', '')
                        elif enterprise_name.find('县') != -1:
                            processed = enterprise_name.replace('县', '')
                        else:
                            processed = enterprise_name

                        areas = pseg.cut(processed)
                        for area, flag in areas:
                            if flag == 'findarea':
                                m += 1
                                if m >= 2:
                                    continue

                                is_area = Area.objects.filter(
                                    name=area).values_list('id', flat=True)
                                if is_area.exists():
                                    area_id = is_area[0]
                                else:
                                    area_id = '1'

                                # 判断企业是否合格
                                if unitem_name not in invalid_words:
                                    is_qualitied = 0
                                else:
                                    is_qualitied = 1

                                # 去企业库查询企业是否存在
                                queryset = Enterprise.objects.filter(JGMC=enterprise_name)
                                if queryset.exists():
                                    enterprise_ids = Enterprise.objects.filter(
                                        JGMC=enterprise_name).values_list('id', flat=True)
                                    Enterprise.objects.filter(
                                        id=enterprise_ids[0]).update(area_id=area_id)
                                    Unitem(
                                        name='-' if is_qualitied == 1 else unitem_name,
                                        status=0,
                                        enterprise_id=enterprise_ids[0],
                                        inspection_id=id,
                                        is_qualitied=is_qualitied,
                                    ).save()
                                else:
                                    Enterprise(
                                        JGMC=enterprise_name,
                                        area_id=area_id,
                                    ).save()

                                    enterprise_id = Enterprise.objects.filter(
                                        JGMC=enterprise_name).values_list('id', flat=True)
                                    Unitem(
                                        name='-' if is_qualitied == 1 else unitem_name,
                                        status=0,
                                        enterprise_id=enterprise_id[0],
                                        inspection_id=id,
                                        is_qualitied=is_qualitied,
                                    ).save()

                        if m == 0:
                            area = '全国'
                            n += 1
                            if n >= 2:
                                continue

                            is_area = Area.objects.filter(
                                name=area).values_list('id', flat=True)

                            area_id = is_area[0]

                            # 判断企业是否合格
                            if unitem_name not in invalid_words:
                                is_qualitied = 0
                            else:
                                is_qualitied = 1

                            # 去企业库查询企业是否存在
                            queryset = Enterprise.objects.filter(JGMC=enterprise_name)
                            if queryset.exists():
                                Enterprise.objects.filter(
                                    id=queryset[0].id).update(area_id=area_id)
                                Unitem(
                                    name='-' if is_qualitied == 1 else unitem_name,
                                    status=0,
                                    enterprise_id=queryset[0].id,
                                    inspection_id=id,
                                    is_qualitied=is_qualitied,
                                ).save()
                            else:
                                Enterprise(
                                    JGMC=enterprise_name,
                                    area_id=area_id,
                                ).save()

                                enterprise_id = Enterprise.objects.filter(
                                    JGMC=enterprise_name).values_list('id',flat=True)
                                Unitem(
                                    name='-' if is_qualitied == 1 else unitem_name,
                                    status=0,
                                    enterprise_id=enterprise_id[0],
                                    inspection_id=id,
                                    is_qualitied=is_qualitied,
                                ).save()

                        m = 0
                        n = 0

        Inspection.objects.filter(id=id).update(status=2) # status:0 未爬取; 2 已爬取; 1 已审核

        print(id, '-', product_name, '已爬取完毕', '\n')
