# -*- coding: utf-8 -*-
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin

from observer.apps.origin.models import (Enterprise, Industry,
                                         InspectionPublisher, Inspection)
from observer.apps.origin.resource import (InspectionPublisherResources,
                                           InspectionResources, EnterpriseResources)


class IndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'parent': ('name',)}
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent__name')
    list_filter = ('level', )


class EnterpriseAdmin(ImportExportModelAdmin):
    resource_class = EnterpriseResources
    fields = ('name', 'area')
    list_display = ('name', 'area')
    search_fields = ('name', 'area__name')
    list_filter = ('area', )


class InspectionPublisherAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionPublisherResources


class InspectionAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionResources
    search_fields = ('url', 'title', 'enterprise__name',
                     'industry__name', 'area__name')
    list_display = ('title', 'qualitied', 'pubtime', 'publisher',)
    list_filter = ('pubtime', 'qualitied')


admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(InspectionPublisher, InspectionPublisherAdmin)
admin.site.register(Inspection, InspectionAdmin)
