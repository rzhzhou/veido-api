#coding=utf-8
from django.db import models

from observer.apps.riskmonitor.models import (Industry, Product, Enterprise,
    Metrics)

# Create your models here.
class Corpus(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'语料词')

    industry = models.ForeignKey(Industry, null=True, blank=True, verbose_name=u'行业')
    enterprise = models.ForeignKey(Enterprise, null=True, blank=True, verbose_name=u'企业')
    product = models.ForeignKey(Product, null=True, blank=True, verbose_name=u'产品')
    metrics = models.ForeignKey(Metrics, null=True, blank=True, verbose_name=u'指标')

    class Meta:
            db_table = 'corpus'
            verbose_name_plural = u'语料库'

    def __unicode__(self):
        return self.name