# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawInspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', tinymce.models.HTMLField(blank=True, verbose_name='\u6b63\u6587')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u539f\u59cb\u98ce\u9669\u62bd\u68c0',
            },
        ),
    ]
