# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from observer.apps.base.models import Area, Group


class Brand(models.Model):
    zh_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'中文名称')
    en_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'英文名称')
    logo = models.URLField(verbose_name=u'图标')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'brand'
        verbose_name_plural = u'品牌'

    def __unicode__(self):
        return self.en_name+self.zh_name


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'企业名')

    area = models.ForeignKey(Area, verbose_name=u'地域')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'enterprise'
        verbose_name_plural = u'企业'

    def __unicode__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'行业层级')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'industry'
        verbose_name_plural = u'行业'

    def __unicode__(self):
        return self.name


class Metrics(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'指标')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')

    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'metrics'
        verbose_name_plural = u'指标'

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'生产产品')

    enterprise = models.ForeignKey(Enterprise, null=True, blank=True, verbose_name=u'企业')
    industry = models.ForeignKey(Industry, null=True, blank=True, verbose_name=u'产品')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'product'
        verbose_name_plural = u'生产产品'

    def __unicode__(self):
        return self.name


class ProductMetrics(models.Model):
    weight = models.CharField(max_length=255, verbose_name=u'权重')

    metrics = models.ForeignKey(Metrics, verbose_name=u'指标')
    product = models.ForeignKey(Product, verbose_name=u'产品')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'metrics_product'
        verbose_name_plural = u'产品指标'

    def __unicode__(self):
        return self.weight


class RiskData(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'作者链接地址')
    user_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'作者名')
    content = models.TextField(blank=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name=u'发布时间')
    comment = models.CharField(max_length=255, verbose_name=u'是否自营')
    comment_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'评论地址')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    show_pic = models.TextField( null=True, blank=True, verbose_name=u'图片评论图')
    score = models.IntegerField(null=True, blank=True, verbose_name=u'评分')
    url = models.URLField( null=True, blank=True, verbose_name=u'网站链接')
    uuid = models.CharField(max_length=255, default=uuid.uuid4, verbose_name=u'uuid')

    area = models.ForeignKey(Area, verbose_name=u'地域')
    brand = models.ForeignKey(Brand, verbose_name=u'品牌')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'risk_data'
        verbose_name_plural = u'电商风险评论'

    def __unicode__(self):
        return self.source


class ScoreIndustry(models.Model):
    score = models.IntegerField(default=0, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', default=timezone.now)
    increment = models.IntegerField(default=0, verbose_name=u'增量')
    reducescore = models.IntegerField(default=0, verbose_name=u'所减的分数')

    industry = models.ForeignKey(Industry, null=True, verbose_name=u'行业')
    user = models.ForeignKey(User, null=True, verbose_name=u'用户')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'score_industry'
        verbose_name_plural = u'行业分值'

    def __unicode__(self):
        return self.score


class ScoreEnterprise(models.Model):
    score = models.IntegerField(default=0, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', default=timezone.now)
    increment = models.IntegerField(default=0, verbose_name=u'增量')
    reducescore = models.IntegerField(default=0, verbose_name=u'所减的分数')

    enterprise = models.ForeignKey(Enterprise, verbose_name=u'企业')
    user = models.ForeignKey(User, null=True, verbose_name=u'用户')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'score_enterprise'
        verbose_name_plural = u'企业分值'

    def __unicode__(self):
        return self.score


class ScoreProduct(models.Model):
    score = models.CharField(max_length=255, verbose_name=u'分值')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间', default=timezone.now)

    product = models.ForeignKey(Product, verbose_name=u'产品')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'score_product'
        verbose_name_plural = u'产品分值'

    def __unicode__(self):
        return self.score


class UserEnterprise(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    enterprise = models.ForeignKey(Enterprise, verbose_name=u'企业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'user_enterprise'
        verbose_name_plural = u'监测企业'

    def __unicode__(self):
        return self.enterprise.name


class UserIndustry(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')

    user = models.ForeignKey(User, verbose_name=u'用户')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'user_industry'
        verbose_name_plural = u'支柱行业'

    def __unicode__(self):
        return self.name


class RiskNewsPublisher(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'发布者')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'risk_news_publisher'
        verbose_name_plural = u'风险新闻发布者'

    def __unicode__(self):
        return self.name


class RiskKeyword(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'关键词')

    class Meta:
        db_table = 'risk_keyword'
        verbose_name_plural = u'风险新闻关键词'

    def __unicode__(self):
        return self.name


class RiskNews(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = HTMLField(blank=True, verbose_name=u'正文')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(RiskNewsPublisher, verbose_name=u'文章发布者')
    reprinted = models.IntegerField(verbose_name=u'转载数')

    area = models.ManyToManyField(Area, related_name='rareas',
        related_query_name='rarea',verbose_name=u'地域')
    industry = models.ManyToManyField(Industry, related_name='industrys',
        related_query_name='industry', verbose_name=u'行业')
    enterprise = models.ManyToManyField(Enterprise, related_name='enterprises',
        related_query_name='enterprise', verbose_name=u'企业')

    risk_keyword = models.ForeignKey(RiskKeyword, null= True, blank=True,
        default=u'', verbose_name= u'风险新闻关键词')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'risk_news'
        verbose_name_plural = u'风险新闻'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class ProductKeyword(models.Model):
    newkeyword = models.CharField(max_length=255, verbose_name=u'关键词')
    review = models.CharField(max_length=255, default=u'', verbose_name=u'审核')
    # synced = models.CharField(max_length=255, default=u'', verbose_name=u'同步')
    group = models.ForeignKey(Group)
    product = models.ForeignKey(Product, null=True, blank=True, default=u'')

    class Meta:
        db_table = 'product_keyword'
        verbose_name_plural = u'产品监测关键词'

    def __unicode__(self):
        return self.newkeyword


class UserArea(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    area = models.ForeignKey(Area, verbose_name=u'地域')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'user_area'
        verbose_name_plural = u'用户地域弱关联'

    def __unicode__(self):
        return self.user.username


class ManageIndex(models.Model):
    licence = models.BooleanField(default=False, verbose_name=u'列入许可证目录')
    productauth = models.BooleanField(default=False, verbose_name=u'列入产品认证目录')
    policy = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'产业政策')
    year = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'年度')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'manage_index'
        verbose_name_plural = u'管理指标(维)'

    def __unicode__(self):
        return licence


class SocietyIndex(models.Model):
    trade = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'贸易量')
    qualified = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'抽检合格率')
    accident = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'案例发生状况')
    year = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'年度')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'society_index'
        verbose_name_plural = u'社会性指标(维)'

    def __unicode__(self):
        return trade


class ConsumeIndex(models.Model):
    force = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'国家强制性要求')
    close = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'密切程度')
    consume = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'涉及特定消费群体和特殊要求')
    year = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'年度')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'consume_index'
        verbose_name_plural = u'消费指标(维)'

    def __unicode__(self):
        return close


class MultiDimension(models.Model):
    manage = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'管理纬')
    society = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'社会影响纬')
    consume = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'民生相关纬')
    news = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'互联网信息纬')
    inspection = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=u'抽检纬')
    industry = models.ForeignKey(Industry, verbose_name=u'行业')

    class Meta:
        app_label = 'riskmonitor'
        db_table = 'multi_dimension'
        verbose_name_plural = u'多维表'

    def __unicode__(self):
        return manage