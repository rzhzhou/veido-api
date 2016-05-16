# -*- coding: utf-8 -*-
from django.db import models
from observer.apps.base.models import Area
from observer.apps.riskmonitor.models import Industry, Enterprise


class InspectionPublisher(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'抽检单位')

    class Meta:
        app_label = 'origin'
        db_table = 'origin_inspection_publisher'
        verbose_name_plural = u'抽检单位'

    def __unicode__(self):
        return self.name


class Inspection(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'标题')
    url = models.URLField(blank=True, null=True, verbose_name=u'网站链接')
    content = models.TextField(blank=True, null=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(blank=True, null=True, auto_now=False, verbose_name=u'发布时间')
    samtime = models.DateTimeField(blank=True, null=True, auto_now=False, verbose_name=u'抽检时间')
    publisher = models.ForeignKey(InspectionPublisher, verbose_name=u'抽检单位')
    qualitied = models.FloatField(blank=True, null=True, verbose_name=u'合格率')
    unitem = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'不合格项')
    brand = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'商标')

    area = models.ManyToManyField(Area, related_name='inspections',
        related_query_name='inspection',verbose_name=u'抽检地域')
    industry = models.ManyToManyField(Industry, related_name='inspections',
        related_query_name='inspection', verbose_name=u'行业')
    enterprise = models.ManyToManyField(Enterprise, related_name='inspections',
        related_query_name='inspection', verbose_name=u'企业')

    class Meta:
        app_label = 'origin'
        db_table = 'origin_inspection'
        verbose_name_plural = u'风险抽检'
        ordering = ['-pubtime']
