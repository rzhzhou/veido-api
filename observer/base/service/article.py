import openpyxl
from io import BytesIO
import threading

import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, Article, ArticleArea, 
                                Category, ArticleCategory, )
from django.contrib.auth.models import Group
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
        fields = ('guid', 'url', 'title', 'source', 'pubtime', 'score', )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'score': getattr(self, 'score', None),
            'status': 1, 
        }
        area_ids = getattr(self, 'areas', None)
        category_ids = getattr(self, 'categories', None)
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Article.objects.filter(**args)

        if category_ids:
            a_ids = ArticleCategory.objects.filter(category_id=category_ids).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)
        else:
            c_ids = Category.objects.filter(parent__id=self.category).values_list('id', flat=True)
            if not c_ids:
                a_ids = ArticleCategory.objects.filter(category_id=self.category).values_list('article_id', flat=True)
            else:
                a_ids = ArticleCategory.objects.filter(category_id__in=c_ids).values_list('article_id', flat=True)
            
            queryset = queryset.filter(guid__in=a_ids)

        if area_ids:
            a_ids = ArticleArea.objects.filter(area_id__in=area_ids[:-1:].split(',')).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)


        return queryset.values(*fields).order_by('-pubtime')


class RiskData(Abstract):

    def __init__(self, user, params):
        super(RiskData, self).__init__(params)
        self.user = user

    def get_all(self):
        fields = ('guid', 'url', 'title', 'source', 'pubtime', 'score', 'status' )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'score': getattr(self, 'score', None),
            'status': getattr(self, 'status', None),
            'industry_id': getattr(self, 'industry', None),
        }
        area_ids = getattr(self, 'areas', None)
        cond_category = {'category_id' : getattr(self, 'category', None)}

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Article.objects.exclude(status=-1).filter(**args)

        if area_ids:
            a_ids = ArticleArea.objects.filter(area_id__in=area_ids[:-1:].split(',')).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)

        args_category = dict([k, v] for k, v in cond_category.items() if v)
        if args_category != {}:
            guid_ids = ArticleCategory.objects.filter(**args_category).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=guid_ids)

        # 判断当前用户是否为武汉深度网科技有限公司成员，然后取出该用户管理的资料
        group_ids = Group.objects.filter(user=self.user).values_list('id', flat=True)
        if 4 in group_ids and 3 in group_ids:
            queryset = queryset.filter(corpus_id = self.user.id).values(*fields)

        queryset = queryset.values(*fields).order_by('-pubtime')
            
        return queryset


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

        if not url or not pubtime or not source or not areas or not categories:
            return 400

        guid = str_to_md5str(url)

        if Article.objects.filter(guid=guid).exists():
            return 202

        Article(
            guid=guid,
            title=title,
            url=url,
            pubtime=pubtime,
            source=source,
            score=score,
            status=1,
        ).save()

        a_ids = areas.split(',')[:-1:]
        c_ids = categories.split(',')[:-1:]

        for a_id in a_ids:
            if not ArticleArea.objects.filter(article_id=guid, area_id=a_id).exists():
                ArticleArea(
                    article_id=guid,
                    area_id=a_id,
                ).save()

        for c_id in c_ids:
            if not ArticleCategory.objects.filter(article_id=guid, category_id=c_id).exists():
                ArticleCategory(
                    article_id=guid,
                    category_id=c_id,
                ).save()

        return 200


class RiskDataAudit(Abstract):
    def __init__(self, params={}):
        super(RiskDataAudit, self).__init__(params)

    def edit(self, aid):
        del_ids = aid
        for ids in del_ids.split(","):
            Article.objects.filter(guid=ids).update(status=1)

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

        article = Article.objects.get(guid=edit_id)
        article.title = title
        article.pubtime = pubtime
        article.score = score
        article.source = source
        article.save()

        a_ids = areas.split(',')[:-1:]
        c_ids = categories.split(',')[:-1:]

        ArticleArea.objects.filter(article_id=edit_id).delete()
        ArticleCategory.objects.filter(article_id=edit_id).delete()

        for a_id in a_ids:
            if not ArticleArea.objects.filter(article_id=edit_id, area_id=a_id).exists():
                ArticleArea(
                    article_id=edit_id,
                    area_id=a_id,
                ).save()

        for c_id in c_ids:
            if not ArticleCategory.objects.filter(article_id=edit_id, category_id=c_id).exists():
                ArticleCategory(
                    article_id=edit_id,
                    category_id=c_id,
                ).save()

        return 200


class RiskDataDelete(Abstract):

    def __init__(self, user):
        self.user = user

    def delete(self, aid):
        del_ids = aid
        for ids in del_ids.split(","):
            Article.objects.filter(guid=ids).delete()

        return 200


