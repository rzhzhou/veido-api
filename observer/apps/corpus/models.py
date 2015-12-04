#coding=utf-8
from django.db import models

from observer.apps.riskmonitor.models import (Industry, Product, Enterprise,
    Metrics)

# Create your models here.
class RiskWord(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'风险语料词')

    class Meta:
        db_table = 'riskword'
        verbose_name_plural=u'风险语料'

    def __unicode__(self):
        return self.name

class Corpus(models.Model):
    riskword = models.ForeignKey(RiskWord, null=True, blank=True, verbose_name=u'风险语料词')
    industry = models.ForeignKey(Industry, null=True, blank=True, verbose_name=u'行业')

    class Meta:
            db_table = 'corpus'
            verbose_name_plural = u'语料库'

    def __unicode__(self):
        return self.riskword.name