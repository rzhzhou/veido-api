# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tinymce.models import HTMLField
from django.db import models

class AdministrativePenalties(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = HTMLField(blank=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    province = models.CharField(max_length=255, verbose_name=u'省')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'市')
    district = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'地域')
    industry = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'行业')
    productCategory=models.CharField(max_length=255, null=True, blank=True, verbose_name=u'产品种类')
    brand = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'商标')
    caseName = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'案件名称')
    penaltyOrgan = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'处罚机关')
    punishedName = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'被处罚者名称')
    punishedDistrict = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'被处罚者所在地')
    illegalBehavior = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'违法行为')
    punishmentBasis = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'处罚依据')
    punishmentRsult = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'处罚结果')

    class Meta:
        app_label = 'penalty'
        db_table = 'administrative_penalties'
        verbose_name_plural = u'行政处罚'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title

