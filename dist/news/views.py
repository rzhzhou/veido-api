# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base.views import BaseTemplateView
from base.models import Article


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
        return self.render_to_response('news/news.html', {'article': SetLogo(news), 'relate': relateddata, 'event': event, 'isCollected': iscollected})
