# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.origin.models import IndustryScore
from observer.apps.seer.models import RiskNews
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_news_list(self, search_value, industry=None, publisher=None):
        fields = ('id', 'title', 'pubtime', 'url', 'risk_keyword', 'invalid_keyword', 'publisher__name', 'industry__name')

        max_id = RiskNews.objects.all().aggregate(Max('id'))

        args = {
            'id__lte': max_id.get('id__max'),
            'status': False,
        }

        if search_value:
            args['title__contains'] = search_value
            
        if publisher != "null" and publisher is not None:
            args['publisher__id'] = publisher

        if industry != "null" and industry is not None:
            args['industry'] = industry

        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def get_all_news_list(self, search_value):
        fields = ('id', 'title', 'pubtime', 'url')

        max_id = RiskNews.objects.all().aggregate(Max('id'))

        args = {
            'id__lte': max_id.get('id__max'),
            'status': False,
        }

        if search_value:
            args['title__contains'] = search_value
            
        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def cal_date_range(self, x_axis_units, days):
        if x_axis_units == 'day':
            cal_date_func = lambda x: (
                self.start + timedelta(days=x),
                self.start + timedelta(days=x + 1)
            )

            date_range = map(cal_date_func, xrange(days))

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
            'categories': result[0],
            'data': result[1]
        }

    def cal_news_nums(self, date_range, x_axis_units):
        args = self.set_args()

        if x_axis_units == 'day':
            # Generate $aggregate_args by date_range
            aggregate_args = dict([(
                start.strftime('%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(pubtime__gte=start, pubtime__lt=end, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for start, end in date_range])

        elif x_axis_units == 'month':
            # Generate $aggregate_args by months
            aggregate_args = dict([(
                datetime(year, month, 1).strftime(
                    '%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(pubtime__year=year, pubtime__month=month, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for year, month in date_range])

        queryset = RiskNews.objects.filter(**args).aggregate(**aggregate_args)

        if queryset:
            # Convert $queryset
            # key:      str     ->  local datetime
            # value:    None    ->  0
            result = [(
                utc_to_local_time(k),
                v if v is not None else 0
            ) for k, v in queryset.iteritems()]

            # sorted by $queryset key
            return zip(*sorted(result, key=lambda data: data[0]))

        return [[], []]


    def cal_date_range_two(self, x_axis_units, days):
        if x_axis_units == 'day':
            cal_date_func = lambda x: (
                self.start + timedelta(days=x),
                self.start + timedelta(days=x + 1)
            )

            date_range = map(cal_date_func, xrange(days))

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

        result = self.cal_score_nums(date_range, x_axis_units)

        return {
            'categories': result[0],
            'data': result[1]
        }

    def cal_score_nums(self, date_range, x_axis_units):
     
        cond = {
            'time__gte': self.start,
            'time__lt': self.end,
            'industry__id': getattr(self, 'industry', None),
        }

        # Exclude $cond None Value
        args = dict([(k, v) for k, v in cond.iteritems() if v is not None])

        if x_axis_units == 'day':
            # Generate $aggregate_args by date_range
            aggregate_args = dict([(
                start.strftime('%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(time__gte=start, time__lt=end, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for start, end in date_range])

        elif x_axis_units == 'month':
            # Generate $aggregate_args by months
            aggregate_args = dict([(
                datetime(year, month, 1).strftime(
                    '%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(time__year=year, time__month=month, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for year, month in date_range])

        queryset = IndustryScore.objects.filter(**args).values('score', 'time')
        if queryset:
            result = []
            for q in queryset:
                result.append((utc_to_local_time(q.get('time')), q.get('score'),))

            return zip(*sorted(result, key=lambda data: data[0]))

        return [[], []]



class NewsRecycleQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsRecycleQuerySet, self).__init__(params)

    def get_news_list(self, search_value, industry=None, publisher=None):
        fields = ('id', 'title', 'pubtime', 'url', 'risk_keyword', 'invalid_keyword', 'publisher__name', 'industry__name')

        max_id = RiskNews.objects.all().aggregate(Max('id'))

        args = {
            'id__lte': max_id.get('id__max'),
            'status': True,
        }
        
        if search_value:
            args['title__contains'] = search_value
            
        if publisher != "null" and publisher is not None:
            args['publisher__id'] = publisher

        if industry != "null" and industry is not None:
            args['industry'] = industry

        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def get_all_news_list(self, search_value):
        fields = ('id', 'title', 'pubtime', 'url')

        max_id = RiskNews.objects.all().aggregate(Max('id'))

        args = {
            'id__lte': max_id.get('id__max'),
            'status': True,
        }

        if search_value:
            args['title__contains'] = search_value
            
        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def cal_date_range(self, x_axis_units, days):
        if x_axis_units == 'day':
            cal_date_func = lambda x: (
                self.start + timedelta(days=x),
                self.start + timedelta(days=x + 1)
            )

            date_range = map(cal_date_func, xrange(days))

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
            'categories': result[0],
            'data': result[1]
        }

    def cal_news_nums(self, date_range, x_axis_units):
        args = self.set_args()

        if x_axis_units == 'day':
            # Generate $aggregate_args by date_range
            aggregate_args = dict([(
                start.strftime('%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(pubtime__gte=start, pubtime__lt=end, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for start, end in date_range])

        elif x_axis_units == 'month':
            # Generate $aggregate_args by months
            aggregate_args = dict([(
                datetime(year, month, 1).strftime(
                    '%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(pubtime__year=year, pubtime__month=month, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for year, month in date_range])

        queryset = RiskNews.objects.filter(**args).aggregate(**aggregate_args)

        if queryset:
            # Convert $queryset
            # key:      str     ->  local datetime
            # value:    None    ->  0
            result = [(
                utc_to_local_time(k),
                v if v is not None else 0
            ) for k, v in queryset.iteritems()]

            # sorted by $queryset key
            return zip(*sorted(result, key=lambda data: data[0]))

        return [[], []]



class NewsValidQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsValidQuerySet, self).__init__(params)

    def get_news_list(self, search_value, industry=None, publisher=None):
        fields = ('id', 'title', 'pubtime', 'url', 'risk_keyword', 'invalid_keyword', 'publisher__name', 'industry__name')

        max_id = RiskNews.objects.all().aggregate(Max('id'))

        args = {
            'id__lte': max_id.get('id__max'),
            'status': 2,
        }
        
        if search_value:
            args['title__contains'] = search_value
            
        if publisher != "null" and publisher is not None:
            args['publisher__id'] = publisher

        if industry != "null" and industry is not None:
            args['industry'] = industry

        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def get_all_news_list(self, search_value):
        fields = ('id', 'title', 'pubtime', 'url')

        max_id = RiskNews.objects.all().aggregate(Max('id'))

        args = {
            'id__lte': max_id.get('id__max'),
            'status': 2,
        }

        if search_value:
            args['title__contains'] = search_value
            
        queryset = RiskNews.objects.filter(**args).values(*fields)

        return queryset

    def cal_date_range(self, x_axis_units, days):
        if x_axis_units == 'day':
            cal_date_func = lambda x: (
                self.start + timedelta(days=x),
                self.start + timedelta(days=x + 1)
            )

            date_range = map(cal_date_func, xrange(days))

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
            'categories': result[0],
            'data': result[1]
        }

    def cal_news_nums(self, date_range, x_axis_units):
        args = self.set_args()

        if x_axis_units == 'day':
            # Generate $aggregate_args by date_range
            aggregate_args = dict([(
                start.strftime('%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(pubtime__gte=start, pubtime__lt=end, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for start, end in date_range])

        elif x_axis_units == 'month':
            # Generate $aggregate_args by months
            aggregate_args = dict([(
                datetime(year, month, 1).strftime(
                    '%Y-%m-%d %H:%M:%S'),  # Type must be <Str>
                Sum(
                    Case(
                        When(pubtime__year=year, pubtime__month=month, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ) for year, month in date_range])

        queryset = RiskNews.objects.filter(**args).aggregate(**aggregate_args)

        if queryset:
            # Convert $queryset
            # key:      str     ->  local datetime
            # value:    None    ->  0
            result = [(
                utc_to_local_time(k),
                v if v is not None else 0
            ) for k, v in queryset.iteritems()]

            # sorted by $queryset key
            return zip(*sorted(result, key=lambda data: data[0]))

        return [[], []]
