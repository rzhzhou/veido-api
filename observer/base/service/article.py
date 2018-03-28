from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Article, Category, ArticleCategory
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class ArticleData(Abstract):  # 行业列表

    def __init__(self, params):
        super(IndustryData, self).__init__(params)

    def get_all(self):
        category = getattr(self, 'category')
        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'title', None),
            'source__contains': getattr(self, 'source', None),
            'area_id__in': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Article.objects.filter(**args).order_by('-pubtime')

        return queryset

