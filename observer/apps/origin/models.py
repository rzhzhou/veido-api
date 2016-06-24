# -*- coding: utf-8 -*-
from django.db import models
from observer.apps.base.models import Area


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'企业名')

    area = models.ForeignKey(Area, verbose_name=u'地域')

    class Meta:
        app_label = 'origin'
        db_table = 'enterprise'
        verbose_name_plural = u'企业'

    def __unicode__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'行业层级')
    parent = models.ForeignKey(
        'self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        app_label = 'origin'
        db_table = 'industry'
        verbose_name_plural = u'行业'

    def __unicode__(self):
        return self.name


class InspectionPublisher(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'抽检单位')

    class Meta:
        app_label = 'origin'
        db_table = 'origin_inspection_publisher'
        verbose_name_plural = u'抽检单位'

    def __unicode__(self):
        return self.name


class Inspection(models.Model):
    title = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=u'标题')
    url = models.URLField(blank=True, null=True, verbose_name=u'网站链接')
    content = models.TextField(blank=True, null=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(
        blank=True, null=True, auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(InspectionPublisher, verbose_name=u'抽检单位')
    qualitied = models.FloatField(blank=True, null=True, verbose_name=u'合格率')
    unitem = models.TextField(blank=True, null=True, verbose_name=u'不合格项')
    brand = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=u'商标')
    product = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=u'产品种类')

    area = models.ManyToManyField(Area, related_name='areas',
                                  related_query_name='area', verbose_name=u'抽检地域')
    industry = models.ManyToManyField(Industry, related_name='industries',
                                      related_query_name='industry', verbose_name=u'行业')
    enterprise_qualified = models.ManyToManyField(Enterprise, related_name='enterprises_qualified',
                                        related_query_name='enterprise_qualified', verbose_name=u'合格企业')
    enterprise_unqualified = models.ManyToManyField(Enterprise, related_name='enterprises_unqualified',
                                        related_query_name='enterprise_unqualified', verbose_name=u'不合格企业')

    class Meta:
        app_label = 'origin'
        db_table = 'origin_inspection'
        verbose_name_plural = u'风险抽检'
        ordering = ['-pubtime']
