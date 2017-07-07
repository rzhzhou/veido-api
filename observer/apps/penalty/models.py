# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tinymce.models import HTMLField
from django.db import models


class AdministrativePenalties(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = HTMLField(blank=True, verbose_name=u'正文')
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
        app_label = 'penalty'
        verbose_name_plural = u'行政处罚'

    def __unicode__(self):
        return self.title
