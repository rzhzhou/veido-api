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
        app_label = 'hqi'
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
        app_label = 'hqi'
        db_table = 'base_govreports'
        verbose_name_plural = '政府报告'

    def __str__(self):
        return self.title


class Policy(models.Model):
    category = models.CharField(max_length=255, verbose_name='政策类别')
    industry = models.CharField(max_length=255, null=True, verbose_name='产业类别')
    url = models.URLField(verbose_name='网站链接', null=True, default='')
    pubtime = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    name = models.CharField(max_length=255, null=True, verbose_name='政策')


    areas = models.ManyToManyField(Area)

    class Meta:
        app_label = 'hqi'
        db_table = 'base_policy'
        verbose_name_plural = '政府政策'

    def __unicode__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    unit = models.CharField(max_length=255, null=True, blank=True, verbose_name='单位')
    level = models.IntegerField(verbose_name='等级')
    index=models.IntegerField(verbose_name='索引',null=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'hqi'
        db_table = 'base_indicator'
        verbose_name_plural = '指标'

    def __str__(self):
        return self.name


class IndicatorDataParent(models.Model):
    value = models.FloatField(default=0, verbose_name='值')
    year = models.IntegerField(verbose_name='年份')

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name=u'地域'
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        verbose_name='指标'
    )

    class Meta:
        app_label = 'hqi'
        db_table = 'base_indicatordataparent'
        verbose_name_plural = '指标数据'


class IndicatorScore(models.Model):
    value = models.FloatField(default=0, verbose_name='值')
    year = models.IntegerField(verbose_name='年份')

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name=u'地域'
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        verbose_name='指标'
    )

    class Meta:
        app_label = 'hqi'
        db_table = 'base_indicatorscore'
        verbose_name_plural = '指标数据(量化)'