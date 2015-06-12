#coding: utf-8
import hmac
import hashlib
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'名称')
    level = models.BigIntegerField(null=False, verbose_name=u'等级')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一级')

    class Meta:
        db_table = 'area'
        verbose_name_plural = u'地域'

    def __unicode__(self):
        return self.name

class WeixinPublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'weixinpublisher'
        verbose_name_plural = u'微信发布者'

    def __unicode__(self):
        return self.publisher



class Weixin(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    origin_source = models.CharField(max_length=255, blank=True, verbose_name=u'信息转载来源')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    website_type = models.CharField(max_length=255, blank=True, verbose_name=u'网站类型')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(WeixinPublisher, verbose_name=u'微信发布者')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    uuid = models.CharField(max_length=36)
    readnum = models.IntegerField(blank=True, verbose_name=u'阅读数', default=0)
    likenum = models.IntegerField(blank=True, verbose_name=u'点赞数', default=0)

    class Meta:
        db_table = 'weixin'
        verbose_name_plural = u'微信'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class WeiboPublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'weibopublisher'
        verbose_name_plural = u'微博发布者'

    def __unicode__(self):
        return self.publisher


class Weibo(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    origin_source = models.CharField(max_length=255, blank=True, verbose_name=u'信息转载来源')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    website_type = models.CharField(max_length=255, blank=True, verbose_name=u'网站类型')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(WeiboPublisher, verbose_name=u'微博发布者')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    attitudes_count = models.IntegerField(blank=True, verbose_name=u'点赞数' ,default=0)
    comments_count = models.IntegerField(blank=True, verbose_name=u'评论量' ,default=0)
    reposts_count = models.IntegerField(blank=True, verbose_name=u'转发量' ,default=0)
    uuid = models.CharField(max_length=36)

    class Meta:
        db_table = 'weibo'
        verbose_name_plural = u'微博'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class ArticlePublisher(models.Model):
    photo = models.URLField(verbose_name=u'用户头像')
    publisher = models.CharField(max_length=255, verbose_name=u'发布者')
    brief = models.CharField(max_length=255, verbose_name=u'简介')
    searchmode = models.IntegerField(default=0, verbose_name=u'搜索方式')

    class Meta:
        db_table = 'articlepublisher'
        verbose_name_plural = u'文章发布者'

    def __unicode__(self):
        return self.publisher


class Article(models.Model):
    author = models.CharField(max_length=255, verbose_name=u'作者')
    title = models.CharField(max_length=255,blank=True, verbose_name=u'标题')
    url = models.URLField(verbose_name=u'网站链接')
    content = models.TextField(blank=True, verbose_name=u'正文')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'信息来源')
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    publisher = models.ForeignKey(ArticlePublisher, verbose_name=u'文章发布者')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    uuid = models.CharField(max_length=36)
    feeling_factor = models.FloatField(default=-1, verbose_name=u'正负面')
    website_type = models.CharField(max_length=20, blank=True, verbose_name=u'类型')

    class Meta:
        db_table = 'article'
        verbose_name_plural = u'文章'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    abstract = models.TextField(blank=True, verbose_name=u'简介')
    source = models.CharField(max_length=255, blank=True, verbose_name=u'首发媒体')
    area = models.ForeignKey(Area, verbose_name=u'地域')
    keywords = models.CharField(max_length=255, default=u'', verbose_name=u'关键词', blank=True)
    articles = models.ManyToManyField(Article, related_name='topic', related_query_name='topics', null=True, blank=True, verbose_name=u'文章')
    weibo = models.ManyToManyField(Weibo, related_name='topic', related_query_name='topics', null=True, blank=True, verbose_name=u'微博')
    weixin = models.ManyToManyField(Weixin, related_name='topic', related_query_name='topics', null=True, blank=True, verbose_name=u'微信')

    class Meta:
        db_table = 'topic'
        verbose_name_plural = u'聚类事件'

    def __unicode__(self):
        return self.title


class RelatedData(models.Model):
    uuid = models.CharField(max_length=36, verbose_name=u'uuid')
    articles = models.ManyToManyField(Article, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'文章')
    weibo = models.ManyToManyField(Weibo, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'微博')
    weixin = models.ManyToManyField(Weixin, related_name='relateddata', related_query_name='relateddatas', null=True, blank=True, verbose_name=u'微信')

    class Meta:
        db_table = 'relateddata'
        verbose_name_plural = u'关联文章'

    def __unicode__(self):
        return self.uuid


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=u'名称')
    remark = models.CharField(max_length=255, blank=True, verbose_name=u'备注')

    articles = models.ManyToManyField(Article, related_name='category', related_query_name='categorys', null=True, blank=True, verbose_name=u'文章')

    class Meta:
        db_table = 'category'
        verbose_name_plural = u'文章分类'

