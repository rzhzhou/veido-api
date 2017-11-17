
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.base.models import Article
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time
from datetime import datetime, timedelta, date
import time

class AnalyticsViewQuerySet(Abstract):

    def __init__(self, params={}):
        super(AnalyticsViewQuerySet, self).__init__(params)
        cond={"pubtime__gte" : getattr(self,'starttime', None),"pubtime__lt" : getattr(self,'endtime',None)}
        self.start = cond['pubtime__gte']
        self.end = cond['pubtime__lt']
        self.days = (self.end - self.start).days
        self.date = [self.start + timedelta(days= i) for i in xrange(self.days)]


    def get_timelist(self):
        datelist = map(lambda x: x.strftime("%m-%d"), self.date)
        return datelist

    def get_news_count(self):
        list1=[]
        for i in self.date:
            article_count = Article.objects.filter(Q(pubtime__gte =i) & Q(pubtime__lt = i+timedelta(days =1))).count()
            list1.append(article_count)
        return list1


    def get_all_news_list(self):
        data ={
            'datetime':self.get_timelist(),
            'news_count': self.get_news_count(),
        }
        return data




