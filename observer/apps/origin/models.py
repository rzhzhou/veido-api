# -*- coding: utf-8 -*-
from django.db import models
from observer.apps.base.models import Area
from observer.apps.riskmonitor.models import Industry, Enterprise


class InspectionPublisher(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'发布者')

    class Meta:
        app_label = 'origin'
        db_table = 'origin_inspection_publisher'
        verbose_name_plural = u'抽检发布者'

    def __unicode__(self):
        return self.name


class Inspection(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'作者')
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, null=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(InspectionPublisher, verbose_name=u'文章发布者')
    qualitied = models.FloatField(verbose_name=u'合格率')
    reprinted = models.IntegerField(verbose_name=u'转载数', default=0)

    area = models.ManyToManyField(Area, related_name='inspections',
        related_query_name='inspection',verbose_name=u'地域')
    industry = models.ManyToManyField(Industry, related_name='inspections',
        related_query_name='inspection', verbose_name=u'行业')
    enterprise = models.ManyToManyField(Enterprise, related_name='inspections',
        related_query_name='inspection', verbose_name=u'企业')

    class Meta:
        app_label = 'origin'
        db_table = 'origin_inspection'
        verbose_name_plural = u'风险抽检'
        ordering = ['-pubtime']
