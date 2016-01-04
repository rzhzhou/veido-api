# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CacheType(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'项目名')

    class Meta:
        app_label = 'config'
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
        app_label = 'config'
        db_table = 'cacheconf'
        verbose_name_plural = u'缓存管理'

    def __unicode__(self):
        return self.name


class SettingsOne(models.Model):
    allowed_hosts = models.CharField(max_length=255, verbose_name=u'ALLOWED_HOSTS', 
        default="['192.168.1.104', '27.17.61.26', 'cnshendu.com', 'www.cnshendu.com']")
    debug = models.CharField(max_length=225, verbose_name=u'DEBUG', 
        default="False")
    company_name = models.CharField(max_length=225, verbose_name=u'COMPANY_NAME', 
        default=u"舆情风险监测系统") 
    language_code = models.CharField(max_length=225, verbose_name=u'LANGUAGE_CODE', 
        default="en-us")
    time_zone = models.CharField(max_length=225, verbose_name=u'TIME_ZONE', 
        default="Asia/Shanghai")
    use_i18n = models.CharField(max_length=225, verbose_name=u'USE_I18N', 
        default="True")
    use_l10n = models.CharField(max_length=225, verbose_name=u'USE_L10N', 
        default="True")
    use_tz = models.CharField(max_length=225, verbose_name=u'USE_TZ', 
        default="True")
    media_root = models.CharField(max_length=225, verbose_name=u'MEDIA_ROOT', 
        default="/var/www/wh/media")
    static_root = models.CharField(max_length=225, verbose_name=u'STATIC_ROOT', 
        default="/var/www/wh/static")
    news = models.CharField(max_length=225, verbose_name=u'news', 
        default=u"质监热点")
    event = models.CharField(max_length=225, verbose_name=u'event', 
        default=u"质量事件")
    location = models.CharField(max_length=225, verbose_name=u'location', 
        default=u"区域信息")
    custom = models.CharField(max_length=225, verbose_name=u'custom', 
        default=u"风险监测")
    site = models.CharField(max_length=225, verbose_name=u'site', 
        default=u"风险监测")
    business = models.CharField(max_length=225, verbose_name=u'business', 
        default=u"['综合', '标准化', '稽查打假', '质量监管', '科技兴检', '特种设备', '计量', '认证监管', '质量管理']")
    news_page_limit = models.IntegerField(verbose_name=u'NEWS_PAGE_LIMIT', default=25)
    risk_page_limit = models.IntegerField(verbose_name=u'RISK_PAGE_LIMIT', default=25)
    event_page_limit = models.IntegerField(verbose_name=u'EVENT_PAGE_LIMIT', default=25)
    weixin_table_limit = models.IntegerField(verbose_name=u'WEIXIN_TABLE_LIMIT', default=20)
    weibo_table_limit = models.IntegerField(verbose_name=u'WEIBO_TABLE_LIMIT', default=20)
    location_weixin_limit = models.IntegerField(verbose_name=u'LOCATION_WEIXIN_LIMIT', default=10)
    location_weibo_limit = models.IntegerField(verbose_name=u'LOCATION_WEIBO_LIMIT', default=10)
    event_weixin_limit = models.IntegerField(verbose_name=u'EVENT_WEIXIN_LIMIT', default=10)
    event_weibo_limit = models.IntegerField(verbose_name=u'EVENT_WEIBO_LIMIT', default=10)
    risk_weixin_limit = models.IntegerField(verbose_name=u'RISK_WEIXIN_LIMIT', default=10)
    risk_weibo_limit = models.IntegerField(verbose_name=u'RISK_WEIBO_LIMIT', default=10)
    custom_news_limit = models.IntegerField(verbose_name=u'CUSTOM_NEWS_LIMIT', default=10)
    custom_weixin_limit = models.IntegerField(verbose_name=u'CUSTOM_WEIXIN_LIMIT', default=10)
    custom_weibo_limit = models.IntegerField(verbose_name=u'CUSTOM_WEIBO_LIMIT', default=10)
    product_limit = models.IntegerField(verbose_name=u'PRODUCT_LIMIT', default=10)
    search_limit = models.IntegerField(verbose_name=u'SEARCH_LIMIT', default=20)
    mysql_default = models.CharField(max_length=225, verbose_name=u'mysql_default', 
        default="mysql://shendu:P@55word@192.168.1.205:3306/yqj")
    mysql_master = models.CharField(max_length=225, verbose_name=u'mysql_master', 
        default="mysql://shendu:P@55word@192.168.1.205:3306/yqj")
    mongo_conn = models.CharField(max_length=225, verbose_name=u'mongo_conn', 
        default="mongodb://192.168.1.202:27017")
    redis_conn = models.CharField(max_length=225, verbose_name=u'redis_conn', 
        default="redis://192.168.1.205:6379/8")
    mysql_slave = models.CharField(max_length=225, verbose_name=u'mysql_slave', 
        default="mysql://root:123456@192.168.1.101:3306/yqj2")

    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u'用户')

    class Meta:
        app_label = 'config'
        db_table = 'settings_one'
        verbose_name_plural = u'设置'

    def __unicode__(self):
        return self.user.username
