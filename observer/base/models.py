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


class CCCIndustry(models.Model):
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
        verbose_name_plural = '3C行业'

    def __str__(self):
        return self.name


class LicenseIndustry(models.Model):
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
        verbose_name_plural = '许可证行业'

    def __str__(self):
        return self.name


class AliasIndustry(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='行业名称')
    
    industry_id = models.IntegerField(verbose_name='行业ID')
    ccc_id = models.IntegerField(default=0, blank=True, verbose_name='3C行业ID')
    license_id = models.IntegerField(default=0, blank=True, verbose_name='许可证行业ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '行业别名'

    def __str__(self):
        return self.name


class Inspection(models.Model):
    guid = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='主键')
    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(blank=True, null=True, verbose_name='网站链接')
    pubtime = models.DateField(verbose_name='发布时间')
    source = models.CharField(max_length=80, verbose_name='信息来源')
    unitem = models.CharField(max_length=255, verbose_name='不合格项')
    qualitied = models.FloatField(default=1.0, verbose_name='合格率')
    category = models.CharField(max_length=32, verbose_name='抽查类别')
    level = models.CharField(max_length=2, verbose_name='检验等级') # 国、省、市

    industry_id = models.IntegerField(verbose_name='行业/产品ID')
    area_id = models.IntegerField(verbose_name='地域ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '抽检信息'
        ordering = ['-pubtime']

    def __str__(self):
        return self.title


class Enterprise(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称')

    area_id = models.IntegerField(verbose_name='地域ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '企业'

    def __str__(self):
        return self.title


class InspectionEnterprise(models.Model):
    inspection_id = models.CharField(max_length=32, verbose_name='抽检信息GUID')
    enterpise_id = models.IntegerField(verbose_name='地域ID')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '抽检企业'

    def __str__(self):
        return self.title


class Article(models.Model):
    guid = models.CharField(max_length=32, primary_key=True, editable=False, verbose_name='主键')
    title = models.CharField(max_length=255, blank=True, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    pubtime = models.DateTimeField(auto_now=False, verbose_name='发布时间')
    source = models.CharField(max_length=80, blank=True, verbose_name='信息来源')
    score = models.IntegerField(default=0, verbose_name='风险程度')# 0, 默认值
    risk_keyword = models.CharField(max_length=255, blank=True, verbose_name='关键词')
    invalid_keyword = models.CharField(max_length=255, blank=True, verbose_name='无效关键词')
    status = models.IntegerField(default=0, verbose_name='状态')# 0, 默认值 -1, 无效 1 有效

    class Meta:
        app_label = 'base'
        verbose_name_plural = '文章'
        ordering = ['-pubtime']

    def __str__(self):
        return self.title


class ArticleArea(models.Model):
    article_id = models.CharField(max_length=32, verbose_name='文章GUID')
    area_id = models.IntegerField(verbose_name='地域ID')
    
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
