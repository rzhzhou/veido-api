# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0008_user_isadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255, verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('manufacturer', models.CharField(max_length=255, null=True, verbose_name='\u8f6c\u8f7d\u6b21\u6570', blank=True)),
                ('qualitied', models.FloatField(null=True, verbose_name='\u5173\u6ce8\u5ea6', blank=True)),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('product', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('status', models.IntegerField(null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('province', models.CharField(max_length=255, verbose_name='\u7701')),
                ('city', models.CharField(max_length=255, null=True, verbose_name='\u5e02', blank=True)),
                ('district', models.CharField(max_length=255, null=True, verbose_name='\u5730\u533a', blank=True)),
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'inspection',
                'verbose_name_plural': '\u62bd\u68c0',
            },
            bases=(models.Model,),
        ),
    ]
