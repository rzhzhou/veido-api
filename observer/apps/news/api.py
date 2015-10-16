# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base.models import Area, Article, Category
from observer.apps.base.views import BaseAPIView


class ArticleTableView(BaseAPIView):
    def get(self, request, id):
        container = self.requestContainer()
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
        container = self.requestContainer()
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


class NewsView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def get_custom_artice(self):
        articles = Category.objects.get(name='质监热点').articles.all()
        return articles

    def get(self, request):
        container = self.requestContainer(
            limit=self.HOME_PAGE_LIMIT, limit_list=settings.NEWS_PAGE_LIMIT)
        items = self.get_custom_artice()
        datas = self.paging(items, container['limit'], container['page'])
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/%s_tpl.html' % container['type'], {
            'news_list': result})
        return Response({'total': datas['total_number'], 'html': html_string})
