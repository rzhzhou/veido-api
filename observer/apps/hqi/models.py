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
        db_table = 'hqi_area'
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
        db_table = 'hqi_govreports'
        verbose_name_plural = '政府报告'

    def __str__(self):
        return self.title


class Policy(models.Model):
    category = models.CharField(max_length=255, verbose_name='政策类别')
    industry = models.CharField(max_length=255, null=True, verbose_name='产业类别')
    name = models.CharField(max_length=255, null=True, verbose_name='政策')
    detail = models.CharField(max_length=1500, null= True, verbose_name='政策详情')

    class Meta:
        app_label = 'hqi'
        verbose_name_plural = '政府政策'

    def __unicode__(self):
        return self.name


class PolicyArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    pubtime = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    total = models.IntegerField(verbose_name='总计', null=True)
    
    areas = models.ManyToManyField(Area)

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        verbose_name=u'地域链接'
    )

    class Meta:
        app_label = 'hqi'
        verbose_name_plural = '地域链接'

    def __str__(self):
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
        db_table = 'hqi_indicator'
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
        db_table = 'hqi_indicatordataparent'
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
        db_table = 'hqi_indicatorscore'
        verbose_name_plural = '指标数据(量化)'
