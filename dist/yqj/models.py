#coding: utf-8
from django.db import models

# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        db_table = 'area'
        verbose_name_plural = u'地域'

    def __unicode__(self):
        return self.name

class WeixinPublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'weixinpublisher'
        verbose_name_plural = u'微信发布者'

    def __unicode__(self):
        return self.publisher



class Weixin(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    origin_source = models.CharField(max_length=255, blank=True, verbose_name=u'信息转载来源')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    website_type = models.CharField(max_length=255, blank=True, verbose_name=u'网站类型')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(WeixinPublisher, verbose_name=u'微信发布者')
    area = models.ForeignKey(Area, verbose_name=u'名称')

    class Meta:
        db_table = 'weixin'
        verbose_name_plural = u'微信'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class WeiboPublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'weibopublisher'
        verbose_name_plural = u'微博发布者'

    def __unicode__(self):
        return self.publisher


class Weibo(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    origin_source = models.CharField(max_length=255, blank=True, verbose_name=u'信息转载来源')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    website_type = models.CharField(max_length=255, blank=True, verbose_name=u'网站类型')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(WeiboPublisher, verbose_name=u'微博发布者')
    area = models.ForeignKey(Area, verbose_name=u'名称')
    praise = models.IntegerField(blank=True, verbose_name=u'点赞数')
    comment = models.IntegerField(blank=True, verbose_name=u'评论量')
    tansmit = models.IntegerField(blank=True, verbose_name=u'转发量')

    class Meta:
        db_table = 'weibo'
        verbose_name_plural = u'微博'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class ArticlePublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'articlepublisher'
        verbose_name_plural = u'文章发布者'

    def __unicode__(self):
        return self.publisher


class Article(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(ArticlePublisher, verbose_name=u'文章发布者')
    area = models.ForeignKey(Area, verbose_name=u'名称')

    class Meta:
        db_table = 'article'
        verbose_name_plural = u'文章'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    abstract = models.TextField(blank=True, verbose_name=u'正文')
    articles = models.ManyToManyField(Article, related_name='topic', related_query_name='topics', null=True, blank=True, verbose_name=u'文章')
    weibo = models.ManyToManyField(Weibo, related_name='topic', related_query_name='topics', null=True, blank=True, verbose_name=u'微博')
    weibo = models.ManyToManyField(Weixin, related_name='topic', related_query_name='topics', null=True, blank=True, verbose_name=u'微信')

    class Meta:
        db_table = 'topic'
        verbose_name_plural = u'聚类事件'

    def __unicode__(self):
        return self.title


class RealtedData(models.Model):
    uuid = models.CharField(max_length=36, verbose_name=u'uuid')
    articles = models.ManyToManyField(Article, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'文章')
    weibo = models.ManyToManyField(Weibo, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'微博')
    weixin = models.ManyToManyField(Weixin, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'微信')

    class Meta:
        db_table = 'relateddata'
        verbose_name_plural = u'关联文章'

    def __unicode__(self):
        return self.uuid


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=u'')
    remark = models.CharField(max_length=255, blank=True, verbose_name=u'备注')

    articles = models.ManyToManyField(Article, related_name='categorys', related_query_name='category', null=True, blank=True, verbose_name=u'文章')

    class Meta:
        db_table = 'article_category'
        verbose_name_plural = u'文章分类'
