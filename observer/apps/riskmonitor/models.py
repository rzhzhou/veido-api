# -*- coding: utf-8 -*-
from django.db import models

from observer.apps.base.models import Area
from django.contrib.auth.models import User 


class Score(models.Model):
    score = models.CharField(max_length=255, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')

    class Meta:
        db_table = 'score'
        verbose_name_plural = u'分值'

    def __unicode__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'行业层级')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')
    score = models.ForeignKey(Score, null=True, blank=True, verbose_name=u'分值')

    class Meta:
        db_table = 'industry'
        verbose_name_plural = u'行业'

    def __unicode__(self):
        return self.name


class UserIndustry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')

    user = models.ForeignKey(User, verbose_name=u'用户')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        db_table = 'user_industry'
        verbose_name_plural = u'支柱行业'

    def __unicode__(self):
        return self.name


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'企业名')
    locate_x = models.FloatField(verbose_name=u'纬度', null=True, blank=True)
    locate_y = models.FloatField(verbose_name=u'经度', null=True, blank=True)
    scale = models.CharField(max_length=255, verbose_name=u'规模')
    ccc = models.BooleanField(default=False, verbose_name=u'ccc认证')

    area = models.ForeignKey(Area, verbose_name=u'地域')
    score = models.ForeignKey(Score, verbose_name=u'分值')

    class Meta:
        db_table = 'enterprise'
        verbose_name_plural = u'企业'

    def __unicode__(self):
        return self.name



class UserEnterprise(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    enterprise = models.ForeignKey(Enterprise, verbose_name=u'企业')

    class Meta:
        db_table = 'user_enterprise'
        verbose_name_plural = u'监测企业'

    def __unicode__(self):
        return self.enterprise.name



class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'产品')
    score = models.ForeignKey(Score, verbose_name=u'分值')
    industry = models.ManyToManyField(Industry, related_name='industrys', 
        related_query_name='industry', null=True, blank=True, verbose_name=u'行业')

    class Meta:
        db_table = 'product'
        verbose_name_plural = u'产品'

    def __unicode__(self):
        return self.name


class EnterpriseProduct(models.Model):
    alias = models.CharField(max_length=255, verbose_name=u'别名')

    enterprise = models.ForeignKey(Enterprise, verbose_name=u'企业')
    product = models.ForeignKey(Product, verbose_name=u'产品')
    score = models.ForeignKey(Score, verbose_name=u'分值')

    class Meta:
        db_table = 'enterprise_product'
        verbose_name_plural = u'企业产品'

    def __unicode__(self):
        return self.alias


class Metrics(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'指标')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')

    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        db_table = 'metrics'
        verbose_name_plural = u'指标'

    def __unicode__(self):
        return self.name


class MetricsProduct(models.Model):
    weight = models.CharField(max_length=255, verbose_name=u'权重')

    metrics = models.ForeignKey(Metrics, verbose_name=u'指标')
    product = models.ForeignKey(Product, verbose_name=u'产品')

    class Meta:
        db_table = 'metrics_product'
        verbose_name_plural = u'产品指标'

    def __unicode__(self):
        return self.weight
