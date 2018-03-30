from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Article, ArticleArea, Category,
                                ArticleCategory, )
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


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