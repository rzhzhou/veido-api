# -*- coding: utf-8 -*-
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from observer.apps.penalty.models import AdministrativePenalties

# Register your models here.


class AdministrativePenaltiesAdmin(ImportExportModelAdmin):

    # related_search_fields = {'area': ('name',)}
    fields = ('title', 'url', 'publisher', 'pubtime','province','city','district','industry','productCategory','brand','caseName','penaltyOrgan','punishedName','punishedDistrict','illegalBehavior','punishmentBasis','punishmentRsult')
    list_display = ('title', 'url', 'publisher', 'pubtime','publisher','province','city','district','industry','productCategory','brand','caseName','penaltyOrgan','punishedName','punishedDistrict','illegalBehavior','punishmentBasis','punishmentRsult')
    search_fields = ('title', 'url', 'publisher', 'pubtime','publisher','province','city','district','industry','productCategory','brand','caseName','penaltyOrgan','punishedName','punishedDistrict','illegalBehavior','punishmentBasis','punishmentRsult')


admin.site.register(AdministrativePenalties, AdministrativePenaltiesAdmin)
