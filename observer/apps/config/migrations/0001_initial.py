# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CacheConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u9879\u76ee\u540d')),
                ('time', models.IntegerField(null=True, verbose_name='*/min', blank=True)),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('task', models.CharField(max_length=255, null=True, verbose_name='\u4efb\u52a1', blank=True)),
            ],
            options={
                'db_table': 'cacheconf',
                'verbose_name_plural': '\u7f13\u5b58\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CacheType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u9879\u76ee\u540d')),
            ],
            options={
                'db_table': 'cachetype',
                'verbose_name_plural': '\u7f13\u5b58\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SettingsOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allowed_hosts', models.CharField(default=b"['192.168.1.104', '27.17.61.26', 'cnshendu.com', 'www.cnshendu.com']", max_length=255, verbose_name='ALLOWED_HOSTS')),
                ('debug', models.CharField(default=b'False', max_length=225, verbose_name='DEBUG')),
                ('company_name', models.CharField(default='\u8206\u60c5\u98ce\u9669\u76d1\u6d4b\u7cfb\u7edf', max_length=225, verbose_name='COMPANY_NAME')),
                ('language_code', models.CharField(default=b'en-us', max_length=225, verbose_name='LANGUAGE_CODE')),
                ('time_zone', models.CharField(default=b'Asia/Shanghai', max_length=225, verbose_name='TIME_ZONE')),
                ('use_i18n', models.CharField(default=b'True', max_length=225, verbose_name='USE_I18N')),
                ('use_l10n', models.CharField(default=b'True', max_length=225, verbose_name='USE_L10N')),
                ('use_tz', models.CharField(default=b'True', max_length=225, verbose_name='USE_TZ')),
                ('media_root', models.CharField(default=b'/var/www/wh/media', max_length=225, verbose_name='MEDIA_ROOT')),
                ('static_root', models.CharField(default=b'/var/www/wh/static', max_length=225, verbose_name='STATIC_ROOT')),
                ('news', models.CharField(default='\u8d28\u76d1\u70ed\u70b9', max_length=225, verbose_name='news')),
                ('event', models.CharField(default='\u8d28\u91cf\u4e8b\u4ef6', max_length=225, verbose_name='event')),
                ('location', models.CharField(default='\u533a\u57df\u4fe1\u606f', max_length=225, verbose_name='location')),
                ('custom', models.CharField(default='\u98ce\u9669\u76d1\u6d4b', max_length=225, verbose_name='custom')),
                ('site', models.CharField(default='\u98ce\u9669\u76d1\u6d4b', max_length=225, verbose_name='site')),
                ('business', models.CharField(default="['\u7efc\u5408', '\u6807\u51c6\u5316', '\u7a3d\u67e5\u6253\u5047', '\u8d28\u91cf\u76d1\u7ba1', '\u79d1\u6280\u5174\u68c0', '\u7279\u79cd\u8bbe\u5907', '\u8ba1\u91cf', '\u8ba4\u8bc1\u76d1\u7ba1', '\u8d28\u91cf\u7ba1\u7406']", max_length=225, verbose_name='business')),
                ('news_page_limit', models.IntegerField(default=25, verbose_name='NEWS_PAGE_LIMIT')),
                ('risk_page_limit', models.IntegerField(default=25, verbose_name='RISK_PAGE_LIMIT')),
                ('event_page_limit', models.IntegerField(default=25, verbose_name='EVENT_PAGE_LIMIT')),
                ('weixin_table_limit', models.IntegerField(default=20, verbose_name='WEIXIN_TABLE_LIMIT')),
                ('weibo_table_limit', models.IntegerField(default=20, verbose_name='WEIBO_TABLE_LIMIT')),
                ('location_weixin_limit', models.IntegerField(default=10, verbose_name='LOCATION_WEIXIN_LIMIT')),
                ('location_weibo_limit', models.IntegerField(default=10, verbose_name='LOCATION_WEIBO_LIMIT')),
                ('event_weixin_limit', models.IntegerField(default=10, verbose_name='EVENT_WEIXIN_LIMIT')),
                ('event_weibo_limit', models.IntegerField(default=10, verbose_name='EVENT_WEIBO_LIMIT')),
                ('risk_weixin_limit', models.IntegerField(default=10, verbose_name='RISK_WEIXIN_LIMIT')),
                ('risk_weibo_limit', models.IntegerField(default=10, verbose_name='RISK_WEIBO_LIMIT')),
                ('custom_news_limit', models.IntegerField(default=10, verbose_name='CUSTOM_NEWS_LIMIT')),
                ('custom_weixin_limit', models.IntegerField(default=10, verbose_name='CUSTOM_WEIXIN_LIMIT')),
                ('custom_weibo_limit', models.IntegerField(default=10, verbose_name='CUSTOM_WEIBO_LIMIT')),
                ('product_limit', models.IntegerField(default=10, verbose_name='PRODUCT_LIMIT')),
                ('search_limit', models.IntegerField(default=20, verbose_name='SEARCH_LIMIT')),
                ('mysql_default', models.CharField(default=b'mysql://shendu:P@55word@192.168.1.205:3306/yqj', max_length=225, verbose_name='mysql_default')),
                ('mysql_master', models.CharField(default=b'mysql://shendu:P@55word@192.168.1.205:3306/yqj', max_length=225, verbose_name='mysql_master')),
                ('mongo_conn', models.CharField(default=b'mongodb://192.168.1.202:27017', max_length=225, verbose_name='mongo_conn')),
                ('redis_conn', models.CharField(default=b'redis://192.168.1.205:6379/8', max_length=225, verbose_name='redis_conn')),
                ('mysql_slave', models.CharField(default=b'mysql://root:123456@192.168.1.101:3306/yqj2', max_length=225, verbose_name='mysql_slave')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'settings_one',
                'verbose_name_plural': '\u8bbe\u7f6e',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cacheconf',
            name='typename',
            field=models.ForeignKey(verbose_name='\u7c7b\u578b', blank=True, to='config.CacheType', null=True),
            preserve_default=True,
        ),
    ]
