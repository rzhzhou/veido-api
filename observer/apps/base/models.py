from django.db import models

from uuid import uuid4


class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')
    level = models.IntegerField(verbose_name='等级')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'地域'

    def __unicode__(self):
        return self.name


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name='企业名')

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'企业'

    def __unicode__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')
    code = models.CharField(max_length=5, null=True, blank=True, unique=True, verbose_name='编码')
    level = models.IntegerField(verbose_name='行业层级')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'行业'

    def __unicode__(self):
        return self.name


class Corpus(models.Model):
    riskword = models.TextField(max_length=255, verbose_name='风险语料词')
    invalidword = models.TextField(max_length=255, verbose_name='无效词')

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name='行业'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'语料库'

    def __unicode__(self):
        return str(self.uuid)


class Inspection(models.Model):
    guid = models.CharField(max_length=32, primary_key=True, verbose_name='主键')
    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(blank=True, null=True, verbose_name='网站链接')
    content = models.TextField(verbose_name='正文')
    pubtime = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    level = models.IntegerField(default=0, verbose_name='检验等级')# 0, 默认值; 1 国抽; 2 省抽; 3 市抽;
    qualitied = models.FloatField(default=1.0, verbose_name='合格率')
    unitem = models.TextField(verbose_name='不合格项')
    brand = models.CharField(max_length=255, verbose_name='商标')
    product = models.CharField(max_length=255, verbose_name='产品种类')
    source = models.CharField(max_length=255, verbose_name='信息来源')
    status = models.IntegerField(default=0, verbose_name='状态')  # 0, 默认值 -1, 无效 1 有效

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='抽检地域'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'抽检信息'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class AdministrativePenalties(models.Model):
    guid = models.CharField(max_length=32, primary_key=True, verbose_name='主键')
    title = models.CharField(max_length=255, blank=True, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    pubtime = models.DateTimeField(blank=True, null=True, auto_now=False, verbose_name='发布时间')
    publisher = models.CharField(max_length=255, verbose_name='发布者')
    case_name = models.CharField(max_length=255, verbose_name='案件名称')
    illegal_behavior = models.CharField(max_length=255, verbose_name='违法行为')
    punishment_basis = models.CharField(max_length=255, verbose_name='处罚依据')
    punishment_result = models.CharField(max_length=255, verbose_name='处罚结果')
    penalty_organ = models.CharField(max_length=255, verbose_name='处罚机关')
    credit_code = models.CharField(max_length=255, verbose_name='统一社会信用代码')
    area = models.CharField(max_length=255, verbose_name='地域')
    enterprise = models.CharField(max_length=255, verbose_name='处罚企业')
    industry = models.CharField(max_length=255, verbose_name='行业')

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'行政处罚'

    def __unicode__(self):
        return self.title


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')# 质检热点 质量事件 信息参考 ...
    level = models.BigIntegerField(null=False, verbose_name='等级')
    remark = models.CharField(max_length=255, blank=True, verbose_name='备注')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'文章分类'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    guid = models.CharField(max_length=32, primary_key=True, verbose_name='主键')
    title = models.CharField(max_length=255, blank=True, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    content = models.TextField(blank=True, verbose_name='正文')
    pubtime = models.DateTimeField(auto_now=False, verbose_name='发布时间')
    source = models.CharField(max_length=255, blank=True, verbose_name='信息来源')
    reprinted = models.IntegerField(verbose_name='转载数')
    feeling_factor = models.FloatField(default=-1, verbose_name='正负面')
    score = models.IntegerField(default=0, verbose_name='评分')
    risk_keyword = models.CharField(max_length=255, blank=True, verbose_name='关键词')
    invalid_keyword = models.CharField(
        max_length=255, blank=True, verbose_name='无效关键词')
    status = models.IntegerField(
        default=0, verbose_name='状态')  # 0, 默认值 -1, 无效 1 有效

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = u'文章'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title
