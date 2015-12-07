# -*- coding: utf-8 -*-
import os

from django.contrib import admin

from observer.apps.corpus.models import Corpus
from observer.utils.crawler.api import CrawlerTask


class CorpusAdmin(admin.ModelAdmin):
    list_display = ('industry', 'riskword')
    list_editable = ('industry', 'riskword')
    list_filter = ('industry', 'riskword')
    search_fields = ('industry', 'riskword')

    def __init__(self, *args, **kwargs):
        super(CorpusAdmin, self).__init__(*args, **kwargs)
        self.stype = os.path.basename(os.path.dirname(__file__))

    def save_model(self, request, obj, form, change):
        if not change:
            CrawlerTask(obj.uuid, obj.industry.name, 
                obj.riskword.name, 'riskmonitor', self.stype).build()
        else:
            CrawlerTask(obj.uuid, obj.industry.name, 
                obj.riskword.name, 'riskmonitor', self.stype).update(obj.uuid)

        obj.save()

    def delete_model(self, request, obj):
        CrawlerTask(obj.uuid, obj.industry.name, 
                obj.riskword.name, 'riskmonitor', self.stype).remove(obj.uuid)
        obj.delete()


admin.site.register(Corpus, CorpusAdmin)
