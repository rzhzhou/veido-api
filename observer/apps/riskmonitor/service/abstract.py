# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Case, Count, IntegerField, Q, Sum, When
from django.http import Http404

from observer.apps.base.api_function import get_season
from observer.apps.base.views import BaseView
from observer.apps.riskmonitor.models import (Enterprise, Industry, Product,
                                              RiskNews, RiskNewsPublisher,
                                              ScoreEnterprise, ScoreIndustry,
                                              UserIndustry)
from observer.utils.connector.mysql import query
from observer.utils.date.tz import utc_to_local_time


class Abstract(object):

    def __init__(self, params):
        for k, v in params.iteritems():
            setattr(self, k, v)

    def indu_make_level(self, score):
        level = 'A'
        if score <= 100 and score >= 90:
            level = 'C'
        if score < 90 and score >= 80:
            level = 'B'
        if score < 80:
            level = 'A'
        return level

    def ente_make_level(self, score):
        level = 'A'
        if score <= 100 and score >= 90:
            level = 'C'
        if score < 90 and score >= 80:
            level = 'B'
        if score < 80:
            level = 'A'
        return level

    def entegenerate(self, entescores):
        for entescore in entescores:
            score = entescore.score
            level = self.ente_make_level(score)
            yield entescore.enterprise, level

    def risk_industry(self):
        industries = []

        user_industries = UserIndustry.objects.filter(user__id=self.user_id)

        for u in user_industries:
            queryset = ScoreIndustry.objects.filter(
                pubtime__gte=self.start,
                pubtime__lt=self.end,
                industry=u.industry.id
            ).order_by('-score')

            score = queryset.aggregate(Avg('score')) if queryset else 100

            industries.append((u.industry.id, u.name, score['score__avg']))

        return sorted(industries, key=lambda industry: industry[2])

    def risk_enterprise(self, start, end, type):
        entescore = ScoreEnterprise.objects.filter(
            pubtime__range=(start, end)).order_by('-score')
        enteobject = self.entegenerate(entescore)
        count = 3 if type is 'abstract' else Enterprise.objects.all().count()
        try:
            enteobjects = [enteobject.next() for i in xrange(count)]
        except:
            enteobjects = []
        return enteobjects

    def news_nums(self, date_range):
        try:
            self.industry = UserIndustry.objects.get(
                id=self.industry).industry.id
        except UserIndustry.DoesNotExist:
            self.industry = None

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': self.industry,
            'enterprise__id': self.enterprise,
            'publisher__id': self.source
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        # Generate $aggregate_args by date_range
        aggregate_args = dict([(
            start.strftime('%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
            Sum(
                Case(When(pubtime__gte=start, pubtime__lt=end, then=1),
                     output_field=IntegerField(), default=0)
            )
        ) for start, end in date_range])

        queryset = RiskNews.objects.filter(**args).aggregate(**aggregate_args)

        # Convert $queryset None Value to Zero
        return dict(map(lambda x: (x[0], x[1] if x[1] is not None else 0), queryset.iteritems()))

    def compare(self, start, end, id):

        def count(start, end, id):
            try:
                industry = Industry.objects.get(
                    id=id) if id is not None else None
            except ObjectDoesNotExist:
                raise Http404("Industry does not exist")
            count = RiskNews.objects.filter(
                Q(pubtime__range=(start, end)) & Q(industry=industry
                                                   ) if industry is not None else Q()
            ).aggregate(reprinted=Count('reprinted'))
            return count['reprinted']

        def compare_with_the_statistics_last_year(start, end, id):
            timedelta_one_year = relativedelta(years=1)
            a_period_count = count(start, end, id)
            b_period_count = count(
                start - timedelta_one_year, end - timedelta_one_year, id)
            try:
                increase = (a_period_count - b_period_count) / b_period_count
            except:
                increase = 0
            return increase

        def compare_with_the_statistics_last_season(start, end, id):
            timedelta_one_season = relativedelta(months=3)
            a_period_count = count(start, end, id)
            b_period_count = count(
                start - timedelta_one_season, end - timedelta_one_season, id)
            try:
                increase = (a_period_count - b_period_count) / b_period_count
            except:
                increase = 0
            return increase

        def compare_with_the_statistics_last_month(start, end, id):
            timedelta_one_month = relativedelta(months=1)
            a_period_count = count(start, end, id)
            b_period_count = count(
                start - timedelta_one_month, end - timedelta_one_month, id)
            try:
                increase = (a_period_count - b_period_count) / b_period_count
            except:
                increase = 0
            return increase

        date_range = (end - start).days

        if date_range > 6 * 30:
            season = get_season(start)
            data = [[compare_with_the_statistics_last_year(start, end, id)],
                    [compare_with_the_statistics_last_season(start, end, id)]]
            return {
                'data': data,
                'date': season
            }
        # data range by month    less two axis has data
        else:
            month = start.month
            data = [[compare_with_the_statistics_last_year(start, end, id)],
                    [compare_with_the_statistics_last_month(start, end, id)]]
            return {
                'data': data,
                'date': month
            }

    def enterprise_rank(self):
        fields = ('enterprise__id', 'enterprise__name', 'score')

        try:
            self.industry = UserIndustry.objects.get(
                id=self.industry).industry.id
        except UserIndustry.DoesNotExist:
            self.industry = None

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': self.industry,
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = ScoreEnterprise.objects.filter(
            **args).order_by('score').values(*fields)

        return queryset

    def sources(self):
        """
        "source": {
            "labels": ["赢商网", "中国产业调研", "新浪", "华西都市网", "人民网"],
            "data": [
                {"value": "335", "name": "赢商网"},
                {"value": "310", "name": "中国产业调研"},
                {"value": "234", "name": "新浪"},
                {"value": "135", "name": "华西都市网"},
                {"value": "1548", "name": "人民网"}
            ]
        }
        """
        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': UserIndustry.objects.get(
                id=self.industry).industry.id if self.industry else None,
            'enterprise__id': self.enterprise,
            'publisher__id': self.source
        }
        args = {}
        for k, v in cond.iteritems():
            if v:
                args[k] = v

        queryset = RiskNews.objects.filter(**args).values(
            'publisher').annotate(num_publishers=Count('publisher')).order_by('-num_publishers')[:20]

        data = [{'value': q['num_publishers'], 'name': RiskNewsPublisher.objects.get(
            id=q['publisher']).publisher} for q in queryset]
        labels = [d['name'] for d in data]
        return {'labels': labels, 'data': data}
