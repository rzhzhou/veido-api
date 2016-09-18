# -*- coding: utf-8 -*-
from django.contrib import admin

from observer.apps.inspection.models import RawInspection

# Register your models here.


class RawInspectionAdmin(admin.ModelAdmin):

    # related_search_fields = {'area': ('name',)}
    fields = ('title', 'url', 'publisher', 'pubtime')
    list_display = ('title', 'url', 'publisher', 'pubtime')
    search_fields = ('title', 'content', 'url', 'publisher')
    actions = ['delete_selected']

    def delete_model(self, request, obj):
        self.reduce_score(obj)
        obj.delete()

    def delete_selected(self, request, objs):
        for obj in objs:
            self.reduce_score(obj)
            obj.delete()


admin.site.register(RawInspection, RawInspectionAdmin)
