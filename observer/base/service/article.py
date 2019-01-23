import openpyxl
from io import BytesIO
import threading

import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, Article, Category, )
from django.contrib.auth.models import Group, User
from observer.base.service.abstract import Abstract
from observer.base.service.base import (areas, categories, )
from observer.utils.date_format import (date_format, str_to_date, get_months)
from observer.utils.str_format import str_to_md5str
from observer.utils.excel import (read_by_openpyxl, write_by_openpyxl, )
from observer.utils.crawler.news_crawler import newsCrawler


class ArticleData(Abstract):

    def __init__(self, params, category):
        self.category = category
        super(ArticleData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'url', 'title', 'source', 'pubtime', 'score')

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lte': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'score': getattr(self, 'score', None),
            'areas': getattr(self, 'areas', None),
            'categories': getattr(self, 'categories', None),
            'status': 1,
        }

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Article.objects.filter(**args)

        c_ids = Category.objects.filter(parent__id=self.category).values_list('id', flat=True)
        if not c_ids:
            queryset = queryset.filter(categories=self.category)
        else:
            queryset = queryset.filter(categories__in=c_ids)

        return queryset.values(*fields).order_by('-pubtime')


class RiskData(Abstract):

    def __init__(self, user, params):
        super(RiskData, self).__init__(params)
        self.user = user

    def get_all(self):
        fields = ('id', 'url', 'title', 'source', 'pubtime', 'score', 'status' )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lte': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'score': getattr(self, 'score', None),
            'status': getattr(self, 'status', None),
            'industry_id': getattr(self, 'industry', None),
            'areas': getattr(self, 'areas', None),
            'categories': getattr(self, 'category', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Article.objects.filter(**args)

        # 判断当前用户是否为武汉深度网科技有限公司成员，然后取出该用户管理的资料
        group_ids = Group.objects.filter(user=self.user).values_list('id', flat=True)
        if 4 in group_ids and 3 in group_ids:
            queryset = queryset.filter(user_id = self.user.id).values(*fields)

        return queryset.values(*fields).order_by('-pubtime')


class RiskDataAdd(Abstract):

    def __init__(self, user, params={}):
        super(RiskDataAdd, self).__init__(params)
        self.user = user

    def add(self):
        url = getattr(self, 'url', '')
        title = getattr(self, 'title', '')
        pubtime = getattr(self, 'pubtime', '')
        score = getattr(self, 'score', 0)
        source = getattr(self, 'source', '')
        areas = getattr(self, 'areas', '')
        categories = getattr(self, 'categories', '')
        industries = getattr(self, 'industries', '')

        if not url or not title or not pubtime or not source or not areas or not categories:
            return 400

        if Article.objects.filter(url=url).exists():
            return 202

        # 有多个地域时逗号分隔，并且忽略掉最后一个逗号
        a_ids = areas.split(',')[:-1:]
        area = Area.objects.filter(id__in=a_ids)

        c_ids = categories.split(',')[:-1:]
        category = Category.objects.filter(id__in=c_ids)

        article = Article(
            title=title,
            url=url,
            pubtime=pubtime,
            source=source,
            score=score,
            industry_id=industries,
            user_id=self.user.id,
            status=1,
        )
        article.save()

        article.areas.add(*area)
        article.categories.add(*category)

        article.save()

        return 200


class RiskDataAudit(Abstract):
    def __init__(self, params={}):
        super(RiskDataAudit, self).__init__(params)

    def edit(self, aid):
        audit_ids = aid.split(',')

        Article.objects.filter(id__in=audit_ids).update(status=1)

        return 200


class RiskDataEdit(Abstract):

    def __init__(self, params={}):
        super(RiskDataEdit, self).__init__(params)

    def edit(self, aid):
        edit_id = aid
        title = getattr(self, 'title', '')
        pubtime = getattr(self, 'pubtime', '')
        score = getattr(self, 'score', 0)
        source = getattr(self, 'source', '')
        areas = getattr(self, 'areas', '')
        categories = getattr(self, 'categories', '')

        if not pubtime or not source or not areas or not categories:
            return 400

        article = Article.objects.get(id=edit_id)
        article.title = title
        article.pubtime = pubtime
        article.score = score
        article.source = source
        article.save()

        a_ids = areas.split(',')[:-1:] # 有多个地域时逗号分隔，并且忽略掉最后一个逗号
        c_ids = categories.split(',')[:-1:]

        area = Area.objects.filter(id__in=a_ids)
        category = Category.objects.filter(id__in=c_ids)

        article.areas.clear()
        article.categories.clear()
        article.areas.add(*area)
        article.categories.add(*category)

        article.save()

        return 200


class RiskDataDelete(Abstract):

    def __init__(self, user):
        self.user = user

    def delete(self, aid):
        del_ids = aid.split(',')

        Article.objects.filter(id__in=del_ids).delete()

        return 200


class RiskDataUpload(Abstract):

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        #Model weight
        model = {'标题': 0, 'URL': 0, '发布时间': 0, '来源': 0, '风险程度': 0, '地域': 0, '类别': 0, '行业编号': 0}
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
                    title = str(sv(i, model['标题'], sheet)).strip()
                    if title == 'None':
                        continue

                    url = str(sv(i, model['URL'], sheet)).strip()
                    if url == 'None':
                        continue

                    pubtime = str(date_format(sv(i, model['发布时间'], sheet))).strip()
                    if pubtime == 'None':
                        continue

                    source = str(sv(i, model['来源'], sheet)).strip()
                    if source == 'None':
                        continue

                    score = str(sv(i, model['风险程度'], sheet)).strip()
                    if score == 'None':
                        continue

                    # 行业编号
                    industry_id = sv(i, model['行业编号'], sheet)
                    if not industry_id or industry_id == '0':
                        industry_id = '-1'

                    # 地域
                    area = str(sv(i, model['地域'], sheet)).strip()
                    if area == 'None':
                        continue
                    else:
                        print('area', area)
                        areas = area.split(',')
                        a_ids = Area.objects.filter(name__in=areas).values_list('id', flat=True)

                        if len(areas) != len(a_ids):
                            return {
                                'status': 0,
                                'message': '操作失败！请检查第 %s 行 "地域"！' % (i + 1, )
                            }

                        area = Area.objects.filter(id__in=a_ids)

                    # 风险类别
                    category = str(sv(i, model['类别'], sheet)).strip()
                    if category == 'None':
                        continue
                    else:
                        categories = category.split(',')
                        c_ids = Category.objects.filter(name__in=categories).values_list('id', flat=True)

                        if len(categories) != len(c_ids):
                            return {
                                'status': 0,
                                'message': '操作失败！请检查第 %s 行 "类别"！' % (i + 1, )
                            }

                        category = Category.objects.filter(id__in=c_ids)

                    total += 1

                    # 唯一性
                    old_article = Article.objects.filter(url=url)

                    if old_article.exists():
                        old_article = old_article[0]
                        old_article.title = title
                        old_article.url = url
                        old_article.pubtime = pubtime
                        old_article.source = source
                        old_article.score = score
                        old_article.industry_id = industry_id
                        old_article.save()
                        old_article.areas.clear()
                        old_article.categories.clear()
                        old_article.areas.add(*area)
                        old_article.categories.add(*category)
                        old_article.save()

                        dupli += 1
                        continue

                    article = Article(
                        title=title,
                        url=url,
                        pubtime=pubtime,
                        source=source,
                        score=score,
                        industry_id=industry_id,
                        user_id=self.user.id,
                        status=1,
                    )
                    article.save()
                    article.areas.add(*area)
                    article.categories.add(*category)
                    article.save()

                except Exception as e:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }

        return {
                    'status': 1,
                    'message': '操作成功！共处理%s条数据，新增数据%s条，更新数据%s条！' % (total, total - dupli, dupli, )
                }


