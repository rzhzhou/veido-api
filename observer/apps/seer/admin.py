# -*- coding: utf-8 -*-
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from daterange_filter.filter import DateRangeFilter
from observer.apps.seer.resource import (
    ConsumeIndexResources, ManageIndexResources, SocietyIndexResources)
from observer.apps.seer.models import (Enterprise, Industry,
                                              UserArea, AreaIndustry,
                                              SocietyIndex, ConsumeIndex,
                                              ManageIndex, Cache, CacheConf,
                                              ModelWeight)



class AreaIndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'industry': ('name',), 'area': ('name',)}
    fields = ('name', 'status', 'area', 'industry')
    list_display = ('name','status', 'area', 'industry')
    search_fields = ('name', 'industry__name', 'area__name')
    list_filter = ('area', 'industry__level')

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


class ModelWeightAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'industry': ('name',), 'area': ('name',)}


class IndustryScoreAdmin(admin.ModelAdmin):
    search_fields = ('score', )
    list_display = ('score', 'time',)
    list_filter = ('score', ('time', DateRangeFilter),)


admin.site.register(AreaIndustry, AreaIndustryAdmin)
admin.site.register(UserArea, UserAreaAdmin)
admin.site.register(SocietyIndex, SocietyIndexAdmin)
admin.site.register(ConsumeIndex, ConsumeIndexAdmin)
admin.site.register(ManageIndex, ManageIndexAdmin)
admin.site.register(Cache, CacheAdmin)
admin.site.register(CacheConf, CacheConfAdmin)
admin.site.register(ModelWeight, ModelWeightAdmin)
# admin.site.register(IndustryScore, IndustryScoreAdmin)
