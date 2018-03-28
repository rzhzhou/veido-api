from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Article, ArticleArea, ArticleCategory
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class ArticleData(Abstract):

    def __init__(self, params, category):
        self.category = category
        super(ArticleData, self).__init__(params)

    def get_all(self):
        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'score': getattr(self, 'score', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Article.objects.filter(**args)
        ac_guids = ArticleCategory.objects.filter(category=self.category).values_list('article_id', flat=True)
        area_ids = getattr(self, 'area', None)
        if area_ids:
            aa_guids = ArticleArea.objects.filter(area_id__in=area_ids).values_list('article_id', flat=True)
            return queryset.filter(guid__in=article_guids).filter(guid__in=aa_guids).order_by('-pubtime')
        else:
            return queryset.filter(guid__in=article_guids).order_by('-pubtime')