class RiskDataExport(Abstract):

    def __init__(self, user):
        self.user = user

    # def export(self):
    #     filename = "articles.xlsx"

    #     # process data
    #     data = [
    #         ['GUID', '标题', 'URL', '发布时间', '来源', '发布者', '风险程度', '地域', '类别', ],
    #     ]
    #     months = get_months()[-1::][0]
    #     start = months[0].strftime('%Y-%m-%d')
    #     end = months[1].strftime('%Y-%m-%d')

    #     queryset = Article.objects.filter(pubtime__gte=start, pubtime__lte=end).values('guid', 'title', 'url', 'pubtime', 'source', 'score')

    #     for q in queryset:
    #         data.append([q['guid'],
    #                      q['title'],
    #                      q['url'],
    #                      date_format(q['pubtime'], '%Y-%m-%d'),
    #                      q['source'],
    #                      q['score'],
    #                      areas(q['guid'], flat=True),
    #                      categories(q['guid'], flat=True)])

    #     # write file
    #     write_by_openpyxl(filename, data)

    #     return open(filename, 'rb')


class RiskDataSuzhou(Abstract):

    def __init__(self, params={}):
        super(RiskDataSuzhou, self).__init__(params)

    def get_risk_data_list(self, search_value):
        fields = ('id', 'title', 'pubtime', 'url', 'source', 'score' )

        args = {}
        ac_id = Category.objects.get(name='风险快讯').id

        if not search_value:
            queryset = Article.objects.filter(categories__in=ac_id, status=1).values(*fields)
        else:
            queryset = Article.objects.filter(Q(title__contains=search_value) | Q(source__contains=search_value), status=1).values(*fields)
            queryset = queryset.filter(categories__in=ac_id)

        return queryset

