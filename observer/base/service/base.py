from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import (Area, ArticleArea, ArticleCategory, 
                                Category, )
from observer.utils.date_format import date_format


def area(article_id):
    a_ids = ArticleArea.objects.filter(article_id=article_id).values_list('area_id', flat=True)
    a_names = Area.objects.filter(id__in=a_ids).values_list('name', flat=True)

    return a_names if a_names else '未知'


def category(article_id):
    a_ids = ArticleCategory.objects.filter(article_id=article_id).values_list('category_id', flat=True)
    try:
        return Category.objects.get(level=2, id=a_ids).name
    except ObjectDoesNotExist:
        return '未知'