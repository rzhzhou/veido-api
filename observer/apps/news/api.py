# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response

from observer.apps.base import read
from observer.apps.base.models import Area, Article, Category
from observer.apps.base.views import BaseAPIView, BaseView

class ArticleTableView(BaseAPIView):
    def get(self, request, id):
        container = self.requesthead()
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'total': 0, 'data': []})

        items = category.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, container['page'])
        result = self.news_to_json(datas['items'])
        news_html = render_to_string('news/list_tpl.html', {'news_list': result})
        return Response({'total': datas['total_number'], 'html': news_html})


class LocationTableView(BaseAPIView):
    def get(self, request, id):
        container = self.requesthead()
        try:
            id = int(id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'total': 0, 'data': []})

        items = Article.objects.filter(area=area)
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, container['page'])
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/list_tpl.html', {'news_list': result})
        return Response({'total': datas['total_number'], 'html': html_string})

@api_view(['GET'])
@read('news')
def news_view(request):
    HOME_PAGE_LIMIT = 10
    container = request.GET
    page = int(container['page']) if container.has_key('spage') else 1
    limit = 10
    if container['type'] == 'list':
        limit = settings.NEWS_PAGE_LIMIT

    items = Category.objects.get(name='质监热点').articles.all()
    datas = BaseView().paging(items, limit, page)
    result = BaseView().news_to_json(datas['items'])
    html_string = render_to_string('news/%s_tpl.html' % container['type'], {
        'news_list': result})
    return Response({'total': datas['total_number'], 'html': html_string})
