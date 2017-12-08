from django.db import models

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
