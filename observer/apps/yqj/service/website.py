from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.base.models import Article
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time

class WebsiteQuerySet(Abstract):

    def __init__(self, params={}):
        super(WebsiteQuerySet, self).__init__(params)

    def get_all_news_list(self, starttime=None, endtime=None):
        fields = ('id', 'title', 'pubtime', 'source', 'url')

        cond={
            'pubtime__gte': getattr(self, 'starttime' ,None),
            'pubtime__lt': getattr(self, 'endtime', None),
            'title__contains': getattr(self, 'search[value]', None)
        }
        args = dict([k, v] for k, v in cond.iteritems() if v)

        queryset = Article.objects.filter(**args).values(*fields)
        return queryset
        