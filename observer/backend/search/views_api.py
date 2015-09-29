# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings

from collection.views_api import CollectView
from base.models import Collection, Article, Topic


class SearchView(CollectView):
    def get(self, request, keyword, *args, **kwargs):
        try:
            self.collection = request.myuser.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save(using='master')
        news = []
        for data in self.search_article(keyword):
            news.append(self.article_html(data))
        event = []
        for data in self.search_event(keyword):
            event.append(self.topic_html(data))
        return JsonResponse({"news": news, "event": event})

    def search_article(self, key):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s') LIMIT %s" % (key, settings.LIMIT))

    def search_event(self, key):
        #return Topic.objects.raw(u"SELECT * FROM topic WHERE MATCH (abstract, title) AGAINST ('%s') LIMIT %s" % (key, self.LIMIT))
        return Topic.objects.raw(u"SELECT * FROM topic WHERE title like '%%{0}%%' LIMIT {1}".format(key, settings.LIMIT))