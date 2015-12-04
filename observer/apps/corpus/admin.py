# -*- coding: utf-8 -*-
from django.contrib import admin
from observer.apps.corpus.models import Corpus


class CorpusAdmin(admin.ModelAdmin):
    list_display = ('industry', 'riskword')
    list_editable = ('industry', 'riskword')
    list_filter = ('industry', 'riskword')
    search_fields = ('industry', 'riskword')

    def save_model(self, request, obj, form, change):
        if not change:
            CrawlerTask(obj.uuid, obj.riskword.name, 
            	obj.corpus.name, 'riskmonitor', u'关键词').build()
        else:
            CrawlerTask(obj.uuid, obj.riskword.name, 
            	obj.corpus.name, 'riskmonitor', u'关键词').update(obj.uuid)

        obj.save()

admin.site.register(Corpus, CorpusAdmin)
