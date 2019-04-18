import uuid
import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from observer.settings.development import UPLOAD_URL
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
        app_label = 'base'
        verbose_name_plural = '地域'

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    theme = models.CharField(default='', max_length=50, verbose_name='主题')
    logo = models.CharField(default='', max_length=50, verbose_name='logo')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '用户信息'

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
        verbose_name='强制认证'
    )
    consumer = models.ForeignKey(
        ConsumerIndustry,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='消费品'
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


class CorpusCategories(models.Model):
    keyword = models.CharField(default=0, max_length=255, verbose_name='关键词语料词')
    status = models.IntegerField(default=0, verbose_name='状态') # 默认值 0 :未执行爬虫, 1 ： 已执行爬虫， 2：已停止并删除爬虫（但保留关键词来显示新闻关联来源）
    category_id = models.CharField(max_length=5, verbose_name='信息类别')
    industry_id = models.IntegerField(default=0, verbose_name='产品类别')
    startTime = models.DateField(null=True, verbose_name='开始时间')
    stopTime = models.DateField(null=True, verbose_name='结束时间')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '语料库-信息类别'


class Enterprise(models.Model):
    STATUS_CHOICES = (
        ('1', '已审核'),
        ('0', '未审核'),
    )

    name = models.CharField(max_length=255, verbose_name='名称')
    unitem = models.CharField(max_length=255, verbose_name='不合格项')

    status = models.IntegerField(
        default=0,
        choices=STATUS_CHOICES,
        verbose_name='状态',
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '企业'


class Inspection(models.Model):
    INSPECTION_LEVEL_CHOICES = (
        ('2', '国'),
        ('1', '省'),
        ('0', '市'),
    )
    STATUS_CHOICES = (
        ('2', '已爬取'),
        ('1', '已审核'),
        ('0', '未审核'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    pubtime = models.DateField(verbose_name='发布时间')
    source = models.CharField(max_length=255, verbose_name='信息来源')
    origin_product = models.CharField(blank=True, null=True, max_length=255, verbose_name='导入产品名')
    product_name = models.CharField(max_length=255, verbose_name='产品名称')
    qualitied = models.FloatField(default=1.0, verbose_name='合格率')
    unqualitied_patch = models.IntegerField(default=0, verbose_name="不合格批次")
    qualitied_patch = models.IntegerField(default=0, verbose_name="合格批次")
    inspect_patch = models.IntegerField(default=0, verbose_name="抽查批次")
    category = models.CharField(max_length=32, verbose_name='抽查类别')

    level = models.IntegerField(
        default=0,
        choices=INSPECTION_LEVEL_CHOICES,
        verbose_name='检验等级',
    )
    status = models.IntegerField(
        default=0,
        choices=STATUS_CHOICES,
        verbose_name='状态',
    )

    industry = models.ForeignKey(
        MajorIndustry,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='产品类别'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='地域'
    )

    enterprises = models.ManyToManyField(Enterprise)

    class Meta:
        app_label = 'base'
        verbose_name_plural = '抽检信息'
        ordering = ['-pubtime']

    def __str__(self):
        return self.title


class Category(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=True, verbose_name='类别ID')
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


class Article(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='标题')
    url = models.URLField(verbose_name='网站链接')
    pubtime = models.DateTimeField(auto_now=False, verbose_name='发布时间')
    source = models.CharField(max_length=80, blank=True, verbose_name='信息来源')
    score = models.IntegerField(default=0, verbose_name='风险程度')# 0, 默认值
    status = models.IntegerField(default=0, verbose_name='状态')# 0, 默认值 1 有效
    sentiment = models.IntegerField(null=True, verbose_name='情感属性')# 0:负面，1:中性，2:正面

    industry = models.ForeignKey(
        MajorIndustry,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='产品类别'
    )
    corpus = models.ForeignKey(
        CorpusCategories,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='语料词'
    )
    user = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )

    areas = models.ManyToManyField(Area)
    categories = models.ManyToManyField(Category)

    class Meta:
        app_label = 'base'
        verbose_name_plural = '文章'
        ordering = ['-pubtime']

    def __str__(self):
        return self.title


class Harm(models.Model):
    environment = models.IntegerField(null=True, verbose_name='发生时环境')
    activity = models.IntegerField(null=True, verbose_name='进行的活动')
    mind_body = models.IntegerField(null=True, verbose_name='心里和生理因素')
    behavior = models.IntegerField(null=True, verbose_name='行为')
    indoor = models.IntegerField(null=True, verbose_name='室内环境')
    outdoor = models.IntegerField(null=True, verbose_name='室外环境')
    physics = models.IntegerField(null=True, verbose_name='物理危害')
    chemical = models.IntegerField(null=True, verbose_name='化学危害')
    biology = models.IntegerField(null=True, verbose_name='生物危害')
    damage_types = models.IntegerField(null=True, verbose_name='伤害类型')
    damage_degree = models.IntegerField(null=True, verbose_name='伤害程度')
    damage_reason = models.IntegerField(null=True, verbose_name='伤害原因')

    article = models.OneToOneField(
        Article,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='文章'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '风险伤害'



class HarmPeople(models.Model):
    age = models.IntegerField(null=True, verbose_name='年龄')
    sex = models.IntegerField(null=True, verbose_name='性别')

    harm = models.ForeignKey(
        Harm,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='风险伤害'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '伤害涉及者'


class HarmIndicator(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    desc = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='定义'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '风险伤害'


class Events(models.Model):
    title = models.CharField(max_length=100, verbose_name='名称')
    socialHarm = models.CharField(max_length=50, verbose_name='社会危害程度')
    scope = models.CharField(max_length=50, verbose_name='影响范围')
    grading = models.CharField(max_length=50, verbose_name='分级')
    pubtime = models.DateField(default=datetime.date.today, verbose_name='发布时间')
    desc = models.TextField(null=True, verbose_name='事件总结')

    articles = models.ManyToManyField(Article)

    class Meta:
        app_label = 'base'
        verbose_name_plural = '事件分析'


class EventsKeyword(models.Model):
    name = models.CharField(max_length=100, verbose_name='关键词名')

    events = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='事件'
    )

    articles = models.ManyToManyField(Article)

    class Meta:
        app_label = 'base'
        verbose_name_plural = '事件关键词'


class KeywordsStatistical(models.Model):
    name = models.CharField(max_length=20, verbose_name='关键词')
    number = models.IntegerField(null=True, verbose_name='总数')

    events = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        verbose_name='事件'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '关键词统计'


class EventsMedia(models.Model):
    source = models.CharField(max_length=50, verbose_name='新闻来源')
    website = models.CharField(max_length=50, verbose_name='自身发布网站')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='上一级'
    )

    articles = models.ForeignKey(
        Article,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='文章'
    )
    
    class Meta:
        app_label = 'base'
        verbose_name_plural = '新闻来源关联' 


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
    href = models.CharField(default='', max_length=50, verbose_name='链接')
    level = models.IntegerField(verbose_name='等级') # 1: 一级, 2： 二级页面, 3: 三级页面, -1: 子页面
    icon = models.CharField(default='', max_length=50, verbose_name='图标')
    component = models.CharField(default='', max_length=50, verbose_name='组件')
    index = models.IntegerField(default=0, verbose_name='索引') # 排序依据
    project = models.IntegerField(default=0, verbose_name='所属项目') # 0: 共用, 1: 质量舆情(App), 2: 产品目录管理(Admin)
    nav_type = models.IntegerField(default=0, verbose_name='导航类型') # 0: 普通导航, 1: 主页面包含子导航的导航

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


class NewsReport(models.Model):
    year = models.IntegerField(verbose_name='年份')
    period = models.IntegerField(verbose_name='期数')
    news_type = models.CharField(max_length=50, verbose_name='类型')
    publisher = models.CharField(max_length=50, verbose_name='发布者')
    pubtime = models.DateField(default=datetime.date.today, verbose_name='发布时间')
    file = models.FileField(upload_to=UPLOAD_URL, verbose_name='文件')
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='单位'
    )

    class Meta:
        app_label = 'base'
        verbose_name_plural = '舆情报告'

    def __str__(self):
        return self.group.name


class VersionRecord(models.Model):
    version = models.CharField(max_length=255, verbose_name='版本号')
    content = HTMLField(verbose_name='内容')
    pubtime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        app_label = 'base'
        verbose_name_plural = '版本记录'
        ordering = ['-pubtime']

    def __str__(self):
        return self.version
