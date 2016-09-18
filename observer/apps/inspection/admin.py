# -*- coding: utf-8 -*-
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from observer.apps.inspection.models import RawInspection

# Register your models here.


class RawInspectionAdmin(ImportExportModelAdmin):

    # related_search_fields = {'area': ('name',)}
    fields = ('title', 'url', 'publisher', 'pubtime')
    list_display = ('title', 'url', 'publisher', 'pubtime')
    search_fields = ('title', 'content', 'url', 'publisher')


admin.site.register(RawInspection, RawInspectionAdmin)
