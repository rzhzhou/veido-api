from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User, Group

from observer.base.models import (Area, Category, UserInfo, AliasIndustry, MajorIndustry,
                                Enterprise, UserNav, Article, HarmIndicator, HarmPeople)
from observer.apps.hqi.models import Indicator,IndicatorDataParent,Policy,PolicyData
from observer.utils.date_format import date_format


def areas(article_id, flat=False):
    a_ids = Article.objects.filter(id=article_id).values_list('areas__id', flat=True)
    queryset = Area.objects.filter(id__in=a_ids)

    if not queryset.exists():
        queryset = Area.objects.filter(name='全国')

    if not flat:
        return list(map(lambda x: {'id': x['id'], 'name': x['name']}, queryset.values('id', 'name')))
    else:
        return ','.join(queryset.values_list('name', flat=True))


def categories(article_id, admin=False, flat=False):
    c_ids = Article.objects.filter(id=article_id).values_list('categories__id', flat=True)
    queryset = Category.objects.filter(id__in=c_ids)

    if not admin:
        queryset = queryset.filter(level=2)

    if not queryset.exists():
        queryset = Category.objects.filter(name='其它')

    if not flat:
        return list(map(lambda x: {'id': x['id'], 'name': x['name']}, queryset.values('id', 'name')))
    else:
        return ','.join(queryset.values_list('name', flat=True))

#政策
def content(policydata_id, admin=False, flat=False):
    c_ids = PolicyData.objects.filter(id=policydata_id).values_list('content__id', flat=True)
    queryset = Policy.objects.using('hqi').filter(id__in=c_ids)

    if not admin:
        queryset = queryset.filter(level=2)

    if not queryset.exists():
        queryset = Policy.objects.using('hqi').filter(name='其它')

    if not flat:
        return list(map(lambda x: {'id': x['id'], 'name': x['name']}, queryset.values('id', 'name')))
    else:
        return ','.join(queryset.values_list('name', flat=True))

#指标
def indicatores(indicator_id, admin=False, flat=False):
    c_ids = IndicatorDataParent.objects.filter(id=indicator_id).values_list('indicatores__id', flat=True)
    queryset = Indicator.objects.using('hqi').filter(id__in=c_ids)

    if not admin:
        queryset = queryset.filter(level=2)

    if not queryset.exists():
        queryset = Indicator.objects.filter(name='其它')

    if not flat:
        return list(map(lambda x: {'id': x['id'], 'name': x['name']}, queryset.values('id', 'name')))
    else:
        return ','.join(queryset.values_list('name', flat=True))

# 本地相关度算法
def local_related(article_id, user):
    f = lambda x, y : set(x).issubset(set(y)) or set(y).issubset(set(x))

    area_ids = Article.objects.filter(id=article_id).values_list('areas__id', flat=True)
    u_area = UserInfo.objects.get(user=user).area
    u_area_id = u_area.id
    u_level = u_area.level

    # 当前用户的地域存在于新闻中
    if u_area_id in area_ids:
        return 3
    else:
        # 当前用户的地域是省份城市
        if u_level == 2:
            if f(Area.objects.filter(parent=u_area).values_list('id', flat=True), area_ids):
                return 3
        # 当前用户的地域是市级城市
        elif u_level == 3:
            if u_area.parent.id in area_ids:
                return 2
            if f(Area.objects.filter(parent=u_area.parent).values_list('id', flat=True), area_ids):
                return 2

    # 不符合上述所有情况
    return 1


def area(area_id, flat=False):
    queryset = Area.objects.get(id=area_id)

    if not flat:
        return {'id': queryset.id, 'name': queryset.name}
    else:
        return queryset.name

def gov_area(area_id, flat=False):
    queryset = Area.objects.get(id=area_id)

    if not flat:
        return [{'id': queryset.id, 'name': queryset.name}]
    else:
        return queryset.name

def get_major_industry(industry_id, flat=False):
    queryset = MajorIndustry.objects.get(id=industry_id)

    if not flat:
        return {'id': queryset.id, 'name': queryset.name}
    else:
        return queryset.name

