from django.contrib import admin, messages

from observer.apps.yqj.models import (Inspection, Article, )

class InspectionAdmin(admin.ModelAdmin):
    fields = ('base_inspection', 'qualitied')
    list_display = ('base_inspection', 'qualitied')
    list_filter = ('base_inspection', 'qualitied')
    search_fields = ('base_inspection', 'qualitied')

class ArticleAdmin(admin.ModelAdmin):
    fields = ('base_article', 'category')
    list_display = ('base_article', 'category')
    list_filter = ('base_article', 'category')
    search_fields = ('base_article', 'category')


admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Article, ArticleAdmin)
