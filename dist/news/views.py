# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base import set_logo
from base.views import BaseTemplateView
from base.models import Area, Article, Category, RelatedData, Topic


class NewsView(BaseTemplateView):
    def get(self, request):
        return self.render_to_response('news/news_list.html', {})


class NewsDetailView(BaseTemplateView):
    def get(self, request, news_id):
        try:
            news_id = int(news_id)
            news = Article.objects.get(id=news_id)
        except Article.DoesNotExist:
            return self.render_to_response('news/news.html', {'article': '', 'relate': []})

        try:
            r = RelatedData.objects.filter(uuid=news.uuid)[0]
            relateddata = list(r.articles.all())
        except IndexError:
            relateddata = []
        try:
            event = Topic.objects.filter(articles__id=news_id)[0]
        except IndexError:
            event = ''
        user = self.request.myuser
        try:
            collection = user.collection
        except Collection.DoesNotExist:
            collection = Collection(user=user)
            collection.save(using='master')
        items = user.collection.articles.all()
        iscollected = any(filter(lambda x: x.id == news.id, items))
        return self.render_to_response('news/news.html', {'article': set_logo(news), 'relate': relateddata, 'event': event, 'isCollected': iscollected})


class CategoryView(BaseTemplateView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = ''
        return self.render_to_response('category/category.html', {'category': category})


class LocationView(BaseTemplateView):
    def get(self, request, location_id):
        """
        try:
            location = Area.objects.get(id=int(location_id))
        except Area.DoesNotExist:
            location = ''
        weixin = [set_logo(data) for data in Weixin.objects.filter(area=location)][:10]
        weibo = [set_logo(data) for data in Weibo.objects.filter(area=location)][:10]
        return self.render_to_response("location/location.html", {'location': location, 'weixin_list': weixin, 'weibo_list': weibo})
        """
        try:
            location = Area.objects.get(id=int(location_id))
        except Area.DoesNotExist:
            location = ''
        return self.render_to_response("location/location.html", {'location': location})