def get_major_category(category_id, flat=False):
    queryset = Category.objects.get(id=category_id)

    if not flat:
        return {'id': queryset.id, 'name': queryset.name}
    else:
        return queryset.name


def alias_industry(alias_industry_id, flat=False):
    queryset = AliasIndustry.objects.get(id=alias_industry_id)

    if not flat:
        return {'id': queryset.id, 'text': queryset.name}
    else:
        return queryset.name


def involve_local(local_name, area_name):
        if local_name == area_name:
            return '是'
        else:
            return '否'


def industry_number(alias_industry_id):
    queryset = AliasIndustry.objects.get(id=alias_industry_id)

    return queryset.industry_id


def qualitied(q):
    return '{0}%'.format('%.2f' % float(0 if q == 0 else q * 100))


def enterprise_name(inspection_id, flat=False):
    # enterprise_ids = InspectionEnterprise.objects.filter(inspection_id=inspection_id).values_list('enterprise_id', flat=True)
    # queryset = Enterprise.objects.filter(id__in=enterprise_ids)

    # if not flat:
    #     return list(map(lambda x: {'id': x['id'], 'text': x['name']}, queryset.values('id', 'name')))
    # else:
    #     return ','.join(queryset.values_list('name', flat=True))
    return


def enterprise_unitem(inspection_id, flat=False):
    # enterprise_ids = InspectionEnterprise.objects.filter(inspection_id=inspection_id).values_list('enterprise_id', flat=True)
    # queryset = Enterprise.objects.filter(id__in=enterprise_ids)

    # if not flat:
    #     return list(map(lambda x: {'id': x['id'], 'text': x['unitem']}, queryset.values('id', 'unitem')))
    # else:
    #     return ','.join(queryset.values_list('unitem', flat=True))
    return


def enterprise_area_name(inspection_id, flat=False):
    # enterprise_ids = InspectionEnterprise.objects.filter(inspection_id=inspection_id).values_list('enterprise_id', flat=True)
    # area_ids = Enterprise.objects.filter(id__in=enterprise_ids).values_list('area_id', flat=True)
    # queryset = Area.objects.filter(id__in=area_ids)

    # if not flat:
    #     return list(map(lambda x: {'id': x['id'], 'text': x['name']}, queryset.values('id', 'name')))
    # else:
    #     return ','.join(queryset.values_list('name', flat=True))
    return


# def risk_injury(article_id):
#     c_ids = ArticleCategory.objects.filter(article_id=article_id).values_list('category_id', flat=True)
#     c_id = Category.objects.get(name="风险伤害").id

#     if c_id in c_ids:
#         return 1
#     return 0


def get_user_nav(user_id):
    return UserNav.objects.filter(user_id=user_id).values_list('nav_id', flat=True)


def get_user_extra(user_id):
    extra = {}
    groups = Group.objects.filter(user=user_id).values_list('name', flat=True)

    if '管理员' in groups:
        extra['groups'] = list(groups)
        extra['groups'].remove('管理员')
        # extra['groups'] = extra['groups'][0]
        extra['role'] = 1
    elif '超级管理员' in groups:
        extra['groups'] = list(groups)
        extra['groups'].remove('超级管理员')
        # extra['groups'] = extra['groups'][0]
        extra['role'] = 2
    else:
        extra['groups'] = list(groups)
        extra['role'] = 0

    return extra


def harmName(harm_id):
    harmIndicator = HarmIndicator.objects.filter(id=harm_id).values_list('name', flat=True)
    name = list(harmIndicator)

    return name[0]


def harmPeople(harm_id):
    harmpeople = HarmPeople.objects.filter(harm_id=harm_id).values('age', 'sex')

    return list(map(lambda x: {'age': harmName(x['age']), 'sex': harmName(x['sex'])}, harmpeople))


def countPeople(harm_id):
    harmpeople = HarmPeople.objects.filter(harm_id=harm_id)

    return harmpeople.count()
