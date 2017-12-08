from django.db import models
from django.contrib.auth.models import User

from observer.apps.base.models import ArticleCategory


class Article(models.Model):
    base_article = models.CharField(max_length=32, verbose_name='基础文章库')

    category = models.ForeignKey(
        'base.ArticleCategory',
        on_delete=models.CASCADE,
        verbose_name='文章类别'
    )

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = '文章'

    def __unicode__(self):
        return self.base_article


class DesignatedMonitoringKeywords(models.Model):
    keywords = models.CharField(max_length=255, verbose_name='关键词')
    remarks = models.TextField(verbose_name='备注信息')
    create_at = models.DateTimeField(verbose_name='创建时间')
    update_at = models.DateTimeField(verbose_name='更新时间')
    status = models.IntegerField(verbose_name='状态')

    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='创建者'
    )

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = '指定监测关键词'


class DesignatedMonitoringLink(models.Model):
    link = models.CharField(max_length=255, verbose_name='网站链接')
    remarks = models.TextField(verbose_name='备注信息')
    create_at = models.DateTimeField(verbose_name='创建时间')
    update_at = models.DateTimeField(verbose_name='更新时间')
    status = models.IntegerField(verbose_name='状态')

    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='创建者'
    )

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = '指定监测链接'
