
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import Http404

from observer.apps.seer.models import AreaIndustry
from observer.apps.base.models import Industry


class Abstract(object):

    def __init__(self, params):
        for k, v in params.items():
            setattr(self, k, v)

    def set_args(self):
        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': getattr(self, 'industry', None),
            'enterprise__id': getattr(self, 'enterprise', None)
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        return args

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


def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=1)
    for season, (start, end) in seasons:
        if start <= now <= end:
            return season
    assert 0, 'never happens'
