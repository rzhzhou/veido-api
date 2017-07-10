# -*- coding: utf-8 -*-
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from daterange_filter.filter import DateRangeFilter
from observer.apps.seer.resource import (
    ConsumeIndexResources, ManageIndexResources, SocietyIndexResources, RiskNewsResources)
from observer.apps.seer.models import (Enterprise, Industry,
                                              RiskNewsPublisher, RiskNews,
                                              UserArea, AreaIndustry,
                                              SocietyIndex, ConsumeIndex,
                                              ManageIndex, Cache, CacheConf,
                                              SummariesScore, InternetScore)



class AreaIndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'industry': ('name',), 'area': ('name',)}
    fields = ('name', 'status', 'area', 'industry')
    list_display = ('name','status', 'area', 'industry')
    search_fields = ('name', 'industry__name', 'area__name')
    list_filter = ('area', 'industry__level')


class RiskNewsAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = RiskNewsResources

    list_display = ('title', 'url', 'publisher', 'reprinted', 'pubtime')
    search_fields = ('title', 'content', 'url', 'reprinted', 'publisher__name',
                     'industry__name', 'enterprise__name', 'area__name')
    list_filter = (('pubtime', DateRangeFilter), 'industry__name')
    actions = ['delete_selected']

    def reduce_score(self, obj):
        industrys = obj.industry.all()
        enterprises = obj.enterprise.all()
        for industry in industrys:
            items = ScoreIndustry.objects.filter(industry=industry)
            for item in items:
                if item.score < 100:
                    score = int(item.score) + 1
                    ScoreIndustry.objects.filter(
                        id=item.id).update(score=score)
                else:
                    continue

        for enterprise in enterprises:
            items = ScoreEnterprise.objects.filter(enterprise=enterprise)
            for item in items:
                if item.score < 100:
                    score = int(item.score) + 1
                    ScoreEnterprise.objects.filter(
                        id=item.id).update(score=score)
                else:
                    continue
        return

    def delete_model(self, request, obj):
        self.reduce_score(obj)
        obj.delete()

    def delete_selected(self, request, objs):
        for obj in objs:
            self.reduce_score(obj)
            obj.delete()


class UserAreaAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    list_display = ('user', 'area')
    search_fields = ('user__username', 'area__name')


class ConsumeIndexAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = ConsumeIndexResources

    related_search_fields = {'industry': ('name',)}

    export_order = ('force', 'close', 'consume', 'year', 'industry', 'area')
    fields = ('force', 'close', 'consume', 'year', 'industry', 'area')
    list_display = ('force', 'close', 'consume', 'year', 'industry', 'area')
    search_fields = ('force', 'industry__name', 'year')
    list_filter = ('year', 'force', 'close', 'consume')


class SocietyIndexAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = SocietyIndexResources

    related_search_fields = {'industry': ('name',)}

    fields = ('trade', 'qualified', 'accident', 'year', 'industry', 'area')
    list_display = ('trade', 'qualified', 'accident', 'year', 'industry', 'area')
    search_fields = ('trade', 'industry__name', 'year')
    list_filter = ('year', 'trade', 'qualified', 'accident')


class ManageIndexAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = ManageIndexResources

    related_search_fields = {'industry': ('name',)}

    fields = ('licence', 'productauth', 'encourage', 'limit', 'remove',
              'year', 'industry', 'area')
    list_display = ('licence', 'productauth', 'encourage', 'limit',
                    'remove', 'year', 'industry', 'area',)
    search_fields = ('licence', 'productauth', 'encourage', 'limit', 'remove',
                     'industry__name', 'year')
    list_filter = ('year', 'productauth',)


class CacheAdmin(admin.ModelAdmin):
    fields = ('k', 'v', 'update_at')
    list_display = ('k', 'update_at')
    list_filter = ('k',)
    search_fields = ('k',)
    readonly_fields = ('update_at',)


class CacheConfAdmin(admin.ModelAdmin):
    fields = ('name', 'days', 'params')
    list_display = ('name', 'days', 'params')
    list_filter = ('name', 'days')
    search_fields = ('name',)

class SummariesScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'pubtime')
    list_display = ('score', 'pubtime')
    list_filter = ('score', 'pubtime')
    search_fields = ('pubtime',)


class InternetScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'pubtime')
    list_display = ('score', 'pubtime')
    list_filter = ('score', 'pubtime')
    search_fields = ('pubtime',)

admin.site.register(AreaIndustry, AreaIndustryAdmin)
admin.site.register(RiskNewsPublisher)
admin.site.register(RiskNews, RiskNewsAdmin)
admin.site.register(UserArea, UserAreaAdmin)
admin.site.register(SocietyIndex, SocietyIndexAdmin)
admin.site.register(ConsumeIndex, ConsumeIndexAdmin)
admin.site.register(ManageIndex, ManageIndexAdmin)
admin.site.register(Cache, CacheAdmin)
admin.site.register(CacheConf, CacheConfAdmin)
admin.site.register(SummariesScore, SummariesScoreAdmin)
admin.site.register(InternetScore, InternetScoreAdmin)
