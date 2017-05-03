# -*- coding: utf-8 -*-
import os

from django.contrib import admin

from observer.apps.corpus.models import Corpus
from observer.utils.crawler.api import CrawlerTask
from django_extensions.admin import ForeignKeyAutocompleteAdmin

class CorpusAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'industry': ('name',)}
    list_display = ('industry', 'riskword', 'invalidword')
    list_filter = ('industry', 'riskword', 'invalidword')
    search_fields = ('industry__name', 'riskword', 'invalidword')
    readonly_fields = ['uuid']
    actions = ['delete_selected']

    def __init__(self, *args, **kwargs):
        super(CorpusAdmin, self).__init__(*args, **kwargs)
        self.stype = os.path.basename(os.path.dirname(__file__))

    def save_model(self, request, obj, form, change):
        riskwords = list(set(obj.riskword.split()))
        invalidwords = []
        if not change:
            CrawlerTask(obj.uuid, obj.industry.name, riskwords,
                invalidwords).build()
        else:
            corpus = Corpus.objects.get(id=obj.id)
            CrawlerTask(obj.uuid, obj.industry.name, riskwords,
                invalidwords).update(corpus)
        obj.riskword = " ".join(riskwords)
        obj.invalidword = " ".join(invalidwords)
        obj.save()

    def delete_model(self, request, obj):
        CrawlerTask(obj.uuid, obj.industry.name, list(set(obj.riskword.split())),
            list(set(obj.invalidword.split()))).remove(obj)
        obj.delete()

    def delete_selected(self, request, objs):
        for obj in objs:
            CrawlerTask(obj.uuid, obj.industry.name, list(set(obj.riskword.split())),
                list(set(obj.invalidword.split()))).remove(obj)
            obj.delete()


admin.site.register(Corpus, CorpusAdmin)
