# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0003_auto_20150311_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='', blank=True)),
                ('remark', models.CharField(max_length=255, verbose_name='\u5907\u6ce8', blank=True)),
                ('articles', models.ManyToManyField(related_query_name=b'category', related_name='categorys', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'article_category',
                'verbose_name_plural': '\u6587\u7ae0\u5206\u7c7b',
            },
            bases=(models.Model,),
        ),
    ]
