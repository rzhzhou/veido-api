# -*- coding: utf-8 -*-
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta

from observer.utils.date.convert import datetime_to_timestamp
from observer.apps.origin.models import Inspection
from observer.apps.riskmonitor.models import (
    RiskNews, ScoreIndustry, UserIndustry, Industry, ManageIndex, SocietyIndex, ConsumeIndex)
from observer.apps.riskmonitor.service.news import NewsQuerySet


class IndustryTrack(NewsQuerySet):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)

    def trend_chart(self):
        self.days = (self.end - self.start).days

        # less than equal 4 months (122 = 31 + 31 + 30 + 30)
        if self.days > 0 and self.days <= 122:
            result = self.cal_date_range('day')
            result['categories'] = [i.strftime(
                '%m-%d') for i in result['categories']]

        elif self.days > 122:  # great than 4 months
            result = self.cal_date_range('month')
            result['categories'] = [i.strftime(
                '%Y-%m') for i in result['categories']]

        return result

    def compare_chart(self):
        return self.compare(self.start, self.end, self.industry)

    def get_chart(self):
        return (self.trend_chart(), self.compare_chart())

    def count_consume_index_socre(self):
        score = 100
        return score

    def count_society_index_socre(self):
        score = 100
        return score

    def count_manage_index_index_socre(self):
        score = 100
        return score

    def count_risk_news_score(self):
        score = 100

        n_dimension = RiskNews.objects.filter(
            industry__id=self.industry, pubtime__gte=self.start, pubtime__lt=self.end)

        risk_keyword__ids = map(
            lambda x: x['risk_keyword__id'], n_dimension.values('risk_keyword__id'))

        # [x['ri'] for x in n_dimension.values('risk_keyword__id')]
        risk_keywords_set = set(risk_keyword__ids)

        for risk_keyword_id in risk_keywords_set:

            # 得到每个风险关键词出现的次数
            count = risk_keyword__ids.count(risk_keyword_id)

            #如果一个风险关键词出现次数过高, 就让其分值变大
            if count > 10:
                score -= 0.5 * 1.2 * count
            else:
                score -= 0.5 * count

        if score < 60:
            score = 60

        return score

    def count_risk_inspection_socre(self):
        score = 100
        return score

    def get_risk_rank(self):
        risk_rank_score = ((self.count_consume_index_socre() + self.count_society_index_socre() +
                            self.count_manage_index_index_socre() + self.count_risk_news_score() +
                            self.count_risk_inspection_socre()) / 5)

        if 60 <= risk_rank_score < 70:
            risk_rank_color = '#bc3f2b'
        elif 70 <= risk_rank_score < 90:
            risk_rank_color = '#6586a1'
        else:
            risk_rank_color = '#95c5ab'

        if 60 <= risk_rank_score < 70:
            risk_rank_word = 'C'
        elif 70 <= risk_rank_score < 90:
            risk_rank_word = 'B'
        else:
            risk_rank_word = 'A'

        return (risk_rank_word, risk_rank_score, risk_rank_color)

    def get_dimension(self):
        c = ConsumeIndex.objects.filter(industry__id=self.industry)
        s = SocietyIndex.objects.filter(industry__id=self.industry)
        m = ManageIndex.objects.filter(industry__id=self.industry)
        n_dimension = RiskNews.objects.filter(
            industry__id=self.industry, pubtime__gte=self.start, pubtime__lt=self.end)
        i_dimension = Inspection.objects.filter(industry__id=self.industry)

        c_dimension = (c[0].force, c[0].close, c[
                       0].consume) if c else (0, 1, 0)
        c_score = (100 * c_dimension[0] + 50 *
                   (c_dimension[1] - 1) + 100 * c_dimension[2]) / 3
        if 0 <= c_score < 34:
            c_color = '#bc3f2b'
        elif 34 <= c_score < 67:
            c_color = '#6586a1'
        else:
            c_color = '#95c5ab'

        s_dimension = (s[0].trade, s[0].qualified, s[
                       0].accident) if s else (1, 1, 1)
        s_score = (50 * (s_dimension[0] - 1) + 50 *
                   (s_dimension[1] - 1) + 50 * (s_dimension[2] - 1)) / 3
        if 0 <= s_score < 34:
            s_color = '#bc3f2b'
        elif 34 <= s_score < 67:
            s_color = '#6586a1'
        else:
            s_color = '#95c5ab'

        m_dimension = (m[0].licence, m[0].productauth, m[0].encourage, m[
                       0].limit, m[0].remove) if m else (0, 0, 0, 0, 0)
        m_score = (100 * m_dimension[0] + 100 * m_dimension[1] + 100 *
                   m_dimension[2] + 100 * m_dimension[3] + 100 * m_dimension[4]) / 5
        if 0 <= m_score < 34:
            m_color = '#bc3f2b'
        elif 34 <= m_score < 67:
            m_color = '#6586a1'
        else:
            m_color = '#95c5ab'

        n_score = self.count_risk_news_score()
        if 60 <= n_score < 70:
            n_color = '#bc3f2b'
        elif 70 <= n_score < 90:
            n_color = '#6586a1'
        else:
            n_color = '#95c5ab'

        i_score = ''
        i_color = ''
        return (
            (c_dimension, c_score, c_color),
            (s_dimension, s_score, s_color),
            (m_dimension, m_score, m_color),
            (n_dimension, n_score, n_color),
            (i_dimension, i_score, i_color)
        )

    def get_all(self):
        data = {
            'risk_rank': self.get_risk_rank(),
            'indicators': self.get_dimension(),
            'trend': self.trend_chart()
        }
        return data

    def get_industries(self):
        industries = []

        cond = {
            'user__id': self.user_id,
            'industry__name': self.name,
            'industry__level': self.level,
            'industry__parent__id': self.parent
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        user_industries = UserIndustry.objects.filter(**args)

        for u in user_industries:
            queryset = ScoreIndustry.objects.filter(
                pubtime__gte=self.start,
                pubtime__lt=self.end,
                industry=u.industry.id
            )

            score = queryset.aggregate(Avg('score'))[
                'score__avg'] if queryset else 100

            industries.append(
                (u.industry.id, u.name, u.industry.level, round(score)))

        return sorted(industries, key=lambda industry: industry[2])
