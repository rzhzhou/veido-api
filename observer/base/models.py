import uuid
from django.contrib.auth.models import User
from django.db import models


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
        app_label = 'base'
        verbose_name_plural = '地域'

    def __str__(self):
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
        app_label = 'base'
        verbose_name_plural = '用户地域'

    def __str__(self):
        return self.user.username


class Industry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(max_length=255, blank=True, verbose_name='行业描述')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '行业'

    def __str__(self):
        return self.name


class CPCIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='行业描述'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '产品总分类(CPC)'

    def __str__(self):
        return self.name


class CCCIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='行业描述'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '3C行业'

    def __str__(self):
        return self.name


class LicenceIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='行业描述'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '许可证行业'

    def __str__(self):
        return self.name


class ConsumerIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='行业描述'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '消费品目录'

    def __str__(self):
        return self.name


class MajorIndustry(models.Model):
    id = models.IntegerField(primary_key=True, editable=True, verbose_name='行业编号')
    name = models.CharField(max_length=100, verbose_name='行业名称')
    level = models.IntegerField(verbose_name='行业等级')
    desc = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='行业描述'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    licence = models.ForeignKey(
        LicenceIndustry,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='许可证'
    )

    ccc = models.ForeignKey(
        CCCIndustry,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='CCC'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '重点产品目录'

    def __str__(self):
        return self.name


class AliasIndustry(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='行业名称')

    industry_id = models.IntegerField(verbose_name='行业ID')
    ccc_id = models.IntegerField(default=0, blank=True, verbose_name='3C行业ID')
    licence_id = models.IntegerField(default=0, blank=True, verbose_name='许可证行业ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '行业别名'

    def __str__(self):
        return self.name


class Corpus(models.Model):
    riskword = models.CharField(default=0, max_length=255, verbose_name='风险语料词')
    status = models.IntegerField(default=0, verbose_name='状态') # 默认值 0 :不执行爬虫, 1 ： 执行爬虫

    industry_id = models.IntegerField(default=0, verbose_name='产品类别')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '语料库'

class Corpus_categories(models.Model):
    keyword = models.CharField(default=0, max_length=255, verbose_name='关键词语料词')
    status = models.IntegerField(default=0, verbose_name='状态') # 默认值 0 :不执行爬虫, 1 ： 执行爬虫
    category_id = models.CharField(max_length=5, verbose_name='信息类别')
    
    class Meta:
        app_label = 'base'
        verbose_name_plural = '语料库-信息类别'


class Inspection(models.Model):
    guid = models.CharField(default=None, blank=True, null=True, max_length=32, verbose_name='GUID') # url + industry_id -> md5
    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(blank=True, null=True, verbose_name='网站链接')
    pubtime = models.DateField(verbose_name='发布时间')
    source = models.CharField(max_length=80, verbose_name='信息来源')
    qualitied = models.FloatField(default=1.0, verbose_name='合格率')
    unqualitied_patch = models.IntegerField(default=0, verbose_name="不合格批次")
    qualitied_patch = models.IntegerField(default=0, verbose_name="合格批次")
    inspect_patch = models.IntegerField(default=0, verbose_name="抽查批次")
    category = models.CharField(max_length=32, verbose_name='抽查类别')
    level = models.CharField(max_length=2, verbose_name='检验等级') # 国、省、市
    status = models.IntegerField(default=0, verbose_name='状态')# 0, 未审核(默认值) 1, 已审核 2, 已爬取

    industry_id = models.IntegerField(verbose_name='产品类别')
    product_name = models.CharField(blank=True, null=True, max_length=255, verbose_name='产品名称')
    area_id = models.IntegerField(verbose_name='地域ID')
    origin_product = models.CharField(blank=True, null=True, max_length=255, verbose_name='导入产品名')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '抽检信息'
        ordering = ['-pubtime']

    def __str__(self):
        return self.title


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')
    unitem = models.CharField(max_length=255, verbose_name='不合格项')

    area_id = models.IntegerField(verbose_name='地域ID')
    status = models.IntegerField(default=1, verbose_name='状态')# 0, 未审核(默认值)  1, 已审核

    class Meta:
        app_label = 'base'
        verbose_name_plural = '企业'


class InspectionEnterprise(models.Model):
    inspection_id = models.CharField(max_length=32, verbose_name='抽检信息GUID')
    enterprise_id = models.IntegerField(verbose_name='企业ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '抽检企业'

    def __str__(self):
        return self.inspection_id


class Article(models.Model):
    guid = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='主键')# url -> md5
    title = models.CharField(max_length=255, blank=True, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    pubtime = models.DateTimeField(auto_now=False, verbose_name='发布时间')
    source = models.CharField(max_length=80, blank=True, verbose_name='信息来源')
    score = models.IntegerField(default=0, verbose_name='风险程度')# 0, 默认值
    status = models.IntegerField(default=0, verbose_name='状态')# 0, 默认值 1 有效
    industry_id = models.IntegerField(default=0, verbose_name='产品类别')
    corpus_id = models.IntegerField(default=0, verbose_name='语料词编号')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '文章'
        ordering = ['-pubtime']

    def __str__(self):
        return self.title


class ArticleArea(models.Model):
    article_id = models.CharField(max_length=32, verbose_name='文章GUID')
    area_id = models.BigIntegerField(verbose_name='地域ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '文章地域'


class Category(models.Model):
    id = models.CharField(max_length=5, primary_key=True, editable=True, verbose_name='类别ID')
    name = models.CharField(max_length=10, verbose_name='名称')
    level = models.IntegerField(verbose_name='等级')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '类别'

    def __str__(self):
        return self.name


class ArticleCategory(models.Model):
    article_id = models.CharField(max_length=32, verbose_name='文章GUID')
    category_id = models.CharField(max_length=5, verbose_name='信息类别')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '文章类别'


class DMLink(models.Model):
    name = models.CharField(max_length=32, verbose_name='网站名')
    link = models.URLField(verbose_name='网站链接')
    kwords = models.CharField(max_length=255, verbose_name='关键词')
    fwords = models.CharField(max_length=255, verbose_name='过滤词')
    remarks = models.CharField(max_length=255, verbose_name='备注信息')
    create_at = models.DateTimeField(verbose_name='创建时间')
    update_at = models.DateTimeField(verbose_name='更新时间')
    status = models.IntegerField(verbose_name='状态') # 0：待执行；1：执行中；2：完成

    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='创建者'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '指定监测-链接'

    def __unicode__(self):
        return self.link


class IndustryProducts(models.Model):
    name = models.CharField(max_length=100, verbose_name='产品名称')
    industry_id = models.IntegerField(verbose_name='产品行业编号')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '行业产品'

    def __str__(self):
        return self.name


class Nav(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    href = models.CharField(default=0, max_length=50, verbose_name='链接')
    level = models.IntegerField(verbose_name='等级')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '导航栏'

    def __str__(self):
        return self.name


class UserNav(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    nav = models.ForeignKey(
        Nav,
        on_delete=models.CASCADE,
        verbose_name='导航'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '用户导航栏'

    def __str__(self):
        return self.user.username
