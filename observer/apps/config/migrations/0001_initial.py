# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CacheConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u9879\u76ee\u540d')),
                ('time', models.IntegerField(null=True, verbose_name='*/min', blank=True)),
                ('url', models.CharField(max_length=255, verbose_name='url')),
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
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u8bbe\u7f6e\u9879')),
                ('value', models.CharField(max_length=225, verbose_name='\u8bbe\u7f6e\u503c')),
            ],
            options={
                'db_table': 'settings',
                'verbose_name_plural': '\u8bbe\u7f6e',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SettingsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225, verbose_name='\u8bbe\u7f6e\u7c7b\u578b')),
            ],
            options={
                'db_table': 'settings_type',
                'verbose_name_plural': '\u8bbe\u7f6e\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='settings',
            name='type',
            field=models.ForeignKey(verbose_name='\u8bbe\u7f6e\u7c7b\u578b', to='config.SettingsType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='settings',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to='base.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cacheconf',
            name='typename',
            field=models.ForeignKey(verbose_name='\u7c7b\u578b', blank=True, to='config.CacheType', null=True),
            preserve_default=True,
        ),
    ]
