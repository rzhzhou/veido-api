from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import (Area, ArticleArea, ArticleCategory, 
                                Category, UserArea, AliasIndustry, )
from observer.utils.date_format import date_format


def areas(article_id):
    a_ids = ArticleArea.objects.filter(article_id=article_id).values_list('area_id', flat=True)
    queryset = Area.objects.filter(id__in=a_ids)

    if not queryset.exists():
        queryset = Area.objects.filter(name='全国')

    return list(map(lambda x: {'id': x['id'], 'text': x['name']}, queryset.values('id', 'name')))


def categories(article_id, admin=False):
    a_ids = ArticleCategory.objects.filter(article_id=article_id).values_list('category_id', flat=True)
    queryset = Category.objects.filter(id__in=a_ids)
    
    if not admin:
        queryset = queryset.filter(level=2)

    if not queryset.exists():
        queryset = Category.objects.filter(name='其它')
    
    return list(map(lambda x: {'id': x['id'], 'text': x['name']}, queryset.values('id', 'name')))


# 本地相关度算法
def local_related(article_id, user):
    f = lambda x, y : set(x).issubset(set(y)) or set(y).issubset(set(x))

    a_ids = ArticleArea.objects.filter(article_id=article_id).values_list('area_id', flat=True)
    u_area = UserArea.objects.get(user=user).area
    u_area_id = u_area.id
    u_level = u_area.level

    # 当前用户的地域存在于新闻中
    if u_area_id in a_ids:
        return 3
    else:
        # 当前用户的地域是省份城市
        if u_level == 2:
            if f(Area.objects.filter(parent=u_area).values_list('id', flat=True), a_ids):
                return 3
        # 当前用户的地域是市级城市
        elif u_level == 3:
            if u_area.parent.id in a_ids:
                return 2
            if f(Area.objects.filter(parent=u_area.parent).values_list('id', flat=True), a_ids):
                return 2

    # 不符合上述所有情况
    return 1


def area(area_id):
    return Area.objects.get(id=area_id).name


def industry(industry_id):
    return AliasIndustry.objects.get(id=industry_id).name
    

def qualitied(q):
    return '{0}%'.format('%.2f' % float(100.00 if not q else q * 100))