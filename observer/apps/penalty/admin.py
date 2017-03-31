# -*- coding: utf-8 -*-
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from observer.apps.penalty.models import AdministrativePenalties
from observer.apps.penalty.resource import AdministrativePenaltiesResources

# Register your models here.


class AdministrativePenaltiesAdmin(ImportExportActionModelAdmin):
    resource_class = AdministrativePenaltiesResources
    # related_search_fields = {'area': ('name',)}
    search_fields = ('title', 'inspection_publisher__name',)
    list_display = ('title',  'pubtime', 'publisher',)
    list_filter = (('pubtime', DateRangeFilter), 'industry')


admin.site.register(AdministrativePenalties, AdministrativePenaltiesAdmin)
