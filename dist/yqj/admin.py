#coding=utf-8
from django.contrib import admin
from django import forms
from django.contrib import messages
from datetime import datetime, timedelta
from yqj.mongoconnect import MongodbQuerApi
from models import WeixinPublisher, WeiboPublisher, ArticlePublisher,\
                   ArticleCategory, Group, User, Article, Topic, Custom,\
                   Keyword, Area

def show_pubtime(obj):
    return obj.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M')
show_pubtime.short_description = u'发布时间'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'area', 'feeling_factor', 'pubtime')
    list_editable = ('source', 'feeling_factor', 'pubtime', 'area',)
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
    list_display = ('title', 'source', 'area')
    list_editable = ('source', 'area',)
    list_filter = ('source',)
    search_fields = ('title', 'source')

class CrawlerTask(object):

    def __init__(self, key, mongo_task, task_type):
        self.key = key
        self.mongo_task = mongo_task
        self.task_type = task_type

    def insert_task(self, data):
        crawler_conf = {
            "type" : data.get('type',''),
            "status" : data.get('status', 0),
            "priority" : data.get('priority',3),
            "interval" : data.get('interval', 7200),
            "update_time" : datetime.utcnow(),
            "lastrun": datetime.utcnow(),
            "nextrun": datetime.utcnow() - timedelta(days=2),
            "crtetime": datetime.utcnow(),
            "timeout": 3600,
            "key": self.key,
            "data" : {
                "source_type" : self.task_type,
                "source" : data.get('source', '')}
        }

        if not MongodbQuerApi(self.mongo_task).find_one({'type':data.get('type',''),
                    'key': self.key}):
            MongodbQuerApi(self.mongo_task).save(crawler_conf)

    def type_task(self):
        types = {
            "baidu": "zjld.baidu.newstitle",
            "weibo": "zjld.weibo.newstitle",
            "sogou": "zjld.sogou.keywords",
        }
        weibodata = {
            "interval": 21600,
            "type": types.get('weibo'),
            "source": 'weibo'
        }

        weibo = self.insert_task(weibodata)

        baidudata = {
            "type": types.get('baidu'),
            "source": 'baidu',
        }
        baidu = self.insert_task(baidudata)

        weixindata = {
            "type": types.get('sogou'),
            "source": 'sogou'
        }
        weixin = self.insert_task(weixindata)

# Register your models here.

admin.site.register(WeixinPublisher)
admin.site.register(WeiboPublisher)
admin.site.register(ArticlePublisher)
admin.site.register(ArticleCategory)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Custom)
admin.site.register(Keyword, KeywordAdmin)
