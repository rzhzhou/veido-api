import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from observer.apps.base.models import Area, Enterprise, Industry
from observer.utils.fulltext import SearchManager

A_CHOICES = (
    (1, u'低'),
    (2, u'中'),
    (3, u'高'),
)

B_CHOICES = (
    (0, u'否'),
    (1, u'是'),
)

C_CHOICES = (
    (0, u'无'),
    (1, u'有'),
)

class AreaIndustry(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')
    status = models.CharField(max_length=255, default='', verbose_name='状态')

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name='行业'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'地域行业'

    def __unicode__(self):
        return self.name


class UserArea(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name='用户'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE, 
        verbose_name='地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'用户地域弱关联'

    def __unicode__(self):
        return self.user.username


class ConsumeIndex(models.Model):
    force = models.IntegerField(
        choices=C_CHOICES,
        blank=True,
        null=True,
        verbose_name='国家强制性要求'
    )
    close = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name='密切程度'
    )
    consume = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name='涉及特定消费群体和特殊要求'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='年度'
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name='行业'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        default=1,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'消费指标(维)'


class SocietyIndex(models.Model):
    trade = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name='贸易量'
    )
    qualified = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name='抽检合格率'
    )
    accident = models.IntegerField(
        choices=A_CHOICES,
        blank=True,
        null=True,
        verbose_name='案例发生状况'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='年度'
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name='行业'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        default=1,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'社会性指标(维)'


class ManageIndex(models.Model):
    licence = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name='列入许可证目录'
    )
    productauth = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name='列入产品认证目录'
    )
    encourage = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name='是否鼓励'
    )
    limit = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name='是否限制'
    )
    remove = models.IntegerField(
        choices=B_CHOICES,
        blank=True,
        null=True,
        verbose_name='是否淘汰'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='年度'
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name='行业'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        default=1, 
        verbose_name='地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'管理指标(维)'


class Cache(models.Model):
    k = models.CharField(max_length=255, verbose_name='键')
    v = models.TextField(blank=True, verbose_name='值')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'缓存'

    def __unicode__(self):
        return self.k


class CacheConf(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')
    days = models.IntegerField(verbose_name='间隔天数')
    params = models.TextField(blank=True, verbose_name='参数')

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'缓存配置'

    def __unicode__(self):
        return self.name


class ModelWeight(models.Model):
    consume_index = models.FloatField(verbose_name='消费指标(维)')
    society_index = models.FloatField(verbose_name='社会性指标(维)')
    manage_index = models.FloatField(verbose_name='管理指标(维)')
    risk_news_index = models.FloatField(verbose_name='新闻指标(维)')
    inspection_index = models.FloatField(verbose_name='抽检指标(维)')

    industry = models.ForeignKey(
        Industry, 
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='行业'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'模型权重'

    def __unicode__(self):
        return self.area.name


class RiskEnterprise(models.Model):
    product_name = models.CharField(max_length=255, blank=True, verbose_name='风险产品名称')
    issues = models.CharField(max_length=255, blank=True, verbose_name='风险事项')

    enterprise = models.ForeignKey(
        Enterprise,
        on_delete=models.CASCADE,
        verbose_name='企业名称'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'企业风险'

    def __unicode__(self):
        return self.enterprise.name + ' , ' + product_name


class IndustryScore(models.Model):
    score = models.BigIntegerField(verbose_name='分值')
    time = models.DateField(verbose_name='日期')

    industry = models.ForeignKey(
        Industry, 
        on_delete=models.CASCADE,
        verbose_name='行业'
    )
    area = models.ForeignKey(
        Area, 
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'origin'
        verbose_name_plural = u'行业分值'

    def __unicode__(self):
        return self.industry.name 



class Inspection(models.Model):
    base_inspection = models.CharField(max_length=32, verbose_name='基础抽检库')

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='行业'
    )
    enterprise_qualified = models.ForeignKey(
        Enterprise,
        on_delete=models.CASCADE,
        related_name='qualitieds',
        null=True, blank=True,
        verbose_name='合格企业'
    )
    enterprise_unqualified = models.ForeignKey(
        Enterprise,
        on_delete=models.CASCADE,
        related_name='unqualifieds', 
        null=True, blank=True,
        verbose_name='不合格企业'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'抽检信息'

    def __unicode__(self):
        return self.base_inspection


class Article(models.Model):
    base_article = models.CharField(max_length=32, verbose_name='基础文章库')

    category = models.ForeignKey(
        'base.ArticleCategory',
        on_delete=models.CASCADE,
        related_name='seer_category',
        verbose_name='文章类别'
    )
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='行业'
    )
    enterprise = models.ForeignKey(
        Enterprise,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='企业'
    )

    class Meta:
        app_label = 'seer'
        verbose_name_plural = u'文章'

    def __unicode__(self):
        return self.base_article