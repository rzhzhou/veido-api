from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Article, ArticleCategory
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class ArticleData(Abstract):

    def __init__(self, params, category):
        self.article_guids = ArticleCategory.objects.filter(category=category).values_list('article_id', flat=True)
        super(ArticleData, self).__init__(params)

    def get_all(self):
        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'area_id': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Article.objects.filter(**args).filter(guid__in=self.article_guids).order_by('-pubtime')

        return queryset

