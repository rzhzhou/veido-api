#coding=utf-8
import uuid

from django.db import models

from observer.apps.riskmonitor.models import (Industry, Product, Enterprise,
    Metrics)


class Corpus(models.Model):
    uuid = models.CharField(max_length=255, default=uuid.uuid4, verbose_name=u'uuid')
    riskword = models.TextField(max_length=255, null=True, blank=True, verbose_name=u'风险语料词')
    invalidword = models.TextField(max_length=255, null=True, blank=True, verbose_name=u'无效词')
    industry = models.ForeignKey(Industry, null=True, blank=True, verbose_name=u'行业')

    class Meta:
        app_label = 'corpus'
        db_table = 'corpus'
        verbose_name_plural = u'语料库'

    def __unicode__(self):
        return str(self.uuid)


class Event(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    class Meta:
            app_label = 'corpus'
            db_table = 'event'
            verbose_name_plural = u'聚类事件'

    def __unicode__(self):
        return self.title
