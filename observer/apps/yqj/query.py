# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/cluster'
sys.path.append(root_mod)

from datetime import timedelta
from backend.base.models import Area, ArticlePublisher, Article ,\
                        RelatedData, Category

def save_article_publisher(data):
    article_publisher = ArticlePublisher(
        publisher=data["publisher"],
        searchmode=data.get("searchmode", 0)
    )
    article_publisher.save()

    return article_publisher

def save_article(data):
    article = Article(
        author=data["author"],
        title=data["title"],
        url=data["url"],
        content=data["content"],
        source=data["source"],
        pubtime=data["pubtime"],
        publisher=data["publisher"],
        area=data["area"],
        uuid=data["uuid"],
        website_type=data["website_type"],
    )
    article.save()

    return article

def save_relateddata(data):
    relateddata = RelatedData(
        uuid=data["id"]
    )
    relateddata.save()

    return relateddata


def get_article_publisher(publisher):
    return ArticlePublisher.objects.filter(publisher=publisher)[0]


def get_relateddata(uuid):
    """
    Get Single RelatedData Instance
    """
    return RelatedData.objects.get(uuid = uuid)


def get_article(uuid):
    """
    Get Single Article Instance
    """
    return AArticle.objects.get(uuid = uuid)

def get_category(name):

    return Category.objects.get(name = name)


def article_publisher_count(publisher):

    return ArticlePublisher.objects.filter(publisher = publisher).count()
