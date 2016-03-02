# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.db import models
from tinymce.models import HTMLField

from observer.apps.base.models import Article, Area, Category, RelatedData


class News(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = HTMLField(blank=True, verbose_name=u'正文')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')

    area = models.ForeignKey(Area, verbose_name=u'地域')

    class Meta:
        db_table = 'article'
        verbose_name_plural = u'质监热点'

    def __unicode__(self):
        return self.title

class LRisk(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    abstract = models.TextField(blank=True, verbose_name=u'简介')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'首发媒体')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    keywords = models.CharField(max_length=255, default=u'', verbose_name=u'关键词', blank=True)
    score = models.IntegerField(default=0, verbose_name=u'评分')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', null=True, blank=True,)

    class Meta:
        db_table = 'risk'
        verbose_name_plural = u'本地评分'

    def __unicode__(self):
        return self.title


class TRisk(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    abstract = models.TextField(blank=True, verbose_name=u'简介')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'首发媒体')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    keywords = models.CharField(max_length=255, default=u'', verbose_name=u'关键词', blank=True)
    score = models.IntegerField(default=0, verbose_name=u'评分')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', null=True, blank=True,)

    class Meta:
        db_table = 'risk'
        verbose_name_plural = u'风险评分'

    def __unicode__(self):
        return self.title

class ProductMonitor(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name='名称')

    articles = models.ManyToManyField(Article, related_name='products', related_query_name='product', null=True, blank=True, verbose_name=u'文章')

    class Meta:
        db_table = 'product'
        verbose_name_plural = u'产品监测'

    def __unicode__(self):
        return self.name

class ZJInspection(models.Model):
    url = models.URLField(max_length=255, verbose_name=u'网站链接')
    name = models.CharField(max_length=255, verbose_name=u'标题')
    manufacturer = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'转载次数')
    qualitied = models.FloatField(verbose_name=u'合格率')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    product = models.CharField(max_length=255, verbose_name=u'产品')
    source = models.CharField(max_length=255, verbose_name=u'信息来源')
    status = models.IntegerField(null=False, default=3, verbose_name=u'名称')
    create_at = models.DateTimeField(auto_now=False, verbose_name=u'创建时间')
    update_at = models.DateTimeField(auto_now=False, verbose_name=u'更新时间')
    create_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'创建人')
    province = models.CharField(max_length=255, verbose_name=u'省')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'市')
    district = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'地区')
    sync = models.IntegerField(null=True, blank=True, verbose_name=u'同步状态')

    class Meta:
        db_table = 'inspection'
        verbose_name_plural = u'抽检'

    def __unicode__(self):
        return self.name


class RelatedDataAtricle(models.Model):
    article = models.ForeignKey(Article)
    relateddata = models.ForeignKey(RelatedData)

    class Meta:
        db_table = 'relateddata_articles'


class CategoryAtricle(models.Model):
    article = models.ForeignKey(Article)
    category = models.ForeignKey(Category)

    class Meta:
        db_table = 'category_articles'
