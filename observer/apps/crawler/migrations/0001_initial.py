# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-13 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255, verbose_name='\u5e94\u7528')),
                ('sub_app', models.CharField(blank=True, max_length=255, verbose_name='\u5b50\u5e94\u7528')),
                ('file', models.CharField(max_length=255, verbose_name='\u6587\u4ef6\u540d')),
                ('rank', models.IntegerField(verbose_name='\u7b49\u7ea7')),
                ('url', models.URLField(verbose_name='\u94fe\u63a5')),
                ('data', models.TextField(blank=True, verbose_name='\u6570\u636e')),
                ('priority', models.IntegerField(verbose_name='\u4f18\u5148\u7ea7')),
                ('interval', models.IntegerField(verbose_name='\u5468\u671f')),
                ('timeout', models.IntegerField(verbose_name='\u8d85\u65f6\u65f6\u95f4')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('last_run', models.DateTimeField(verbose_name='\u4e0a\u6b21\u6267\u884c\u7ed3\u675f\u65f6\u95f4')),
                ('next_run', models.DateTimeField(verbose_name='\u4e0b\u6b21\u8fd0\u884c\u5f00\u59cb\u65f6\u95f4')),
                ('status', models.IntegerField(verbose_name='\u72b6\u6001')),
            ],
            options={
                'ordering': ['-rank', 'next_run', '-priority'],
                'verbose_name_plural': '\u722c\u866b\u4efb\u52a1',
            },
        ),
        migrations.CreateModel(
            name='TaskConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255, verbose_name='\u5e94\u7528')),
                ('sub_app', models.CharField(blank=True, max_length=255, verbose_name='\u5b50\u5e94\u7528')),
                ('file', models.CharField(max_length=255, verbose_name='\u6587\u4ef6\u540d')),
                ('rank', models.IntegerField(verbose_name='\u7b49\u7ea7')),
                ('priority', models.IntegerField(verbose_name='\u4f18\u5148\u7ea7')),
                ('interval', models.IntegerField(verbose_name='\u5468\u671f')),
                ('timeout', models.IntegerField(verbose_name='\u8d85\u65f6\u65f6\u95f4')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('status', models.IntegerField(verbose_name='\u72b6\u6001')),
            ],
            options={
                'verbose_name_plural': '\u722c\u866b\u4efb\u52a1\u914d\u7f6e',
            },
        ),
    ]
