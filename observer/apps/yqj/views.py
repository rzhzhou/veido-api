from datetime import date, datetime, timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.utils.date.convert import utc_to_local_time

from observer.apps.yqj.models import (Article, )
from observer.apps.base.models import (Area, Article, )

from observer.apps.yqj.service.articles import ArticlesQuerySet


class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {
            'starttime': self.today - timedelta(days=30),
            'endtime': self.today,
        }

    def set_params(self, params):
        for k, v in params.items():
            self.query_params[k] = v
        # self.start=self.query_params.get('start')

        # start, end convert to local datetime
        self.query_params['starttime'], self.query_params['endtime'] = utc_to_local_time(
            [self.query_params['starttime'], self.query_params['endtime']]
        )

        # end add 1 day
        self.query_params['endtime'] = self.query_params['endtime'] + timedelta(days=1)

    def paging(self, queryset, page, num):
        paginator = Paginator(queryset, num)  # Show $num <QuerySet> per page

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            results = paginator.page(paginator.num_pages)

        return results


class ArticleView(BaseView):

    def __init__(self):
        super(ArticleView, self).__init__()

    def set_params(self, request):
        super(ArticleView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params.get('start')) /
                int(self.query_params.get('length'))) + 1

        return super(ArticleView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data = map(lambda r: {
            'url': r['url'],
            'title': r['title'],
            'source': r['source'],
            'area': Area.objects.get(id=r['area']).name,
            'pubtime': utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d'),
            'reprinted': r['reprinted'],
        }, results)

        return data

    def get(self, request):
        self.set_params(request)
        queryset = ArticlesQuerySet(params=self.query_params).get_all_article_list()

        return Response(self.serialize(queryset))
