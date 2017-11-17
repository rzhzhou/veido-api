
import jieba.analyse

from django import forms
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django.contrib import admin, messages
from import_export.admin import ImportExportActionModelAdmin

from observer.utils.connector.mongo import CrawlerTask
from observer.apps.yqj.models import (
    Area, Article, Custom,
    CustomKeyword, Group, GroupAuthUser, LocaltionScore,
    User,save_user)

from import_export.admin import ImportExportActionModelAdmin
from django.conf import settings


def show_pubtime(obj):
    return obj.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M')


show_pubtime.short_description = u'发布时间'


class WeiboAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    list_display = ('title', 'source', 'website_type', 'area', 'pubtime')
    list_editable = ('source', 'pubtime',)
    list_filter = ('pubtime', )
    search_fields = ('title', 'source', 'content')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(level__lt=3)
        return super(WeiboAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class WeixinAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    fields = (
        'author', 'title', 'url', 'content', 'origin_source', 'source',
        'website_type', 'pubtime', 'publisher', 'area', 'uuid', 'readnum', 'likenum')
    list_display = (
        'author', 'title', 'origin_source', 'source', 'pubtime', 'publisher', 'area', 'readnum')
    list_editable = ('title', 'pubtime', 'readnum',)
    list_filter = ('source', 'origin_source', 'pubtime',)
    search_fields = ('title', 'source')


class ArticleAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)} 
    # fields = ('title', 'source', 'area', 'feeling_factor', 'pubtime', 'website_type')
    search_fields = ('title', 'source', 'content')
    # raw_id_fields = ('area', 'source')


class CustomKeywordAdmin(admin.ModelAdmin):
    list_display = ('newkeyword', 'review', 'group', 'custom')
    # list_editable = ('source', 'feeling_factor', 'pubtime',)
    list_filter = ('group', )
    search_fields = ('newkeyword', 'review')

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.custom:
                obj.review = ''
            else:
                CrawlerTask(obj.review, 'zjld', u"关键词").type_task()
            # messages.error(request,
            #         "The Parking Location field cannot be changedaaaaaaaaaaa.")
            obj.save()
        else:
            key_list = CustomKeyword.objects.filter(id=obj.id)
            if len(key_list) == 0:
                return
            old_keyword = key_list[0].review
            if not old_keyword:
                old_keyword = key_list[0].custom
            if old_keyword == obj.review:
                return
            CrawlerTask(obj.review, "zjld", u"关键词").update_task(old_keyword)
            obj.save()

    def delete_model(self, request, obj):
        key_list = CustomKeyword.objects.filter(id=obj.id)
        if len(key_list) == 0:
            return
        del_index = key_list[0].review
        if not del_index:
            del_index = key_list[0].custom
        CrawlerTask(del_index, "zjld", u"关键词").del_task()
        obj.delete()


class TopicAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    fields = ('title', 'abstract', 'source', 'area', 'keywords', 'pubtime')
    list_display = ('title', 'source', 'area', 'pubtime',)
    list_editable = ('source', 'pubtime')
    list_filter = ('source', 'pubtime',)
    search_fields = ('title', 'source')

    def save_model(self, request, obj, form, change):
        obj.keywords = jieba.analyse.extract_tags(
            obj.title,
            topK=3,
            withWeight=True,
            allowPOS=()
        )
        # return <type 'list'> contain tuple
        if not change:
            CrawlerTask(obj.title, 'zjld', u"事件").type_task()
        else:
            key_list = Topic.objects.filter(id=obj.id)
            if not key_list:
                return
            old_keyword = key_list[0].title
            if old_keyword != obj.title:
                CrawlerTask(obj.title, "zjld", u"事件").update_task(old_keyword)

        Event(title=obj.title).save()
        obj.save()

    def delete_model(self, request, obj,):
        key_list = Topic.objects.filter(id=obj.id)
        if not key_list:
            return
        del_index = key_list[0].title
        if not del_index:
            return
        CrawlerTask(del_index, "zjld", u"事件").del_task()
        obj.delete()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(level__lt=3)
        return super(TopicAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ProductKeywordAdmin(admin.ModelAdmin):
    list_display = ('newkeyword', 'review', 'group', 'product')
    list_filter = ('group', )
    search_fields = ('newkeyword', 'review')

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.product:
                obj.review = ''
            else:
                CrawlerTask(obj.review, 'zjld', u"关键词").type_task()
            # messages.error(request,
            #         "The Parking Location field cannot be changedaaaaaaaaaaa.")
            obj.save()
        else:
            key_list = ProductKeyword.objects.filter(id=obj.id)
            if len(key_list) == 0:
                return
            old_keyword = key_list[0].review
            if not old_keyword:
                old_keyword = key_list[0].product
            if old_keyword == obj.review:
                return
            CrawlerTask(obj.review, "zjld", u"关键词").update_task(old_keyword)
            obj.save()

    def delete_model(self, request, obj):
        key_list = ProductKeyword.objects.filter(id=obj.id)
        if len(key_list) == 0:
            return
        del_index = key_list[0].review
        if not del_index:
            del_index = key_list[0].product
        CrawlerTask(del_index, "zjld", u"关键词").del_task()
        obj.delete()


class LocaltionScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'group', 'article')
    # list_display = ('score', 'group', 'risk')
    # list_editable = ('score', 'group')
    list_filter = ('score', 'group')
    search_fields = ('score', 'group')


class RiskScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'risk')
    # list_display = ('score', 'risk')
    # list_filter = ('score', 'article')
    search_fields = ('score', 'risk')


admin.site.register(User)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Custom)
admin.site.register(CustomKeyword, CustomKeywordAdmin)
admin.site.register(GroupAuthUser)
admin.site.register(LocaltionScore, LocaltionScoreAdmin)
