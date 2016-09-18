# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tinymce.models import HTMLField
from django.db import models

# Create your models here.


class RawInspection(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = HTMLField(blank=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')

    class Meta:
        app_label = 'inspection'
        verbose_name_plural = u'原始风险抽检'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title
