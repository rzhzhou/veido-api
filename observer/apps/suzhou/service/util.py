from datetime import datetime, timedelta
import collections,itertools
from django.db.models import Case, IntegerField, Sum, When, Max
from observer.utils.date.convert import utc_to_local_time
from observer.apps.base.models import Area,Article as BaseArticle,Inspection as BaseInspection
from observer.apps.seer.models import AreaIndustry,Article as SeerArticle,Inspection as SeerInspection,\
                                      ConsumeIndex,SocietyIndex,ManageIndex,ModelWeight   

def cal_news_nums(date_range, x_axis_units,start,end):
    cond = {
        'pubtime__gte': start,
        'pubtime__lt': end,
    }
    args = dict([(k, v) for k, v in cond.items() if v ])
    if x_axis_units == 'day':
        aggregate_args = dict([(
            start.strftime('%Y-%m-%d %H:%M:%S'),
            Sum(
                Case(
                    When(pubtime__gte=start, pubtime__lt=end, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ) for start, end in date_range])
    elif x_axis_units == 'month':
        aggregate_args = dict([(
            datetime(year, month, 1).strftime(
                '%Y-%m-%d %H:%M:%S'),  
            Sum(
                Case(
                    When(pubtime__year=year, pubtime__month=month, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ) for year, month in date_range])
    cond = {
        'category__level': 1,
        'category__name': '风险新闻',
    }
    args = dict([k, v] for k, v in cond.items() if v)
    uuids = SeerArticle.objects.filter(**args).values('base_article')
    queryset =  baseArticleList=BaseArticle.objects.filter(
                    guid__in=uuids,
                    pubtime__gte= start,
                    pubtime__lt= end
                ).aggregate(**aggregate_args)
    if queryset:
        # Convert $queryset
        # key:      str     ->  local datetime
        # value:    None    ->  0
        result = [(
            utc_to_local_time(k),
            v if v is not None else 0
        ) for k, v in queryset.items()]
        # sorted by $queryset key
        return zip(*sorted(result, key=lambda data: data[0]))

    return [[], []]

def cal_date_range(x_axis_units, days,start,end):
    if x_axis_units == 'day':
        cal_date_func = lambda x: (
            start + timedelta(days=x),
            start + timedelta(days=x + 1)
        )

        date_range = map(cal_date_func, range(days))

    elif x_axis_units == 'month':
        cal_date_func = lambda month: (year, month)

        if end.year == start.year:
            year = end.year
            iterable = range(start.month + 1, end.month + 1)

            date_range = map(cal_date_func, iterable)

        elif end.year - start.year == 1:
            year = start.year
            iterable = range(start.month + 1, 13)
            date_range_one = map(cal_date_func, iterable)

            year = end.year
            iterable = range(1, end.month + 1)
            date_range_two = map(cal_date_func, iterable)

            date_range = date_range_one + date_range_two

        else:
            years = end.year - start.year

            year = start.year
            iterable = range(start.month + 1, 13)
            date_range_one = map(cal_date_func, iterable)

            year = end.year
            iterable = range(1, end.month + 1)
            date_range_two = map(cal_date_func, iterable)
            date_range = list(date_range_one) + list(date_range_two)

            for y in range(1, years):
                year = start.year + y
                iterable = range(1, 13)
                date_range += list(map(cal_date_func, iterable))

    result = cal_news_nums(date_range, x_axis_units,start,end)
    result_list=list(result)
    return {
        'categories': result_list[0],
        'data': result_list[1]
    }

def get_dimension(industry=None,area_name='全国',starttime=None,endtime=None):
    days=None
    if starttime and endtime:
        days = (endtime - starttime).days
    c = ConsumeIndex.objects.filter(
        industry__id=industry, 
        area__name=area_name
    )
    s = SocietyIndex.objects.filter(
        industry__id=industry, 
        area__name=area_name
    )
    m = ManageIndex.objects.filter(
        industry__id=industry, 
        area__name=area_name
    )
    cond1 = {
        'category__level': 1,
        'category__name': '风险新闻',
        'industry__id':industry
    }
    cond2 = {
        'guid__in': SeerArticle.objects.filter(**cond1).values('base_article'),
        'pubtime__gte': starttime,
        'pubtime__lt': endtime,
    }
    n_dimension = BaseArticle.objects.filter(**cond2).order_by('-pubtime')  
    cond3 = {
        'guid__in': SeerInspection.objects.filter(industry__id=industry).values('base_inspection'),
        'pubtime__gte': starttime,
        'pubtime__lt': endtime,
        'qualitied__lt':1,
        'area__name':area_name
    }
    i1_dimension = BaseInspection.objects.filter(**cond3).order_by('-pubtime')      
    cond4 = {
        'guid__in': SeerInspection.objects.filter(industry__id=industry).values('base_inspection'),
        'pubtime__gte': starttime,
        'pubtime__lt': endtime,
        'qualitied__lt':1,
    }
    i2_dimension = BaseInspection.objects.filter(**cond4).order_by('-pubtime').exclude(area__name='全国')
    c_dimension = (c[0].force,
                 c[0].close,
                 c[0].consume) if c else (0, 1, 0)
    s_dimension = (s[0].trade, 
                s[0].qualified, 
                s[0].accident) if s else (1, 1, 1)
    m_dimension = (m[0].licence, 
                m[0].productauth, 
                m[0].encourage, 
                m[0].limit, 
                m[0].remove) if m else (0, 0, 0, 0, 0)

    c_score = 100 - (50 * c_dimension[0] 
                    + 25 * (c_dimension[1] - 1) 
                    + 50 * c_dimension[2]) / 3
    s_score = 100 - ((50 * (s_dimension[0] - 1)) 
                    + (50 * (s_dimension[1] - 1)) 
                    + (50 * (s_dimension[2] - 1))) / 3
    m_score = 100 - (100 * m_dimension[0] 
                    + 100 * m_dimension[1] 
                    + 100 * m_dimension[2] 
                    + 100 * m_dimension[3] 
                    + 100 * m_dimension[4]) / 5

    # 根据风险关键词出现的次数, 来判断单条新闻权重值
    n_weight = 1.2 if True in map(
        lambda y : y > 10, 
        collections.Counter(
                map(
                    lambda x: x['risk_keyword'], 
                    n_dimension.values('risk_keyword') 
                    if n_dimension.values('risk_keyword') 
                    else [{'risk_keyword':'0'}]
                    )
                ).values()
        ) else 1

    n_count = n_dimension.count()

    if int(days) > 360:
        n_count = n_count / 12
    elif int(days) > 180:
        n_count = n_count / 6
    elif int(days) > 90:
        n_count = n_count / 3

    if n_count > 800:
        n_score = 60 - (n_count * 0.02 * n_weight)
    elif n_count > 60:
        n_score = n_count - 60
        n_score = 60 - (n_count * 0.05 * n_weight)
    else:
        n_score = 100 - (n_count * 0.5 * n_weight)

    i1_score = (100 - i1_dimension.count() * 10)
    i2_score = (100 - i2_dimension.count() * 10)
    i_score = (i1_score + i2_score) * 0.5 
    i_score = randint(55, 60) if i_score < 30 else i_score

    return (
        (c_dimension, c_score),
        (s_dimension, s_score),
        (m_dimension, m_score),
        (n_dimension, n_score),
        (list(itertools.chain(i1_dimension, i2_dimension)), i_score, i1_score, i2_score),
    )

def get_overall_overview_score(industry,area_name,starttime,endtime):
    all_dimensions = get_dimension(industry,area_name,starttime,endtime)
    model_weight = ModelWeight.objects.get(area__name=area_name)
    return (round(
        all_dimensions[0][1] * model_weight.consume_index
        + all_dimensions[1][1] * model_weight.society_index 
        + all_dimensions[2][1] * model_weight.manage_index 
        + all_dimensions[3][1] * model_weight.risk_news_index 
        + all_dimensions[4][2] * (model_weight.inspection_index - 0.04)
        + all_dimensions[4][3] * 0.04, 2), 
        all_dimensions[3][1], 
        all_dimensions[4][1])

def industries_ranking(user_industries,area_name,starttime,endtime):
    return sorted(map(lambda u:[u.industry.id,
                     u.name,
                     u.industry.level,
                     get_overall_overview_score(u.industry.id,area_name,starttime,endtime)[0],
                     u.status,0],user_industries),key=lambda industry: industry[3])