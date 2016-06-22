# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin

from observer.apps.origin.models import InspectionPublisher, Inspection
from resource import InspectionResources


class InspectionAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionResources
    search_fields = ('url', 'title', 'enterprise__name', 'industry__name', 'area__name')
    list_display = ('title', 'qualitied', 'pubtime', 'publisher',)
    list_filter = ('pubtime', 'qualitied' )

admin.site.register(InspectionPublisher)
admin.site.register(Inspection, InspectionAdmin)