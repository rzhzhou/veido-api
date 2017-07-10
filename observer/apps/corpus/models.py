#coding=utf-8
import uuid

from django.db import models

from observer.apps.origin.models import Industry


class Corpus(models.Model):
    uuid = models.CharField(max_length=255, default=uuid.uuid4, verbose_name=u'uuid')
    riskword = models.TextField(max_length=255, default=u'', verbose_name=u'风险语料词')
    invalidword = models.TextField(max_length=255, default=u'', verbose_name=u'无效词')

    industry = models.ForeignKey(
        Industry,
        verbose_name=u'行业'
        )

    class Meta:
        app_label = 'corpus'
        verbose_name_plural = u'语料库'

    def __unicode__(self):
        return str(self.uuid)

