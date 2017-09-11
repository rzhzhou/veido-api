# -*- coding: utf-8 -*-
import hmac
import hashlib

from django.conf import settings
from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from observer.apps.origin.models import Area, Inspection, InspectionPublisher

def make_random_string(
        length=10,
        allowed_chars='abcdefghjkmnpqrstuvwxyz'
        'ABCDEFGHJKLMNPQRSTUVWXYZ'
        '23456789'):
    return get_random_string(length, allowed_chars)


def hash_password(raw_password, salt):
    value = salt + raw_password + salt
    hash = hmac.new(settings.SECRET_KEY, digestmod=hashlib.sha1)
    hash.update(value)
    return hash.hexdigest()


def save_user(username, raw_password, area, group, isAdmin=0):
    kwargs = {}
    kwargs['username'] = username
    kwargs['salt'] = make_random_string()
    kwargs['password'] = hash_password(raw_password, kwargs['salt'])
    kwargs['area'] = area
    kwargs['group'] = group
    kwargs['isAdmin'] = isAdmin
    user = User(**kwargs)
    user.save(using='master')
    return user


class Group(models.Model):
    company = models.CharField(max_length=255)

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'舆情机用户组'

    def __unicode__(self):
        return self.company


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, verbose_name=u'登录名')
    password = models.CharField(max_length=255, verbose_name=u'密码')
    salt = models.CharField(max_length=255)
    area = models.ForeignKey(Area)
    isAdmin = models.IntegerField(default=0)
    group = models.ForeignKey(Group)

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'舆情机用户'

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True


class Custom(models.Model):
    searchkeyword = models.CharField(max_length=255, verbose_name=u'关键词')

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'指定监测'

    def __unicode__(self):
        return self.searchkeyword


class CustomKeyword(models.Model):
    newkeyword = models.CharField(max_length=255, verbose_name=u'关键词')
    review = models.CharField(max_length=255, default=u'', verbose_name=u'审核')
    group = models.ForeignKey(Group)
    custom = models.ForeignKey(Custom, null=True, blank=True, default=u'')

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'指定监测关键词'

    def __unicode__(self):
        return self.newkeyword


class ArticleCollection(models.Model):
    create_time = models.DateTimeField(auto_now=True, verbose_name=u'创建时间')

    user = models.OneToOneField(User, verbose_name=u'用户')
    article = models.ForeignKey(Article, verbose_name=u'文章')

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'文章收藏'

    def __unicode__(self):
        return self.category


class LocaltionScore(models.Model):
    score = models.IntegerField(default=0, verbose_name=u'分数')
    
    group = models.ForeignKey(Group, verbose_name=u'分组')
    article = models.ForeignKey(Article, verbose_name=u'文章')

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'本地相关度'

    def __unicode__(self):
        return str(self.score)


class AnonymousUser(User):
    def is_authenticated(self):
        return False

    class Meta:
        app_label = 'yqj'


class GroupAuthUser(models.Model):
    auth = models.CharField(max_length=255, verbose_name=u'用户名')
    group = models.ForeignKey(Group, verbose_name=u'分组')

    class Meta:
        app_label = 'yqj'
        verbose_name_plural = u'用户绑定'

    def __unicode__(self):
        return self.auth
