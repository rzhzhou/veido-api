# -*- coding: utf-8 -*-
from django.db import models
from observer.apps.base.models import User

# Create your models here.
class CacheType(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'项目名')

    class Meta:
        db_table = 'cachetype'
        verbose_name_plural = u'缓存类型'

    def __unicode__(self):
        return self.name


class CacheConf(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'项目名')
    time = models.IntegerField(null=True, blank=True, verbose_name=u'*/min')
    url = models.CharField(max_length=255, verbose_name=u'url')
    task = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'任务')
    typename = models.ForeignKey(CacheType, null=True, blank=True, verbose_name=u'类型')

    class Meta:
        db_table = 'cacheconf'
        verbose_name_plural = u'缓存管理'

    def __unicode__(self):
        return self.name


class SettingsType(models.Model):
    name = models.CharField(max_length=225, verbose_name=u'设置类型')

    class Meta:
        db_table = 'settings_type'
        verbose_name_plural = u'设置类型'

    def __unicode__ (self):
        return self.name


class Settings(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'设置项')
    value = models.CharField(max_length=225, verbose_name=u'设置值') 
    type =  models.ForeignKey(SettingsType, verbose_name=u'设置类型')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u'用户')

    class Meta:
        db_table = 'settings'
        verbose_name_plural = u'设置'

    def __unicode__(self):
        return self.name + ':' + self.value
