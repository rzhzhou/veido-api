from observer.apps.base.models import Area,Article as BaseArticle,Inspection as BaseInspection
from observer.apps.seer.models import AreaIndustry,Article as SeerArticle,Inspection as SeerInspection,\
                                      ConsumeIndex,SocietyIndex,ManageIndex,ModelWeight
from observer.apps.seer.service.abstract import Abstract
from datetime import datetime, timedelta
from django.db.models import Count,Q
from observer.utils.date.convert import data_format
import collections,itertools
from observer.apps.suzhou.service.util import cal_date_range,get_overall_overview_score,industries_ranking


class RiskProductData(Abstract):  # 风险产品

    def __init__(self, params={}):
        super(RiskProductData, self).__init__(params)

    def get_industries(self):
        area_industries = AreaIndustry.objects.filter(area__name=self.area_name) 
        return industries_ranking(area_industries,self.area_name,self.starttime,self.endtime) 

class RiskEnterprisesData(Abstract):  # 风险企业

    def __init__(self, params={}):
        super(RiskEnterprisesData, self).__init__(params)

    def get_enterprises(self):
        cond = {
            'pubtime__gte': getattr(self, 'start', self.starttime),
            'pubtime__lt': getattr(self, 'end', self.endtime),}
        args = dict([(k, v) for k, v in cond.items() if v is not None])
        uuids=BaseInspection.objects.filter(**args).values("guid")

        fields = ('enterprise_unqualified__id', 'enterprise_unqualified__name',
                  'enterprise_unqualified__area__name')
        cond = {
            'base_inspection__in':uuids,
            'enterprise_unqualified__area__id__in': Area.objects.filter(
                Q(parent__name=self.focus) |
                Q(name=self.focus)
            ).values_list('id', flat=True)
        }

        args = dict([(k, v) for k, v in cond.items() if v is not None])

        queryset = SeerInspection.objects.filter(
            **args).values_list(*fields).distinct().order_by('enterprise_unqualified__id')
        return queryset

class RiskInspectionData(Abstract):
    def __init__(self, params={}):
        super(RiskInspectionData, self).__init__(params)

    def get_inspection_list(self):
        fields = ('guid', 'title', 'pubtime', 'url', 'source', 'qualitied', 'product')
        keywords = getattr(self, 'search[value]', None)
        queryset = BaseInspection.objects.values(*fields)
        return queryset if not keywords else queryset.filter(Q(source__contains=keywords) | Q(title__contains=keywords))

class InternetRiskData(Abstract):
    def __init__(self, params={}):
        super(InternetRiskData, self).__init__(params)

    def trend_chart(self):
        # less than equal 4 months (122 = 31 + 31 + 30 + 30)
        if self.days > 0 and self.days <= 122:
            result =cal_date_range('day', self.days,self.starttime,self.endtime)
            result['categories'] = [i.strftime(
                '%m-%d') for i in result['categories']]

        elif self.days > 122:  # great than 4 months
            result =cal_date_range('month', self.days,self.starttime,self.endtime)
            result['categories'] = [i.strftime(
                '%Y-%m') for i in result['categories']]

        return result

    def get_industries(self):
        area_industries = AreaIndustry.objects.filter(area__name=self.area_name) 
        industries =industries_ranking(area_industries,self.area_name,self.starttime,self.endtime)

        return industries

    @property
    def map(self):
        provinces = list(Area.objects.filter(level=2).values('id', 'name'))
        cond = {
            'category__level': 1,
            'category__name': '风险新闻',
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = SeerArticle.objects.filter(**args).values('base_article')
        baseArticleList=BaseArticle.objects.filter(
                    guid__in=uuids,
                    pubtime__gte= self.starttime,
                    pubtime__lt= self.endtime
                ).exclude(
                    area=None
                ).values_list(
                    'area__id',
                    'area__parent__id'
                )
        risknews_area = zip(*list(baseArticleList))
        area_list=list(risknews_area)
        for province in provinces:
            cities_id = list(
                Area.objects.filter(
                    parent__id=province['id']
                ).values_list(
                    'id',
                    flat=True
                )
            )

            areas_id = cities_id + [province['id']]
            province['count'] = sum([
                sum(
                    map(
                        lambda x: area_list[0].count(x),
                        areas_id
                    )
                ),
                sum(
                    map(
                        # area__parent__id__in=cities_id
                        lambda x: area_list[1].count(x),
                        cities_id
                    )
                )
            ])

        return provinces

    @property
    def risk_level(self):
        self.days = (self.endtime - self.starttime).days
        cal_date_func = lambda x: (
            self.starttime + timedelta(days=x),
            self.starttime + timedelta(days=x + 1)
        )
        date_range = map(cal_date_func, range(self.days))
        date_range=list(date_range)
        date_range_len = len(date_range)
        if date_range_len <= 7:
            area_days = date_range[::]
            last_time = str((date_range[date_range_len-1][0]).strftime('%m-%d'))
            date = map(lambda x: x[0].strftime('%m-%d'), area_days)
            list(date).append(last_time)
        elif  7 < date_range_len <= 32:
            area_days = date_range[::int(date_range_len / 6)]
            last_time = str((date_range[date_range_len-1][0]).strftime('%m-%d'))
            date = map(lambda x: x[0].strftime('%m-%d'), area_days)
            list(date).append(last_time)
        elif date_range_len <= 190:
            area_days = date_range[::31]
            last_time = str((date_range[date_range_len-1][0]).strftime('20%y-%m'))
            date = map(lambda x: x[0].strftime('20%y-%m'), area_days)
            list(date).append(last_time)
        elif date_range_len <= 370:
            area_days = date_range[::61]
            last_time = str((date_range[date_range_len-1][0]).strftime('20%y-%m'))
            date = map(lambda x: x[0].strftime('20%y-%m'), area_days)
            list(date).append(last_time)

        area_score = []
        for index in area_days:
            pubtime = index[0].strftime('%Y-%m-%d')
            total_score = get_overall_overview_score(None,self.area_name,self.starttime,self.endtime)[0]
            area_score.append(total_score)
        last_datetime = (date_range[date_range_len-1][0]).strftime('20%y-%m-%d')
        last_datetimescore = get_overall_overview_score(None,self.area_name,self.starttime,self.endtime)[0]
        area_score.append(last_datetimescore)
        return (date, zip(date, area_score))

    @property
    def risk_product(self):
        products =self.get_industries()
        if len(products) >= 5:
            products = reversed(products[:5])
            return list(zip(*products))
        else:
            return ((), (), ())

    def get_all(self):
        data = {
            'map': self.map,
            'risk': self.trend_chart(),
            'risk_level': self.risk_level,
            'risk_product': self.risk_product,
            'summaries_score': get_overall_overview_score(None,self.area_name,self.starttime,self.endtime),
        }
        return data