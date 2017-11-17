
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.base.models import Article, Area, Inspection
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class DashboardQuerySet(Abstract):

    def __init__(self, params={}):
        super(DashboardQuerySet, self).__init__(params)


    fields = ('id', 'title', 'source', 'url', 'pubtime')
  
    args = {}

    def zjnews(self):
        self.args['category__name']='质监热点'
        return Article.objects.filter(**self.args).values(*self.fields).order_by('-pubtime')[:10]
        # return Article.objects.filter(**self.args).title.order_by('-pubtime')[:10]

    def zlnews(self):
        self.args['category__name']='质量事件'
        return Article.objects.filter(**self.args).values(*self.fields).order_by('-pubtime')[:10]

    def risknews(self):
        self.args['category__name']='风险新闻'
        return Article.objects.filter(**self.args).values(*self.fields).order_by('-pubtime')[:10]

    def get_all_news_list(self):
        data = {
            'zjnews': self.zjnews(),
            'zlnews': self.zlnews(),
            'risknews': self.risknews()
        }

        return data


        

    


        
