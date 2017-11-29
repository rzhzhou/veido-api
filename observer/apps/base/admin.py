import os
import uuid
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter
from observer.apps.base.models import (Area, Corpus, Enterprise, Industry,
                                       Inspection, Article, ArticleCategory,
                                       AdministrativePenalties)
from observer.apps.seer.models import IndustryScore
from observer.apps.base.resource import (
    InspectionResources, EnterpriseResources, AdministrativePenaltiesResources)


class AreaAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'parent': ('name',)}
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent__name')
    list_filter = ('level', )


class IndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'parent': ('name',)}
    fields = ('name', 'code', 'level', 'parent')
    list_display = ('name', 'code', 'level', 'parent')
    search_fields = ('name', 'level', 'parent__name')
    list_filter = ('level', )
    readonly_fields = ('code', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['code']
        else:
            return []


class EnterpriseAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    resource_class = EnterpriseResources
    fields = ('name', 'area')
    list_display = ('name', 'area')
    search_fields = ('name', 'area__name')
    list_filter = ('area', )


class InspectionAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionResources
    search_fields = ('title', 'publisher__name',)
    list_display = ('title', 'pubtime',)
    list_filter = (('pubtime', DateRangeFilter),)


class AdministrativePenaltiesAdmin(ImportExportActionModelAdmin):
    resource_class = AdministrativePenaltiesResources
    # related_search_fields = {'area': ('name',)}
    search_fields = ('title', 'publisher')
    list_display = ('title',  'pubtime', 'publisher',)
    list_filter = (('pubtime', DateRangeFilter), 'industry')


class CorpusAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'industry': ('name',)}
    list_display = ('industry', 'riskword', 'invalidword')
    list_filter = ('industry', 'riskword', 'invalidword')
    search_fields = ('industry__name', 'riskword', 'invalidword')
    # readonly_fields = ['uuid']
    actions = ['delete_selected']

    def __init__(self, *args, **kwargs):
        super(CorpusAdmin, self).__init__(*args, **kwargs)
        self.stype = os.path.basename(os.path.dirname(__file__))

    def save_model(self, request, obj, form, change):
        riskwords = list(set(obj.riskword.split()))
        invalidwords = list(set(obj.invalidword.split()))

        if not change:
            CrawlerTask(obj.uuid, obj.industry.name, riskwords, []).build()
        else:
            corpus = Corpus.objects.get(id=obj.id)
            CrawlerTask(obj.uuid, obj.industry.name,
                        riskwords, []).update(corpus)

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


admin.site.register(Area, AreaAdmin)
admin.site.register(Corpus, CorpusAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(AdministrativePenalties, AdministrativePenaltiesAdmin)
admin.site.register(Article)
admin.site.register(ArticleCategory)
