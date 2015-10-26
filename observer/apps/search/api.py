# -*- coding: utf-8 -*-
import pysolr

from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from observer.apps.base.models import Collection, Article, Topic
from observer.apps.collection.api import CollectView


class SearchView(CollectView):
    def get(self, request, keyword, *args, **kwargs):
        solr = pysolr.Solr('http://192.168.1.182:8983/solr/', timeout=10)
        results = solr.search(keyword)
        return JsonResponse({"news": list(results), "event": {}})