class RiskDataUpload(Abstract):

    def __init__(self, user):
        self.user = user

    def upload(self, filename, file_obj):
        #Model weight
        model = {'GUID': 0, '标题': 0, 'URL': 0, '发布时间': 0, '来源': 0, '风险程度': 0, '地域': 0, '类别': 0, '行业编号': 0}
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
                    title = sv(i, model['标题'], sheet)
                    url = sv(i, model['URL'], sheet)

                    if not url:
                        continue

                    pubtime = date_format(sv(i, model['发布时间'], sheet))
                    if not pubtime:
                        return {
                            'status': 0,
                            'message': '操作失败！Excel %s 行时间格式有误！' % (i + 1, )
                        }

                    source = sv(i, model['来源'], sheet)
                    score = sv(i, model['风险程度'], sheet)
                    area = sv(i, model['地域'], sheet)
                    category = sv(i, model['类别'], sheet)
                    industry_id = sv(i, model['行业编号'], sheet)

                    total += 1

                    a_guid = str_to_md5str(url)

                    if Article.objects.filter(guid=a_guid).exists():
                        dupli += 1
                        continue

                    areas = area.split(',')
                    a_ids = Area.objects.filter(name__in=areas).values_list('id', flat=True)
                    categories = category.split(',')
                    c_ids = Category.objects.filter(name__in=categories).values_list('id', flat=True)
                    for a_id in a_ids:
                        if not ArticleArea.objects.filter(article_id=a_guid, area_id=a_id).exists():
                            ArticleArea(
                                article_id=a_guid,
                                area_id=a_id,
                            ).save()

                    for c_id in c_ids:
                        if not ArticleCategory.objects.filter(article_id=a_guid, category_id=c_id).exists():
                            ArticleCategory(
                                article_id=a_guid,
                                category_id=c_id,
                            ).save()

                    Article(
                        guid=a_guid,
                        title=title,
                        url=url,
                        pubtime=pubtime,
                        source=source,
                        score=score,
                        industry_id=industry_id,
                        corpus_id=self.user.id,
                        status=1,
                    ).save()

                except Exception as e:
                    return {
                        'status': 0,
                        'message': '操作失败！Excel %s 行存在问题。详细错误信息：%s！' % (i + 1, e)
                    }

        return {
                    'status': 1,
                    'message': '操作成功！共处理%s条数据，成功导入%s条数据，重复数据%s条！' % (total, total - dupli, dupli, )
                }


class RiskDataExport(Abstract):

    def __init__(self, user):
        self.user = user

    def export(self):
        filename = "articles.xlsx"

        # process data
        data = [
            ['GUID', '标题', 'URL', '发布时间', '来源', '发布者', '风险程度', '地域', '类别', ],
        ]
        months = get_months()[-1::][0]
        start = months[0].strftime('%Y-%m-%d')
        end = months[1].strftime('%Y-%m-%d')

        queryset = Article.objects.filter(pubtime__gte=start, pubtime__lt=end).values('guid', 'title', 'url', 'pubtime', 'source', 'score')

        for q in queryset:
            data.append([q['guid'],
                         q['title'],
                         q['url'],
                         date_format(q['pubtime'], '%Y-%m-%d'),
                         q['source'],
                         q['score'],
                         areas(q['guid'], flat=True),
                         categories(q['guid'], flat=True)])

        # write file
        write_by_openpyxl(filename, data)

        return open(filename, 'rb')


class RiskDataSuzhou(Abstract):

    def __init__(self, params={}):
        super(RiskDataSuzhou, self).__init__(params)

    def get_risk_data_list(self, search_value):
        fields = ('guid', 'title', 'pubtime', 'url', 'source', 'score' )

        args = {}
        a_ids = ArticleCategory.objects.filter(category_id='0002').values_list('article_id', flat=True)

        if not search_value:
            queryset = Article.objects.exclude(status=0).filter(guid__in=a_ids).values(*fields)
        else:
            queryset = Article.objects.exclude(status=0).filter(Q(title__contains=search_value) | Q(source__contains=search_value)).values(*fields)
            queryset = queryset.filter(guid__in=a_ids)

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


class StatisticsShow(object):
    def __init__(self):
        self.StatisticsShow = StatisticsShow


    def get_data(self):
        now = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        now =now + datetime.timedelta(hours=8, minutes=00, seconds=00)
        time_week = now + datetime.timedelta(days = -7)
        time_month = now + datetime.timedelta(days = -31)

        queryset = Article.objects.filter(pubtime__gte = time_month)
        
        user_id = 65
        listdata = []
        while(user_id <= 71):
            queryset_oneday = queryset.filter(pubtime__gte = now, corpus_id = user_id, status=1)
            queryset_week = queryset.filter(pubtime__gte = time_week, corpus_id = user_id, status=1)
            queryset_month = queryset.filter(pubtime__gte = time_month, corpus_id = user_id, status=1)
            data = {
                'user': user_id,
                'onedayNum': queryset_oneday.count(),
                'weekNum': queryset_week.count(),
                'month': queryset_month.count(),
            }
            listdata.append(data)
            user_id += 1

        return listdata

    


        