def make_random_string(length=10,
                         allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                       'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                       '23456789'):
   return get_random_string(length, allowed_chars)

def hash_password(raw_password, salt):
    value = salt + raw_password + salt
    hash = hmac.new(settings.SECRET_KEY, digestmod=hashlib.sha1)
    hash.update(value)
    return hash.hexdigest()

def save_user(username, raw_password, area, group):
    kwargs = {}
    kwargs['username'] = username
    kwargs['salt'] = make_random_string()
    kwargs['password'] = hash_password(raw_password, kwargs['salt'])
    kwargs['area'] = area
    kwargs['group'] = group
    user = User(**kwargs)
    user.save(using='master')
    return user

class Group(models.Model):
    company = models.CharField(max_length=255)

    def __unicode__(self):
        return self.company


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, verbose_name=u'登录名')
    password = models.CharField(max_length=255, verbose_name=u'hash密码')
    salt = models.CharField(max_length=255)
    area = models.ForeignKey(Area)
    isAdmin = models.IntegerField(default=0)
    group = models.ForeignKey(Group)

    def is_authenticated(self):
        return True


class Custom(models.Model):
    searchkeyword = models.CharField(max_length=255, verbose_name=u'关键词')
    #group = models.ManyToManyField(Group, related_name='custom', related_query_name='customs', null=True, blank=True, verbose_name=u'所属组')
    articles = models.ManyToManyField(Article, related_name='custom', related_query_name='customs', null=True, blank=True, verbose_name=u'文章')
    weibo = models.ManyToManyField(Weibo, related_name='custom', related_query_name='customs', null=True, blank=True, verbose_name=u'微博')
    weixin = models.ManyToManyField(Weixin, related_name='custom', related_query_name='customs', null=True, blank=True, verbose_name=u'微信')

    class Meta:
        db_table = 'custom'
        verbose_name_plural = u'指定监测'

    def __unicode__(self):
        return self.searchkeyword


class Product(models.Model):
    product = models.CharField(max_length=255, verbose_name='产品')

    articles = models.ManyToManyField(Article, related_name='product', related_query_name='products', null=True, blank=True, verbose_name=u'文章')

    class Meta:
        db_table = 'product'
        verbose_name_plural = u'产品监测'

    def __unicode__(self):
        return self.product


class Keyword(models.Model):
    newkeyword = models.CharField(max_length=255, verbose_name=u'关键词')
    review = models.CharField(max_length=255, default=u'', verbose_name=u'审核')
    #synced = models.CharField(max_length=255, default=u'', verbose_name=u'同步')
    group = models.ForeignKey(Group)
    custom = models.ForeignKey(Custom, null=True, blank=True, default=u'')

    class Meta:
        db_table = 'keyword'
        verbose_name_plural = u'关键词'

    def __unicode__(self):
        return self.newkeyword


class Collection(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name=u'用户')
    articles = models.ManyToManyField(Article, null=True, blank=True, related_name='collections', related_query_name='collection', through='ArticleCollection', verbose_name=u'文章')
    events = models.ManyToManyField(Topic, null=True,blank=True, related_name='collections', related_query_name='collection', through='TopicCollection', verbose_name=u'质量事件')

    class Meta:
        db_table = 'collection'
        verbose_name_plural = u'用户收藏'

    def __unicode__(self):
        return self.user.username + ' collection'


class ArticleCollection(models.Model):
    article = models.ForeignKey(Article, verbose_name=u'文章')
    collection = models.ForeignKey(Collection, verbose_name=u'收藏')

    category = models.CharField(max_length=255, blank=True, verbose_name=u'分类')
    create_time = models.DateTimeField(auto_now=True, verbose_name=u'创建时间')

    class Meta:
        db_table = 'article_collection'
        verbose_name_plural = u'文章收藏'
        unique_together = (("article", "collection"),)
    def __unicode__(self):
        return self.category


class TopicCollection(models.Model):
    topic = models.ForeignKey(Topic, verbose_name=u'质量事件')
    collection = models.ForeignKey(Collection, verbose_name=u'收藏')

    create_time = models.DateTimeField(auto_now=True, verbose_name=u'创建时间')

    class Meta:
        db_table = 'topic_collection'
        verbose_name_plural = u'质量事件收藏'
        unique_together = (("topic", "collection"),)


class AnonymousUser(User):
    def is_authenticated(self):
        return False


class Inspection(models.Model):
    url = models.CharField(max_length=255, verbose_name=u'网站链接')
    name = models.CharField(max_length=255, verbose_name=u'标题')
    manufacturer = models.CharField(max_length=255, null=True, blank=True,verbose_name=u'转载次数')
    qualitied = models.FloatField(verbose_name=u'关注度', null=True, blank=True)
    pubtime = models.DateTimeField(auto_now=False, verbose_name=u'发布时间')
    product = models.CharField(max_length=255, verbose_name=u'名称')
    source = models.CharField(max_length=255, verbose_name=u'信息来源')
    province = models.CharField(max_length=255, verbose_name=u'省')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'市')
    district = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'地区')

    class Meta:
        db_table = 'inspection'
        verbose_name_plural = u'抽检'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.name
