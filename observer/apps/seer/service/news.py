
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.seer.models import IndustryScore
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class NewsQuerySet(Abstract):

    def __init__(self, params={}):
        super(NewsQuerySet, self).__init__(params)

    def get_news_list(self):
        cond = {
            'id__lte': RiskNews.objects.aggregate(Max('id')).get('id__max'),
            'status': getattr(self, 'status', 1),
            'title__contains': getattr(self, 'search[value]', None), 
            'publisher__id': getattr(self, 'publisher_id', None),
            'industry__id': getattr(self, 'industry_id', None )
        }

        fields = ('id', 'title', 'pubtime', 'url', 'risk_keyword', 'invalid_keyword', 'publisher__name', 'industry__name')
        
        args = dict([(k, v) for k, v in cond.iteritems() if v ])

        return RiskNews.objects.filter(**args).values(*fields)

    def get_all_news_list(self):
        fields = ('id', 'title', 'pubtime', 'url')

        args = {
            'id__lte': RiskNews.objects.aggregate(Max('id')).get('id__max'),
            'status': 1,
            'title_contains': getattr(self, 'keywords', None)
        }

        return RiskNews.objects.filter(**args).values(*fields)

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


class NewsUpdate(Abstract):

    def __init__(self, params={}):
        super(NewsUpdate, self).__init__(params)

    def update_news(self):
        risk_news_ids = getattr(self, 'risk_news_ids', None)
        new_status = getattr(self, 'new_status', None)

        return 0 if not risk_news_ids and not new_status else RiskNews.objects.filter(id__in=risk_news_ids.split(',')).update(status=new_status)
