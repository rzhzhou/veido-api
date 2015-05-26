#coding=utf-8
from django.contrib import admin
from django import forms
from django.contrib import messages
from yqj.mongoconnect import CrawlerTask
from models import WeixinPublisher, WeiboPublisher,Weibo, ArticlePublisher,\
                   ArticleCategory, Group, User, Article, Topic, Custom,\
                   Keyword, Area

def show_pubtime(obj):
    return obj.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M')
show_pubtime.short_description = u'发布时间'


class WeiboAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'website_type', 'area','pubtime')
    list_editable = ('source', 'pubtime',)
    list_filter = ('pubtime', )
    search_fields = ('title', 'source', 'content')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(level__lt=3)
        return super(WeiboAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'area', 'feeling_factor', 'pubtime')
    list_editable = ('source', 'feeling_factor', 'pubtime',)
    list_filter = ('pubtime', )
    search_fields = ('title', 'source', 'content')
    #raw_id_fields = ('area', 'publisher', )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(level__lt=3)
        return super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('newkeyword', 'review', 'group', 'custom')
    #list_editable = ('source', 'feeling_factor', 'pubtime',)
    list_filter = ('group', )
    search_fields = ('newkeyword', 'review')
    def save_model(self,request, obj, form, change):
        if obj.custom:
            obj.review = ''
        else:
            CrawlerTask(obj.review, 'zjld', u"关键词").type_task()
        # messages.error(request, 
        #         "The Parking Location field cannot be changedaaaaaaaaaaa.")
        obj.save()

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'abstract', 'source', 'area', 'keywords')
    list_display = ('title', 'source', 'area')
    list_editable = ('source', 'area',)
    list_filter = ('source',)
    search_fields = ('title', 'source')
    
    def save_model(self,request, obj, form, change):
        if not change:
            CrawlerTask(obj.title, 'zjld', u"事件").type_task()
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(level__lt=3)
        return super(TopicAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)




# Register your models here.

admin.site.register(WeixinPublisher)
admin.site.register(WeiboPublisher)
admin.site.register(Weibo,WeiboAdmin)
admin.site.register(ArticlePublisher)
admin.site.register(ArticleCategory)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Custom)
admin.site.register(Keyword, KeywordAdmin)
