#coding: utf-8
from django.conf import settings
from django.db import IntegrityError, transaction
from observer.apps.base.models import Article, Area, RelatedData, \
     ArticlePublisher, RelatedDataAtricle, Category, CategoryAtricle
from django.http import HttpResponse
from simArticle import  _cal_values
from query import *
import uuid


class MySQLQuerApi(object):

    def changetype(self, obj, uid):
        dct = {
            'author': obj.author,
            'title': obj.title,
            'url': obj.url,
            'content': obj.content,
            'source': obj.source,
            'pubtime': obj.pubtime,
            'uuid': uid,
            'area': Area.objects.get(name=obj.area.name , level=obj.area.level),
            'publisher': get_article_publisher(obj.source) if article_publisher_count(obj.source) \
                else save_article_publisher(data={"publisher": obj.source}),
        }
        return dct

    def insert_to_categoryarticle(self, article):
        hot_id = get_category('质监热点')
        CategoryAtricle(article=article, category=hot_id).save()


    def insert_to_relateddata(self, article, article_title, article_pubtime, uid):
        relateddata = RelatedData(uuid=uid)
        relateddata.save()
        result = _cal_values("article",article_title, article_pubtime)
        for r in result:
            if not RelatedData.objects.filter(uuid=r.uuid):
                self.insert_to_relateddata(r, r.title, r.pubtime, r.uuid)
            RelatedDataAtricle(article=r, relateddata=relateddata).save()
            re_id = RelatedData.objects.get(uuid=r.uuid)
            if re_id:
                RelatedDataAtricle(article=article, relateddata=re_id).save()


    @transaction.atomic()
    def insert(self, obj):
        sid = transaction.savepoint()
        try:
            uid = uuid.uuid1()
            article_title = obj.title
            article_pubtime = obj.pubtime
            fields = self.changetype(obj, uid)
            article = Article(**fields)
            article.save()

            self.insert_to_relateddata(article, article_title, article_pubtime, uid)
            self.insert_to_categoryarticle(article)
        except:
            return transaction.savepoint_rollback(sid)
        else:
            return transaction.savepoint_commit(sid)
