# -*- coding: utf-8 -*-
from datetime import timedelta

from django.db.models import Case, IntegerField, Sum, When

from observer.apps.riskmonitor.models import RiskNews
from observer.apps.riskmonitor.service.abstract import Abstract
from observer.utils.date.tz import utc_to_local_time


class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_news_list(self):
        fields = ('id', 'title', 'pubtime', 'publisher__publisher')

        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': self.industry,
            'enterprise__id': self.enterprise,
            'publisher__id': self.source
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def cal_date_range(self, x_axis_units):
        if x_axis_units == 'day':
            cal_date_func = lambda x: (
                self.start + timedelta(days=x),
                self.start + timedelta(days=x + 1)
            )

            date_range = map(cal_date_func, xrange(self.days))

        elif x_axis_units == 'month':
            cal_date_func = lambda month: (year, month)

            if self.end.year == self.start.year:
                year = self.end.year
                iterable = xrange(self.start.month + 1, self.end.month + 1)

                date_range = map(cal_date_func, iterable)

            elif self.end.year - self.start.year == 1:
                year = self.start.year
                iterable = xrange(self.start.month + 1, 13)
                date_range_one = map(cal_date_func, iterable)

                year = self.end.year
                iterable = xrange(1, self.end.month + 1)
                date_range_two = map(cal_date_func, iterable)

                date_range = date_range_one + date_range_two

            else:
                years = self.end.year - self.start.year

                year = self.start.year
                iterable = xrange(self.start.month + 1, 13)
                date_range_one = map(cal_date_func, iterable)

                year = self.end.year
                iterable = xrange(1, self.end.month + 1)
                date_range_two = map(cal_date_func, iterable)

                date_range = date_range_one + date_range_two

                for y in xrange(1, years):
                    year = self.start.year + y
                    iterable = xrange(1, 13)
                    date_range += map(cal_date_func, iterable)

        result = self.cal_news_nums(date_range, x_axis_units)

        return {
            'date': result[0],
            'data': result[1]
        }

    def cal_news_nums(self, date_range, x_axis_units):
        cond = {
            'pubtime__gte': self.start,
            'pubtime__lt': self.end,
            'industry__id': self.industry,
            'enterprise__id': self.enterprise,
            'publisher__id': self.source
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        if x_axis_units == 'day':
            # Generate $aggregate_args by date_range
            aggregate_args = dict([(
                start.strftime('%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(When(pubtime__gte=start, pubtime__lt=end, then=1),
                         output_field=IntegerField(), default=0)
                )
            ) for start, end in date_range])

        elif x_axis_units == 'month':
            # Generate $aggregate_args by months
            aggregate_args = dict([(
                '%s-%s-01 00:00:00' % (year, month),  # Type must be <Str>
                Sum(
                    Case(When(pubtime__year=year, pubtime__month=month, then=1),
                         output_field=IntegerField(), default=0)
                )
            ) for year, month in date_range])

        queryset = RiskNews.objects.filter(**args).aggregate(**aggregate_args)

        # Convert $queryset
        # key:      str     ->  local datetime
        # value:    None    ->  0
        result = [(
            utc_to_local_time(k),
            v if v is not None else 0
        ) for k, v in queryset.iteritems()]

        # sorted by $queryset key
        return zip(*sorted(result, key=lambda data: data[0]))
