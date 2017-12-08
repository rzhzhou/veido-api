from django.contrib import admin, messages

from observer.apps.yqj.models import (Article, )

class ArticleAdmin(admin.ModelAdmin):
    fields = ('base_article', 'category')
    list_display = ('base_article', 'category')
    list_filter = ('base_article', 'category')
    search_fields = ('base_article', 'category')


admin.site.register(Article, ArticleAdmin)
