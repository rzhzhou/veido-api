# -*- coding: utf-8 -*-
from django.db.models import Case, IntegerField, Sum, When

from observer.apps.riskmonitor.service.abstract import Abstract
from observer.apps.riskmonitor.models import RiskNews
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

    def cal_news_nums(self, date_range):
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

        # Convert $queryset
        # key:      str     ->  local datetime
        # value:    None    ->  0
        result = [(
            utc_to_local_time(k),
            v if v is not None else 0
        ) for k, v in queryset.iteritems()]

        # sorted by $queryset key
        return zip(*sorted(result, key=lambda data: data[0]))
