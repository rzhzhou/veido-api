from django.db import models

from observer.apps.base.models import (ArticleCategory, )


class Inspection(models.Model):
    base_inspection = models.CharField(max_length=32, verbose_name='基础抽检库')
    qualitied = models.FloatField(default=1.0, verbose_name='关注度')

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = '抽检信息'

    def __unicode__(self):
        return self.base_inspection


class Article(models.Model):
    base_article = models.CharField(max_length=32, verbose_name='基础文章库')
    
    category = models.ForeignKey(
        'base.ArticleCategory',
        verbose_name='文章类别'
    )

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = '文章'

    def __unicode__(self):
        return self.base_article