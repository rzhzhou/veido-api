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


class Weixin(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    origin_source = models.CharField(max_length=255, blank=True, verbose_name=u'信息转载来源')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    website_type = models.CharField(max_length=255, blank=True, verbose_name=u'网站类型')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    area = models.ForeignKey(Area, verbose_name=u'名称')

    class Meta:
        db_table = 'weixin'
        verbose_name_plural = u'微信'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class Weibo(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    origin_source = models.CharField(max_length=255, blank=True, verbose_name=u'信息
转载来源')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    website_type = models.CharField(max_length=255, blank=True, verbose_name=u'网站类型')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    area = models.ForeignKey(Area, verbose_name=u'名称')

    class Meta:
        db_table = 'weibo'
        verbose_name_plural = u'微博'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class Article(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')

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
    uuid = models.CharField(max_length=32, verbose_name=u'uuid')
    articles = models.ManyToManyField(Article, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'文章')
    weibo = models.ManyToManyField(Weibo, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'微博')
    weibo = models.ManyToManyField(Weixin, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'微信')

    class Meta:
        db_table = 'relateddata'
        verbose_name_plural = u'关联文章'

    def __unicode__(self):
        return self.uuid


