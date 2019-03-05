from django.db import models
from tinymce.models import HTMLField


class Area(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    level = models.IntegerField(verbose_name='等级')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'apps'
        db_table = 'base_area'
        verbose_name_plural = '地域'

    def __str__(self):
        return self.name


class GovReports(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    content = HTMLField(verbose_name='内容')
    year = models.IntegerField(verbose_name='年份')

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name=u'地域'
    )

    class Meta:
        app_label = 'apps'
        db_table = 'base_govreports'
        verbose_name_plural = '政府报告'

    def __str__(self):
        return self.title
