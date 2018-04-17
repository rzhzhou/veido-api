from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Article, ArticleArea, Category,
                                ArticleCategory, )
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format
from observer.utils.str_format import str_to_md5str


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
        }
        area_ids = getattr(self, 'areas', None)
        category_ids = getattr(self, 'categorys', None)

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Article.objects.filter(**args)

        if category_ids:
            c_ids = Category.objects.filter(parent=self.category, id__in=category_ids).values_list('id', flat=True)
            a_ids = ArticleCategory.objects.filter(category_id__in=c_ids).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)
        else:
            a_ids = ArticleCategory.objects.filter(category_id=self.category).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)

        if area_ids:
            a_ids = ArticleArea.objects.filter(area_id__in=area_ids[:-1:].split(',')).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)


        return queryset.values(*fields).order_by('-pubtime')


class RiskData(Abstract):

    def __init__(self, params):
        super(RiskData, self).__init__(params)

    def get_all(self):
        fields = ('guid', 'url', 'title', 'source', 'pubtime', 'score', )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'score': getattr(self, 'score', None),
        }
        area_ids = getattr(self, 'areas', None)

        args = dict([k, v] for k, v in cond.items() if v)
        queryset = Article.objects.filter(**args)

        if area_ids:
            a_ids = ArticleArea.objects.filter(area_id__in=area_ids[:-1:].split(',')).values_list('article_id', flat=True)
            queryset = queryset.filter(guid__in=a_ids)


        return queryset.values(*fields).order_by('-pubtime')


class RiskDataAdd(Abstract):

    def __init__(self, user, params={}):
        super(RiskDataAdd, self).__init__(params)
        self.user = user

    def add_dmlink(self):
        url = getattr(self, 'url', '')
        title = getattr(self, 'title', '')
        pubtime = getattr(self, 'pubtime', '')
        score = getattr(self, 'score', 0)
        source = getattr(self, 'source', '')
        areas = getattr(self, 'areas', '')
        categories = getattr(self, 'categories', '')

        if not url:
            return -1

        if not pubtime:
            return -2

        if not source:
            return -3

        if not areas:
            return -4

        if not categories:
            return -5

        guid = str_to_md5str(url)

        if Article.objects.filter(guid=guid).exists():
            return 2

        Article(
            guid=guid,
            title=title,
            url=url,
            pubtime=pubtime,
            source=source,
            score=score,
            risk_keyword='',
            invalid_keyword='',
            status=1,
        ).save()

        a_ids = areas.split(',')
        c_ids = categories.split(',')

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

        return 1


class RiskDataEdit(Abstract): 

    def __init__(self, params={}):
        super(RiskDataEdit, self).__init__(params)

    def edit_dmlink(self, did):
        edit_id = did
        name = getattr(self, 'name')
        link = getattr(self, 'link')
        kwords = getattr(self, 'kwords', '')
        fwords = getattr(self, 'fwords', '')
        remarks = getattr(self, 'remarks', '')

        if not name:
            return -1

        if not link:
            return -2

        try:
            dmlink = Article.objects.get(id=edit_id)
            dmlink.name = name
            dmlink.link = link
            dmlink.kwords = kwords
            dmlink.fwords = fwords
            dmlink.update_at = datetime.now()
            dmlink.status = 0
            dmlink.save()
            return 1
        except Exception as e:
            print(e)
            return 0


class RiskDataDelete(Abstract): 

    def __init__(self, user):
        self.user = user

    def del_dmlink(self, did):
        del_id = did

        try:
            Article.objects.get(id=del_id).delete()
            return 1
        except Exception as e:
            print(e)
            return 0


class DMWordsData(): 

    def get_all(self):
        fields = ('id', 'riskword', 'invalidword', 'industry__name', )

        queryset = Corpus.objects.all().values(*fields)

        return queryset
