# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from observer.apps.base.models import Area


class Brand(models.Model):
    zh_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'中文名称')
    en_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'英文名称')
    logo = models.URLField(verbose_name=u'图标')

    class Meta:
        db_table = 'brand'
        verbose_name_plural = u'品牌'

    def __unicode__(self):
        return self.en_name+self.zh_name


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'企业名')
    locate_x = models.FloatField(verbose_name=u'纬度', null=True, blank=True)
    locate_y = models.FloatField(verbose_name=u'经度', null=True, blank=True)
    scale = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'规模')
    ccc = models.BooleanField(default=False, verbose_name=u'ccc认证')

    area = models.ForeignKey(Area, verbose_name=u'地域')

    class Meta:
        db_table = 'enterprise'
        verbose_name_plural = u'企业'

    def __unicode__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'行业层级')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        db_table = 'industry'
        verbose_name_plural = u'行业'

    def __unicode__(self):
        return self.name


class Metrics(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'指标')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')

    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        db_table = 'metrics'
        verbose_name_plural = u'指标'

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'生产产品')

    enterprise = models.ForeignKey(Enterprise, null=True, blank=True, verbose_name=u'企业')
    industry = models.ForeignKey(Industry, null=True, blank=True, verbose_name=u'产品')

    class Meta:
        db_table = 'product'
        verbose_name_plural = u'生产产品'

    def __unicode__(self):
        return self.name


class ProductMetrics(models.Model):
    weight = models.CharField(max_length=255, verbose_name=u'权重')

    metrics = models.ForeignKey(Metrics, verbose_name=u'指标')
    product = models.ForeignKey(Product, verbose_name=u'产品')

    class Meta:
        db_table = 'metrics_product'
        verbose_name_plural = u'产品指标'

    def __unicode__(self):
        return self.weight


class RiskData(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'作者链接地址')
    user_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'作者名')
    content = models.TextField(blank=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name=u'发布时间')
    comment = models.CharField(max_length=255, verbose_name=u'是否自营')
    comment_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'评论地址')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    show_pic = models.TextField( null=True, blank=True, verbose_name=u'图片评论图')
    score = models.IntegerField(null=True, blank=True, verbose_name=u'评分')
    url = models.URLField( null=True, blank=True, verbose_name=u'网站链接')
    uuid = models.CharField(max_length=255, default=uuid.uuid4, verbose_name=u'uuid')
    
    area = models.ForeignKey(Area, verbose_name=u'地域')
    brand = models.ForeignKey(Brand, verbose_name=u'品牌')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        db_table = 'risk_data'
        verbose_name_plural = u'电商风险评论'

    def __unicode__(self):
        return self.source


class ScoreIndustry(models.Model):
    score = models.CharField(max_length=255, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', default=timezone.now())

    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        db_table = 'score_industry'
        verbose_name_plural = u'行业分值'

    def __unicode__(self):
        return self.score


class ScoreEnterprise(models.Model):
    score = models.CharField(max_length=255, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', default=timezone.now())

    enterprise = models.ForeignKey(Enterprise, verbose_name=u'企业')

    class Meta:
        db_table = 'score_enterprise'
        verbose_name_plural = u'企业分值'

    def __unicode__(self):
        return self.score


class ScoreProduct(models.Model):
    score = models.CharField(max_length=255, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', default=timezone.now())

    product = models.ForeignKey(Product, verbose_name=u'产品')

    class Meta:
        db_table = 'score_product'
        verbose_name_plural = u'产品分值'

    def __unicode__(self):
        return self.score


class UserEnterprise(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    enterprise = models.ForeignKey(Enterprise, verbose_name=u'企业')

    class Meta:
        db_table = 'user_enterprise'
        verbose_name_plural = u'监测企业'

    def __unicode__(self):
        return self.enterprise.name


class UserIndustry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')

    user = models.ForeignKey(User, verbose_name=u'用户')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        db_table = 'user_industry'
        verbose_name_plural = u'支柱行业'

    def __unicode__(self):
        return self.name


class RiskNewsPublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')
    searchmode = models.IntegerField(default=0, verbose_name=u'搜索方式')

    class Meta:
        db_table = 'risknewspublisher'
        verbose_name_plural = u'风险新闻发布者'

    def __unicode__(self):
        return self.publisher


class RiskNews(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(RiskNewsPublisher, verbose_name=u'文章发布者')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    uuid = models.CharField(max_length=36)
    feeling_factor = models.FloatField(default=-1, verbose_name=u'正负面')
    reshipment = models.IntegerField(verbose_name=u'转载数')

    class Meta:
        db_table = 'risk_news'
        verbose_name_plural = u'风险新闻'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title
