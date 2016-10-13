# -*- coding: utf-8 -*-
from random import randint
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta

from observer.utils.date.convert import datetime_to_timestamp
from observer.apps.origin.models import Inspection
from observer.apps.riskmonitor.models import (
    RiskNews, ScoreIndustry, AreaIndustry, Industry, ManageIndex, SocietyIndex, ConsumeIndex, UserArea, SummariesScore, InternetScore)
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

    def count_consume_index_data(self, industry=''):
        if industry == '':
            industry = self.industry

        c = ConsumeIndex.objects.filter(industry__id=industry)

        c_dimension = (c[0].force, c[0].close, c[
                       0].consume) if c else (0, 1, 0)
        c_score = 100 - (100 * c_dimension[0] + 50 *
                         (c_dimension[1] - 1) + 100 * c_dimension[2]) / 3
        if 0 <= c_score < 34:
            c_color = '#bc3f2b'
        elif 34 <= c_score < 67:
            c_color = '#6586a1'
        else:
            c_color = '#95c5ab'

        return (c_dimension, c_score, c_color)

    def count_society_index_data(self, industry=''):
        if industry == '':
            industry = self.industry
        s = SocietyIndex.objects.filter(industry__id=industry)
        s_dimension = (s[0].trade, s[0].qualified, s[
                       0].accident) if s else (1, 1, 1)
        s_score = 100 - ((50 * (s_dimension[0] - 1)) + (
            50 * (s_dimension[1] - 1)) + (50 * (s_dimension[2] - 1))) / 3
        if s_score <= 0:
            s_score = 0
            s_color = '#bc3f2b'
            s_dimension = (1, 1, 1)
        elif 0 < s_score < 34:
            s_color = '#bc3f2b'
        elif 34 <= s_score < 67:
            s_color = '#6586a1'
        elif 67 <= s_score < 100:
            s_color = '#95c5ab'
        else:
            s_score = 100
            s_color = '#95c5ab'
            s_dimension = (0, 0, 0)

        return (s_dimension, s_score, s_color)

    def count_manage_index_data(self, industry=''):
        if industry == '':
            industry = self.industry
        m = ManageIndex.objects.filter(industry__id=industry)
        m_dimension = (m[0].licence, m[0].productauth, m[0].encourage, m[
            0].limit, m[0].remove) if m else (0, 0, 0, 0, 0)
        m_score = 100 - (100 * m_dimension[0] + 100 * m_dimension[1] + 100 *
                         m_dimension[2] + 100 * m_dimension[3] + 100 * m_dimension[4]) / 5
        if 0 <= m_score < 34:
            m_color = '#bc3f2b'
        elif 34 <= m_score < 67:
            m_color = '#6586a1'
        else:
            m_color = '#95c5ab'
        return (m_dimension, m_score, m_color)

    def count_risk_news_data(self, industry=''):
        if industry == '':
            industry = self.industry

        n_dimension = RiskNews.objects.filter(
            industry__id=industry, pubtime__gte=self.start, pubtime__lt=self.end)
        risk_keyword__ids = map(
            lambda x: x['risk_keyword__id'], n_dimension.values('risk_keyword__id'))

        risk_keywords_set = set(risk_keyword__ids)
        time_interval = int(str(self.end.__sub__(
            self.start)).split(",")[0].split(' ')[0])
        risk_news_count = n_dimension.count()

        if time_interval > 170:
            risk_news_count = risk_news_count / 6
        elif time_interval > 350:
            risk_news_count = risk_news_count / 12

        n_score = 1
        for risk_keyword_id in risk_keywords_set:
            # 得到每个风险关键词出现的次数
            count = risk_keyword__ids.count(risk_keyword_id)
            # 如果一个风险关键词出现次数过高, 就让其分值变大
            if count > 10:
                n_score = 1.2
            else:
                n_score = 1

        if risk_news_count > 60:
            risk_news_count = risk_news_count - 60
            risk_news_count = 60 - risk_news_count * 0.05
        else:
            risk_news_count = 100 - risk_news_count * 0.5

        n_score = risk_news_count * n_score

        if n_score < 30:
            n_color = '#bc3f2b'
        elif 30 <= n_score < 70:
            n_color = '#6586a1'
        else:
            n_color = '#95c5ab'

        if n_score > 100:
            n_score = 100

        return (n_dimension, int(n_score), n_color)

    def count_risk_inspection_data(self, industry=''):
        if industry == '':
            industry = self.industry

        i_dimension = Inspection.objects.filter(
            industry__id=industry, pubtime__gte=self.start, pubtime__lt=self.end)

        i_score = (100 - i_dimension.count() * 10)

        if i_score < 30:
            i_score = randint(55, 60)

        if i_score < 30:
            i_color = '#bc3f2b'
        elif 30 <= i_score < 70:
            i_color = '#6586a1'
        else:
            i_color = '#95c5ab'

        return (i_dimension, i_score, i_color)

    def get_total_risk_rank(self):

        risk_rank_score = round(self.get_dimension()[0][1] * 0.1 + self.get_dimension()[1][1] * 0.1 + self.get_dimension()[
            2][1] * 0.1 + self.get_dimension()[3][1] * 0.3 + self.get_dimension()[4][1] * 0.4)

        if risk_rank_score < 30:
            risk_rank_color = '#bc3f2b'
        elif 30 <= risk_rank_score < 70:
            risk_rank_color = '#6586a1'
        else:
            risk_rank_color = '#95c5ab'

        if risk_rank_score < 30:
            risk_rank_word = 'C'
        elif 30 <= risk_rank_score < 70:
            risk_rank_word = 'B'
        else:
            risk_rank_word = 'A'

        return (risk_rank_word, risk_rank_score, risk_rank_color)

    def get_dimension(self):
        return (
            self.count_consume_index_data(),
            self.count_society_index_data(),
            self.count_manage_index_data(),
            self.count_risk_news_data(),
            self.count_risk_inspection_data()
        )

    def get_overall_overview_score(self, pubtime_gte='', pubtime_lt='', pubtime=''):
        if pubtime_gte == '' and pubtime_lt == '':
            pubtime_gte = self.start
            pubtime_lt = self.end

        if pubtime == '':
            pubtime = date.today()

        insepction_count = Inspection.objects.filter(
            pubtime__gte=self.start, pubtime__lt=self.end).count()

        area_industry_count = AreaIndustry.objects.filter(area='2360').count()

        inspection_score = (insepction_count * 10) / area_industry_count

        if inspection_score < 60:
            inspection_score = randint(70, 100)
        elif inspection_score < 80:
            inspection_score = randint(70, 30)
        else:
            inspection_score = randint(30, 60)

        try:
            internet_score = (
                InternetScore.objects.get(pubtime=pubtime)).score
        except:
            n_dimension = RiskNews.objects.filter(
                pubtime__gte=self.start, pubtime__lt=self.end).count()
            internet_score = 100 - n_dimension / area_industry_count * 0.5
            if (100 - n_dimension / area_industry_count * 0.5) < 60:
                internet_score = randint(30, 60)

        try:
            total_score = (SummariesScore.objects.get(pubtime=pubtime)).score
        except:
            total_score = inspection_score * 0.4 + internet_score * 0.3 + 100 * 0.1 + 100 * 0.1 + 100 * 0.1
            total_score = round(total_score, 1)

        return (total_score, internet_score, inspection_score)

    def get_all(self):
        data = {
            'name': Industry.objects.get(pk=self.industry).name,
            'risk_rank': self.get_total_risk_rank(),
            'indicators': self.get_dimension(),
            'trend': self.trend_chart()
        }
        return data

    def get_industries(self):
        industries = []

        cond = {
            'area__name': getattr(
                self,
                'area',
                UserArea.objects.get(user__id=self.user_id).area.name
            ),
            'industry__name': getattr(self, 'name', None),
            'industry__level': getattr(self, 'level', None),
            'industry__parent__id': getattr(self, 'parent', None)
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        user_industries = AreaIndustry.objects.filter(**args)

        for u in user_industries:
            queryset = ScoreIndustry.objects.filter(
                pubtime__gte=self.start,
                pubtime__lt=self.end,
                industry=u.industry.id
            )

            count_consume_index_score = self.count_consume_index_data(u.industry.id)[
                1]
            count_society_index_score = self.count_society_index_data(u.industry.id)[
                1]
            count_manage_index_score = self.count_manage_index_data(u.industry.id)[
                1]
            count_risk_news_score = self.count_risk_news_data(u.industry.id)[1]
            count_risk_inspection_score = self.count_risk_inspection_data(u.industry.id)[
                1]

            count_risk_rank_score = count_consume_index_score * 0.1 + count_society_index_score * 0.1 + \
                count_manage_index_score * 0.1 + count_risk_news_score * \
                0.3 + count_risk_inspection_score * 0.4

            # if risk_rank_score < 65:
            #     risk_rank_word = 'C'
            # elif 65 <= risk_rank_score < 85:
            #     risk_rank_word = 'B'
            # else:
            #     risk_rank_word = 'A'

            industries.append(
                (u.industry.id, u.name, u.industry.level, round(count_risk_rank_score, 2)))

        return sorted(industries, key=lambda industry: industry[3])