# -*- coding: utf-8 -*-
import jieba.analyse

from django import forms
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django.contrib import admin, messages

from observer.utils.connector.mongo import CrawlerTask
from yqj_save import MySQLQuerApi
from observer.apps.base.models import (
    Area, Article, ArticlePublisher, Category, Custom,
    CustomKeyword, Group, GroupAuthUser, LocaltionScore, Product, ProductKeyword,
    Risk, LRisk, TRisk, RiskScore, Topic, User, Weibo, WeiboPublisher, Weixin,
    WeixinPublisher, save_user, ZJInspection, News)
from observer.apps.corpus.models import Event
from resource import InspectionResources
from import_export.admin import ImportExportActionModelAdmin


def show_pubtime(obj):
    return obj.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M')


show_pubtime.short_description = u'发布时间'


class NewsAdmin(admin.ModelAdmin):
    fields = ('url', 'title', 'content', 'author', 'pubtime', 'source', 'area')
    list_display = ('title', 'source', 'pubtime', 'area')
    search_fields = ('url', 'title', 'content', 'author', 'area')
    list_filter = ('pubtime',)

    def save_model(self, request, obj, form, change):
        MySQLQuerApi().insert(obj)


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
    list_display = ('title', 'source', 'area', 'feeling_factor', 'pubtime')
    list_editable = ('source', 'feeling_factor', 'pubtime')
    list_filter = ('pubtime',)
    search_fields = ('title', 'source', 'content')
    raw_id_fields = ('area', 'publisher')


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
        obj.keywords = jieba.analyse.extract_tags(obj.title, topK=3, withWeight=True, allowPOS=())
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


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', )
    list_display = ('name',)
    list_editable = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


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


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'area', 'isAdmin', 'group')
    list_display = ('username', 'password', 'area', 'isAdmin', 'group',)
    list_editable = ('username', 'password', 'area', 'isAdmin', 'group')

    def save_model(self, request, obj, form, change):
        save_user(obj.username, obj.password, obj.area, obj.group, obj.isAdmin)


class GroupAuthUserAdmin(admin.ModelAdmin):
    fields = ('auth', 'group')
    list_display = ('auth', 'group')
    list_editable = ('auth', 'group')
    list_filter = ('auth', 'group')
    search_fields = ('auth', 'group')


class LocaltionScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'group', 'risk')
    list_display = ('score', 'group', 'risk')
    # list_editable = ('score', 'group')
    list_filter = ('score', 'group')
    search_fields = ('score', 'group')


class RiskScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'risk')
    list_display = ('score', 'risk')
    # list_filter = ('score', 'article')
    search_fields = ('score', 'risk')


class RiskAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    fields = ('title', 'abstract', 'source', 'area', 'keywords', 'score', 'pubtime')
    list_display = ('title', 'source', 'area', 'keywords', 'pubtime')
    list_editable = ('title', 'source', 'keywords', 'pubtime')
    list_filter = ('title', 'pubtime')
    search_fields = ('title', 'pubtime')

    def save_model(self, request, obj, form, change):
        obj.keywords = jieba.analyse.extract_tags(obj.title, topK=3, withWeight=True, allowPOS=())
        if not change:
            CrawlerTask(obj.title, 'zjld', u"风险快讯").type_task()
            obj.save()
        else:
            key_list = Risk.objects.filter(id=obj.id)
            if not key_list:
                return
            old_keyword = key_list[0].title
            if not obj.title:
                return
            if old_keyword != obj.title:
                CrawlerTask(obj.title, "zjld", u"风险快讯").update_task(old_keyword)
            obj.save()

    def delete_model(self, request, obj):
        key_list = Risk.objects.filter(id=obj.id)
        if not key_list:
            return
        del_index = key_list[0].title
        CrawlerTask(del_index, "zjld", u"风险快讯").del_task()
        obj.delete()


class LRiskAdmin(admin.ModelAdmin):
    fields = ('title', 'score', 'pubtime')
    list_display = ('title', 'score', 'pubtime')
    list_editable = ('title', 'score', 'pubtime')
    list_filter = ('title', 'pubtime')
    search_fields = ('title', 'pubtime')

    def save_model(self, request, obj, form, change):
        groupauth = GroupAuthUser.objects.get(auth=request.user)
        company = groupauth.group
        risk_id = obj.id
        score = obj.score
        localscore = LocaltionScore(score=score, group=company, risk_id=risk_id)

        loca = LocaltionScore.objects.filter(risk_id=risk_id, group=company)
        if loca:
            loca.delete()
            localscore.save()
        else:
            localscore.save()

        obj.save()


class TRiskAdmin(admin.ModelAdmin):
    fields = ('title', 'score', 'pubtime')
    list_display = ('title', 'score', 'pubtime')
    list_editable = ('title', 'score', 'pubtime')
    list_filter = ('title', 'pubtime')
    search_fields = ('title', 'pubtime')

    def save_model(self, request, obj, form, change):
        score = obj.score
        risk_id = obj.id
        risk_score = RiskScore(score=score, risk_id=risk_id)

        risk = RiskScore.objects.filter(risk_id=risk_id)
        if risk:
            risk.delete()
            risk_score.save()
        else:
            risk_score.save()


class InspectionAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionResources
    search_fields = ('url', 'name', 'source',)
    list_display = ('name', 'product', 'qualitied', 'source', 'pubtime')
    list_filter = ('pubtime', 'province', 'city', 'district', 'product', 'source', )


admin.site.register(WeixinPublisher)
admin.site.register(WeiboPublisher)
admin.site.register(Weibo, WeiboAdmin)
admin.site.register(Weixin, WeixinAdmin)
admin.site.register(ArticlePublisher)
admin.site.register(Category)
admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Custom)
admin.site.register(CustomKeyword, CustomKeywordAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductKeyword, ProductKeywordAdmin)
admin.site.register(GroupAuthUser, GroupAuthUserAdmin)
admin.site.register(LocaltionScore, LocaltionScoreAdmin)
admin.site.register(RiskScore, RiskScoreAdmin)
admin.site.register(Risk, RiskAdmin)
admin.site.register(LRisk, LRiskAdmin)
admin.site.register(TRisk, TRiskAdmin)
admin.site.register(ZJInspection, InspectionAdmin)