class newsCrawlerData(Abstract):
    def __init__(self, user, params={}):
        super(newsCrawlerData, self).__init__(params)
        self.user = user

    def edit(self):
        word = getattr(self, 'word', '')
        page = getattr(self, 'page', '')
        thread = threading.Thread(target = newsCrawler, args = (word, page))
        thread.start()
        return 200


class StatisticsShow(Abstract):
    def __init__(self, params):
        super(StatisticsShow, self).__init__(params)


    def get_data(self):
        now = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        aWeek = -1-datetime.datetime.now().isoweekday() # 获取从上周六开始计算到今天获得的天数的负数
        today = datetime.datetime.now().date() # 获取今天日期的date类型
        monthInit = datetime.date(today.year, today.month, 1) # 获取本月的月初时间
        aMonth = (monthInit - today).days    #获取今天多少号的负数

        time_week = now + datetime.timedelta(days = aWeek)
        time_month = now + datetime.timedelta(days = aMonth)

        queryset = Article.objects.filter(pubtime__gte = time_month)

        if getattr(self, 'category', None) == '0001' or getattr(self, 'category', None) == '0002':
            category_id = getattr(self, 'category')
            category_ids = Article.objects.filter(categories__id = category_id).values_list('id', flat = True)
            queryset = queryset.filter(id__in = category_ids)
        if getattr(self, 'category', None) == '0003':
            category_business_ids = Article.objects.exclude(categories__id = '0001').exclude(categories__id = '0002').values_list('id', flat = True)
            queryset = queryset.filter(id__in = category_business_ids)



        user_id = 65
        listdata = []
        while(user_id <= 78):
            if User.objects.filter(id = user_id).exists():
                queryset_short = queryset
                if getattr(self, 'time', None) == '每日':
                    queryset_short = queryset.filter(pubtime__gte = now, user_id = user_id, status=1)
                elif getattr(self, 'time', None) == '每周':
                    queryset_short = queryset.filter(pubtime__gte = time_week, user_id = user_id, status=1)
                elif getattr(self, 'time', None) == '每月':
                    queryset_short = queryset.filter(pubtime__gte = time_month, user_id = user_id, status=1)
                else:
                    queryset_short = queryset.filter(pubtime__gte = time_week, user_id = user_id, status=1)

                data = {
                    'user': user_id,
                    'times': queryset_short.count(),
                }
                listdata.append(data)

            user_id += 1

        return listdata
