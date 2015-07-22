#coding=utf-8
from django.contrib import admin
from django import forms
from django.contrib import messages
from yqj.mongoconnect import CrawlerTask
from models import WeixinPublisher, WeiboPublisher,Weibo, ArticlePublisher,\
                   Category, Group, User, Article, Topic, Custom,\
                   CustomKeyword, Area,Weixin, Product, ProductKeyword, save_user,\
                   GroupAuthUser, LocaltionScore
# from django.contrib.auth.models import User
import jieba.analyse

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

class WeixinAdmin(admin.ModelAdmin):
    fields=('author','title','url','content','origin_source','source','website_type','pubtime','publisher','area','uuid','readnum','likenum')
    list_display=('author','title','origin_source','source','pubtime','publisher','area','readnum')
    list_editable=('title','pubtime','readnum',)
    list_filter=('source','origin_source','pubtime',)
    search_fields=('title','source')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'area', 'feeling_factor', 'pubtime', 'localtion_score')
    list_editable = ('source', 'feeling_factor', 'pubtime', 'localtion_score')
    list_filter = ('pubtime', 'localtion_score')
    search_fields = ('title', 'source', 'content', 'localtion_score')
    #raw_id_fields = ('area', 'publisher', )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(level__lt=3)
        return super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        groupauth = GroupAuthUser.objects.get(auth=request.user)
        company = groupauth.group
        article = obj
        score = obj.localtion_score
        localscore = LocaltionScore(score=score, group=company, article=article)

        try:
            print LocaltionScore.objects.get(article=article, company=company)
            localscore.save()
        except:
            localscore.save()
        obj.save()  
        # print obj.area
        # obj.save()


class CustomKeywordAdmin(admin.ModelAdmin):
    list_display = ('newkeyword', 'review', 'group', 'custom')
    #list_editable = ('source', 'feeling_factor', 'pubtime',)
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

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'abstract', 'source', 'area', 'keywords')
    list_display = ('title', 'source', 'area')
    list_editable = ('source', 'area',)
    list_filter = ('source',)
    search_fields = ('title', 'source')
    #
    def save_model(self,request, obj, form, change):
        obj.keywords = jieba.analyse.extract_tags(obj.title, topK=3, withWeight=True, allowPOS=())
         # return <type 'list'> contain tuple

        if not change:
            CrawlerTask(obj.title, 'zjld', u"事件").type_task()
        obj.save()

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
    # def save_model(   self, request, obj, form, change):
    def save_model(self,request, obj, form, change):
        save_user(obj.username, obj.password, obj.area, obj.group, obj.isAdmin)


class GroupAuthUserAdmin(admin.ModelAdmin):
    fields = ('auth', 'group')
    list_display = ('auth', 'group')
    list_editable = ('auth', 'group')
    list_filter = ('auth', 'group')
    search_fields = ('auth', 'group')


# class LocaltionScoreAdmin(admin.ModelAdmin):
#     fields = ('score', 'groupauthuser', 'article')
#     list_display = ('score', 'groupauthuser', 'article')
#     list_editable = ('score', 'groupauthuser', 'article')
#     list_filter = ('score', 'groupauthuser', 'article')
#     search_fields = ('score', 'groupauthuser', 'article')
# Register your models here.

admin.site.register(WeixinPublisher)
admin.site.register(WeiboPublisher)
admin.site.register(Weibo,WeiboAdmin)
admin.site.register(Weixin,WeixinAdmin)
admin.site.register(ArticlePublisher)
admin.site.register(Category)
admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Custom)
admin.site.register(CustomKeyword, CustomKeywordAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductKeyword, ProductKeywordAdmin)
admin.site.register(GroupAuthUser, GroupAuthUserAdmin)
# admin.site.register(LocaltionScore, LocaltionScoreAdmin)

