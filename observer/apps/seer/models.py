# -*- coding: utf-8 -*-
import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from observer.apps.base.models import Area, Enterprise, Industry
from observer.utils.fulltext import SearchManager

A_CHOICES = (
    (1, u'低'),
    (2, u'中'),
    (3, u'高'),
)

B_CHOICES = (
    (0, u'否'),
    (1, u'是'),
)

C_CHOICES = (
    (0, u'无'),
    (1, u'有'),
)

class AreaIndustry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    status = models.CharField(max_length=255, default=u'', verbose_name=u'状态')

    area = models.ForeignKey(
        Area,
        verbose_name=u'地域'
    )
    industry = models.ForeignKey(
        Industry,
        verbose_name=u'行业'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'地域行业'

    def __unicode__(self):
        return self.name


class UserArea(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    area = models.ForeignKey(Area, verbose_name=u'地域')

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'用户地域弱关联'

    def __unicode__(self):
        return self.user.username


class ConsumeIndex(models.Model):
    force = models.IntegerField(
        choices=C_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'国家强制性要求'
    )
    close = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'密切程度'
    )
    consume = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'涉及特定消费群体和特殊要求'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u'年度'
    )

    industry = models.ForeignKey(
        Industry,
        verbose_name=u'行业'
    )
    area = models.ForeignKey(
        Area,
        default=1,
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'消费指标(维)'


class SocietyIndex(models.Model):
    trade = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'贸易量'
    )
    qualified = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'抽检合格率'
    )
    accident = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'案例发生状况'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u'年度'
    )

    industry = models.ForeignKey(
        Industry,
        verbose_name=u'行业'
    )
    area = models.ForeignKey(
        Area,
        default=1,
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'社会性指标(维)'


class ManageIndex(models.Model):
    licence = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'列入许可证目录'
    )
    productauth = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'列入产品认证目录'
    )
    encourage = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'是否鼓励'
    )
    limit = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'是否限制'
    )
    remove = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name=u'是否淘汰'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u'年度'
    )

    industry = models.ForeignKey(
        Industry,
        verbose_name=u'行业'
    )
    area = models.ForeignKey(
        Area,
        default=1, 
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'管理指标(维)'


class Cache(models.Model):
    k = models.CharField(max_length=255, verbose_name=u'键')
    v = models.TextField(blank=True, verbose_name=u'值')
    update_at = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'缓存'

    def __unicode__(self):
        return self.k


class CacheConf(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    days = models.IntegerField(verbose_name=u'间隔天数')
    params = models.TextField(blank=True, verbose_name=u'参数')

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'缓存配置'

    def __unicode__(self):
        return self.name


class ModelWeight(models.Model):
    consume_index = models.FloatField(verbose_name=u'消费指标(维)')
    society_index = models.FloatField(verbose_name=u'社会性指标(维)')
    manage_index = models.FloatField(verbose_name=u'管理指标(维)')
    risk_news_index = models.FloatField(verbose_name=u'新闻指标(维)')
    inspection_index = models.FloatField(verbose_name=u'抽检指标(维)')

    industry = models.ForeignKey(
        Industry, 
        null=True, blank=True,
        verbose_name=u'行业'
    )
    area = models.ForeignKey(
        Area,
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'模型权重'

    def __unicode__(self):
        return self.area.name


class RiskEnterprise(models.Model):
    product_name = models.CharField(max_length=255, blank=True, verbose_name=u'风险产品名称')
    issues = models.CharField(max_length=255, blank=True, verbose_name=u'风险事项')

    enterprise = models.ForeignKey(
        Enterprise,
        verbose_name=u'企业名称'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'企业风险'

    def __unicode__(self):
        return self.enterprise.name + ' , ' + product_name

class IndustryScore(models.Model):
    score = models.BigIntegerField(verbose_name=u'分值')
    time = models.DateField(verbose_name=u'日期')

    industry = models.ForeignKey(
        Industry, 
        verbose_name=u'行业'
    )
    area = models.ForeignKey(
        Area, 
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'origin'
        verbose_name_plural = u'行业分值'

    def __unicode__(self):
        return self.industry.name 

