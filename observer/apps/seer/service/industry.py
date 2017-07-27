# -*- coding: utf-8 -*-
import operator

from random import randint
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from itertools import chain
from collections import Counter
from datetime import date, datetime, timedelta

from observer.utils.date.convert import (datetime_to_timestamp, utc_to_local_time)
from observer.apps.origin.models import (Inspection, IndustryScore)
from observer.apps.penalty.models import AdministrativePenalties
from observer.apps.seer.models import (RiskNews, AreaIndustry, Industry,
                                    ManageIndex, SocietyIndex, ConsumeIndex,
                                    UserArea, ModelWeight)
from observer.apps.seer.service.news import NewsQuerySet
from observer.apps.seer.service.abstract import Abstract


class IndustryTrack(Abstract):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)
        self.news_query_set = NewsQuerySet(params)
        self.days = (self.end - self.start).days
        self.area_name = getattr(self, 'area_name', 
            getattr(self, 'area', UserArea.objects.get(user__id=self.user_id).area.name))
            
    def trend_chart(self):
        # less than equal 4 months (122 = 31 + 31 + 30 + 30)
        if self.days > 0 and self.days <= 122:
            result = self.news_query_set.cal_date_range('day', self.days)
            result['categories'] = [i.strftime(
                '%m-%d') for i in result['categories']]

        elif self.days > 122:  # great than 4 months
            result = self.news_query_set.cal_date_range('month', self.days)
            result['categories'] = [i.strftime(
                '%Y-%m') for i in result['categories']]

        return result

    def compare_chart(self):
        return self.compare(self.start, self.end, self.industry)

    def get_chart(self):
        return (self.trend_chart(), self.compare_chart())

    def get_dimension(self, industry=None):
        industry = industry if industry else getattr(self, 'industry', None)

        c = ConsumeIndex.objects.filter(
            industry__id=industry, 
            area__name=self.area_name
        )
        s = SocietyIndex.objects.filter(
            industry__id=industry, 
            area__name=self.area_name
        )
        m = ManageIndex.objects.filter(
            industry__id=industry, 
            area__name=self.area_name
        )
        n_dimension = RiskNews.objects.filter(
            industry__id=industry, 
            pubtime__gte=self.start,
            pubtime__lt=self.end,
            status=1
        )
        i1_dimension = Inspection.objects.filter(
            industry__id=industry, 
            qualitied__lt=1,
            pubtime__gte=self.start,
            pubtime__lt=self.end,
            area__name=self.area_name
        )
        i2_dimension = Inspection.objects.filter(
            industry__id=industry, 
            qualitied__lt=1,
            pubtime__gte=self.start,
            pubtime__lt=self.end
        ).exclude(area__name=self.area_name)

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
            Counter(
                    map(
                        lambda x: x['risk_keyword'], 
                        n_dimension.values('risk_keyword') 
                        if n_dimension.values('risk_keyword') 
                        else [{'risk_keyword':'0'}]
                        )
                    ).values()
            ) else 1

        n_count = n_dimension.count()

        if self.days > 360:
            n_count = n_count / 12
        elif self.days > 180:
            n_count = n_count / 6
        elif self.days > 90:
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
            (list(chain(i1_dimension, i2_dimension)), i_score, i1_score, i2_score),
        )

    def get_overall_overview_score(self, industry=None):
        all_dimensions = self.get_dimension(industry)
        model_weight = ModelWeight.objects.get(area__name=self.area_name, industry__isnull=True)
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
            'area__name': getattr(
                self,
                'area_name',
                UserArea.objects.get(user__id=self.user_id).area.name
            ),
            'industry__name': getattr(self, 'name', None),
            'industry__level': getattr(self, 'level', None),
            'industry__parent__id': getattr(self, 'parent', None),
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])
        status = getattr(self, 'status', None)
        area_industries = AreaIndustry.objects.filter(**args) 
        opt = reduce(operator.or_,(Q(status__contains=x) for x in status.split(',')))
        industries = self.industries_ranking(area_industries if not status else area_industries.filter(opt))

        if self.area_name == u'苏州':
            compare_1 = map(lambda x: x[:3], industries)
            self.start = self.start - timedelta(days=30)
            self.end = self.end - timedelta(days=30)
            compare_2 = map(lambda x: x[:3], self.industries_ranking(user_industries))

            for index, item in enumerate(industries):
                item[5] = index - compare_2.index(compare_1[index])

        return industries        

    def while_risk(self):
        while_risk_data = []
        while_risk_datetime = []
        total_score = []
        date_list = map(
                    lambda x: (
                        self.start + timedelta(days=x),
                        self.start + timedelta(days=x + 1)
                        ), 
                    xrange(self.days))[::-1][:7:]
        for d in date_list:
            self.start = d[0]
            self.end = d[1]
            total_score.append(self.get_overall_overview_score()[0])
            while_risk_datetime.append(datetime.strftime(self.end, "%m-%d"))
            while_risk_data.append(self.get_industries())

        while_risk_data.append(while_risk_datetime)
        while_risk_data.append(total_score)

        return while_risk_data

    def penalty(self):
        return AdministrativePenalties.objects.filter(
            industry=Industry.objects.get(id=self.industry).name,
            pubtime__gte=self.start,
            pubtime__lt=self.end
        ).values('id', 'title', 'url', 'publisher', 'pubtime')

    def industry_everyday_score(self):
        queryset = IndustryScore.objects.filter(
            time__gte=self.start, 
            time__lt=self.end, 
            industry__id=getattr(self, 'industry', None)
        ).values('score', 'time')
        
        if queryset:
            return zip(*sorted([(
                utc_to_local_time(q.get('time')).strftime('%m-%d'),
                q.get('score') if q.get('score') is not None else 0
            ) for q in queryset], key=lambda data: data[0]))
        else:
            return [[], []]

    def get_all(self):
        data = {
            'name': Industry.objects.get(pk=self.industry).name,
            'risk_rank': self.get_overall_overview_score(),
            'indicators': self.get_dimension(),
            'trend': self.trend_chart(),
            'industry_everyday_score': self.industry_everyday_score(),
            'penalty':self.penalty()
        }
        return data
