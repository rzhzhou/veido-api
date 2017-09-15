# -*- coding: utf-8 -*-
from django.db import models

from uuid import uuid4

class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')
    
    parent = models.ForeignKey(
        'self', 
        null=True, blank=True, 
        verbose_name=u'上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'地域'

    def __unicode__(self):
        return self.name


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'企业名')
    
    area = models.ForeignKey(
        Area, 
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'企业'

    def __unicode__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    code = models.CharField(max_length=5, null=True, blank=True, unique=True, verbose_name=u'编码')
    level = models.BigIntegerField(null=False, verbose_name=u'行业层级')

    parent = models.ForeignKey(
        'self', 
        null=True, blank=True, 
        verbose_name=u'上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'行业'

    def __unicode__(self):
        return self.name


class Corpus(models.Model):
    riskword = models.TextField(max_length=255, default=u'', verbose_name=u'风险语料词')
    invalidword = models.TextField(max_length=255, default=u'', verbose_name=u'无效词')

    industry = models.ForeignKey(
        Industry,
        verbose_name=u'行业'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'语料库'

    def __unicode__(self):
        return str(self.uuid)


class Inspection(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'标题')
    url = models.URLField(blank=True, null=True, verbose_name=u'网站链接')
    pubtime = models.DateTimeField(blank=True, null=True, verbose_name=u'发布时间')
    qualitied = models.FloatField(default=1.0, verbose_name=u'合格率')
    unitem = models.TextField(default=u'', verbose_name=u'不合格项')
    brand = models.CharField(max_length=255, default=u'', verbose_name=u'商标')
    product = models.CharField(max_length=255, default=u'', verbose_name=u'产品种类')
    publisher = models.CharField(max_length=255, verbose_name=u'抽检单位')

    area = models.ForeignKey(
        Area,
        verbose_name=u'抽检地域'
    )

    industry = models.ForeignKey(
        Industry,
        null=True, blank=True,
        verbose_name=u'行业'
    )

    enterprise_qualified = models.ForeignKey(
        Enterprise,
        related_name='qualitieds',
        null=True, blank=True,
        verbose_name=u'合格企业'
    )

    enterprise_unqualified = models.ForeignKey(
        Enterprise,
        related_name='unqualifieds', 
        null=True, blank=True,
        verbose_name=u'不合格企业'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'风险抽检'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class AdministrativePenalties(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    pubtime = models.DateTimeField(blank=True, null=True, auto_now=False, verbose_name=u'发布时间')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    case_name = models.CharField(max_length=255, default=u'', verbose_name=u'案件名称')
    illegal_behavior = models.CharField(max_length=255, default=u'', verbose_name=u'违法行为')
    punishment_basis = models.CharField(max_length=255, default=u'', verbose_name=u'处罚依据')
    punishment_result = models.CharField(max_length=255, default=u'', verbose_name=u'处罚结果')
    penalty_organ = models.CharField(max_length=255, verbose_name=u'处罚机关')
    credit_code = models.CharField(max_length=255, default=u'', verbose_name=u'统一社会信用代码')
    area = models.CharField(max_length=255, default=u'', verbose_name=u'地域')
    enterprise = models.CharField(max_length=255, default=u'', verbose_name=u'处罚企业')
    industry = models.CharField(max_length=255, default=u'', verbose_name=u'行业')

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'行政处罚'

    def __unicode__(self):
        return self.title


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')
    remark = models.CharField(max_length=255, blank=True, verbose_name=u'备注')

    parent = models.ForeignKey(
        'self', 
        null=True, blank=True, 
        verbose_name=u'上一级'
    )
    class Meta:
        app_label = 'base'
        verbose_name_plural = u'文章分类'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    reprinted = models.IntegerField(verbose_name=u'转载数')
    feeling_factor = models.FloatField(default=-1, verbose_name=u'正负面')
    score = models.IntegerField(default=0, verbose_name=u'评分')
    risk_keyword = models.CharField(max_length=255, blank=True, verbose_name=u'关键词')
    invalid_keyword = models.CharField(max_length=255, blank=True, verbose_name=u'无效关键词')
    status = models.IntegerField(default=0, verbose_name=u'状态') # 0, 默认值 -1, 无效新闻 1 有效新闻

    category = models.ForeignKey(
        ArticleCategory,
        verbose_name=u'文章类别'
    )
    area = models.ForeignKey(
        Area,
        verbose_name=u'地域'
    )
    industry = models.ForeignKey(
        Industry,
        null=True, blank=True,
        verbose_name=u'行业'
    )
    enterprise = models.ForeignKey(
        Enterprise,
        null=True, blank=True,
        verbose_name=u'企业'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'文章'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


