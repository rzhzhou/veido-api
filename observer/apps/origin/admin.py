# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from resource import InspectionResources
from observer.apps.base.models import Area
from observer.apps.origin.models import InspectionPublisher, Inspection
from observer.apps.riskmonitor.models import Industry, Enterprise



class InspectionAdmin(ImportExportModelAdmin):
    resource_class = InspectionResources
    search_fields = ('url', 'title',)
    list_display = ('title', 'qualitied', 'pubtime', 'publisher')
    list_filter = ('pubtime', 'qualitied' )

admin.site.register(InspectionPublisher)
admin.site.register(Inspection, InspectionAdmin)