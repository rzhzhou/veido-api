from django.contrib import admin, messages

from observer.apps.yqj.models import (Inspection, Article, )

class InspectionAdmin(admin.ModelAdmin):
    fields = ('base_inspection', 'qualitied')
    # list_display = ('score', 'risk')
    # list_filter = ('score', 'article')
    # search_fields = ('score', 'risk')

class ArticleAdmin(admin.ModelAdmin):
    pass
    # fields = ('score', 'risk')
    # list_display = ('score', 'risk')
    # list_filter = ('score', 'article')
    # search_fields = ('score', 'risk')


admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Article, ArticleAdmin)
