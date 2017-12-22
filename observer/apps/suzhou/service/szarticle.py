from observer.apps.base.models import Area,Article as BaseArticle,Inspection as BaseInspection
from observer.apps.seer.models import AreaIndustry,Article as SeerArticle,Inspection as SeerInspection,\
                                      ConsumeIndex,SocietyIndex,ManageIndex,ModelWeight
from observer.apps.seer.service.abstract import Abstract
from datetime import datetime, timedelta
from django.db.models import Count
from observer.utils.date.convert import data_format
import collections,itertools


class RiskProductData(Abstract):  # 风险产品

    def __init__(self, params={}):
        super(RiskProductData, self).__init__(params)

    def get_dimension(self, industry=None):
        c = ConsumeIndex.objects.filter(
            industry__id=industry, 
            area__name='全国'
        )
        s = SocietyIndex.objects.filter(
            industry__id=industry, 
            area__name='全国'
        )
        m = ManageIndex.objects.filter(
            industry__id=industry, 
            area__name='全国'
        )
        cond1 = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
            'industry__id':industry
        }
        cond2 = {
            'guid__in': SeerArticle.objects.filter(**cond1).values('base_article'),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        n_dimension = BaseArticle.objects.filter(**cond2).order_by('-pubtime')  
        cond3 = {
            'guid__in': SeerInspection.objects.filter(industry__id=industry).values('base_inspection'),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'qualitied__lt':1,
            'area__name':'全国'
        }
        i1_dimension = BaseInspection.objects.filter(**cond3).order_by('-pubtime')      
        cond4 = {
            'guid__in': SeerInspection.objects.filter(industry__id=industry).values('base_inspection'),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
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

        if int(self.days) > 360:
            n_count = n_count / 12
        elif int(self.days) > 180:
            n_count = n_count / 6
        elif int(self.days) > 90:
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

    def get_overall_overview_score(self, industry=None):
        all_dimensions = self.get_dimension(industry)
        model_weight = ModelWeight.objects.get(area__name=self.area_name)
        return (round(
            all_dimensions[0][1] * model_weight.consume_index
            + all_dimensions[1][1] * model_weight.society_index 
            + all_dimensions[2][1] * model_weight.manage_index 
            + all_dimensions[3][1] * model_weight.risk_news_index 
            + all_dimensions[4][2] * (model_weight.inspection_index - 0.04)
            + all_dimensions[4][3] * 0.04, 2), 
            all_dimensions[3][1], 
            all_dimensions[4][1])

    def industries_ranking(self, user_industries):
        return sorted(
            map(
                lambda u:[u.industry.id,
                         u.name,
                         u.industry.level,
                         self.get_overall_overview_score(industry=u.industry.id)[0],
                         u.status,
                         0],
                    user_industries),
                  key=lambda industry: industry[3])

    def get_industries(self):
        cond = {
            'area__name': self.area_name,
            'industry__name': getattr(self, 'name', None),
            'industry__level': getattr(self, 'level', None),
            'industry__parent__id': getattr(self, 'parent', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)
        status = getattr(self, 'status', None)
        area_industries = AreaIndustry.objects.filter(**args) 
        industries = self.industries_ranking(area_industries)

        return industries 


class RiskEnterprisesData(Abstract):  # 风险企业

    def __init__(self, params={}):
        super(RiskEnterprisesData, self).__init__(params)

    def get_enterprises(self):
        fields = ('enterprise_unqualified__id', 'enterprise_unqualified__name',
                  'enterprise_unqualified__area__name', 'enterprise_unqualified__product_name',)

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'enterprise_unqualified__area__id__in': Area.objects.filter(
                Q(parent__name=self.focus) |
                Q(name=self.focus)
            ).values_list('id', flat=True)
        }

        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = SeerInspection.objects.filter(
            **args).values_list(*fields).distinct().order_by('enterprise_unqualified__id')

        return queryset