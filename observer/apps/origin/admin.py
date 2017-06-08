# -*- coding: utf-8 -*-
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter
from observer.apps.origin.models import (Area, Enterprise, Industry,
                                         InspectionPublisher, Inspection,
                                         ProductBenchmark, IndustryScore)
from observer.apps.origin.resource import (InspectionPublisherResources,
                                           InspectionResources, EnterpriseResources)


class AreaAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'parent': ('name',)}
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent__name')
    list_filter = ('level', )


class IndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'parent': ('name',)}
    fields = ('name','code', 'level', 'parent')
    list_display = ('name', 'code', 'level', 'parent')
    search_fields = ('name', 'level', 'parent__name')
    list_filter = ('level', )


class EnterpriseAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    resource_class = EnterpriseResources
    fields = ('name', 'area', 'product_name', 'issues')
    list_display = ('name', 'area', 'product_name', 'issues')
    search_fields = ('name', 'area__name', 'product_name', 'issues')
    list_filter = ('area', )


class InspectionPublisherAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionPublisherResources


class InspectionAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionResources
    search_fields = ('title', 'publisher__name',)
    list_display = ('title', 'qualitied', 'pubtime', 'publisher',)
    list_filter = (('pubtime', DateRangeFilter), 'industry', 'qualitied',)


class ProductBenchmarkAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', 'level', 'parent', )
    list_display = ('name', 'code', 'level', 'parent', )
    list_filter = ('level', )


class IndustryScoreAdmin(admin.ModelAdmin):
    search_fields = ('score', )
    list_display = ('score', 'time',)
    list_filter = ('score', ('time', DateRangeFilter),)


admin.site.register(Area, AreaAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(InspectionPublisher, InspectionPublisherAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(ProductBenchmark, ProductBenchmarkAdmin)
admin.site.register(IndustryScore, IndustryScoreAdmin)
