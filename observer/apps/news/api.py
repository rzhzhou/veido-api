# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base.models import (
    Area, Article, Category, RelatedData, Topic, Collection, User)
from observer.apps.base.views import BaseAPIView, BaseView


class NewsDetailView(BaseAPIView):

    def get(self, request, news_id):
        try:
            news_id = int(news_id)
            news = Article.objects.filter(id=news_id)
            result = self.news_to_json(news)[0]
        except IndexError:
            return Response({
            'article': {},
            'relate': [],
            'events': [],
            'collected': 'false'})

        try:
            r = RelatedData.objects.filter(uuid=news[0].uuid)[0]
            data = r.articles.all()
            relateddatas = self.news_to_json(data)
        except IndexError:
            relateddata = []
        try:
            item = Topic.objects.filter(articles__id=news_id)[0]
            event = self.event_to_json(item)
        except IndexError:
            event = []
        user = request.user   
        try:
            yqj_user = User.objects.get(username=user.username)
            collection = yqj_user.collection
        except:
            collection = Collection(user=yqj_user)
            collection.save(using='master')
        items = yqj_user.collection.articles.all()
        iscollected = any(filter(lambda x: x.id == news[0].id, items))
        return Response({
            'article': result,
            'relate': relateddatas,
            'events': event,
            'collected': iscollected,
            })


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
        return Response({'total': datas['total_number'], 'data': result})


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
        return Response({'total': datas['total_number'], 'data': result})


class NewsView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def get_custom_artice(self):
        articles = Category.objects.get(name='质监热点').articles.all()
        return articles

    def get(self, request):
        container = self.requesthead(
            limit=self.HOME_PAGE_LIMIT, limit_list=settings.NEWS_PAGE_LIMIT)
        items = self.get_custom_artice()
        datas = self.paging(items, container['limit'], container['page'])
        print container['limit'], container['page']
        result = self.news_to_json(datas['items'])
        return Response({'list':{'pages': datas['total_number'], 'items': result}})


class NewsApi(BaseView):
    
    def get(self):
        items = Category.objects.get(name='质监热点').articles.all()[:10]
        result = self.news_to_json(items)
        new_data = self.get_info(title=u'质监热点', color='info', types='news', name='newsDetail', items=result)
        
        return new_data

