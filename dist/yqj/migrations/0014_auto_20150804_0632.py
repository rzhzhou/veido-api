# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0013_risk'),
    ]

    operations = [
         migrations.CreateModel(
            name='LRisk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('abstract', models.TextField(verbose_name='\u7b80\u4ecb', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True)),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='\u5173\u952e\u8bcd', blank=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
                ('articles', models.ManyToManyField(related_query_name=b'lrisk', related_name='lrisks', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
                ('weibo', models.ManyToManyField(related_query_name=b'lrisk', related_name='lrisks', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a')),
                ('weixin', models.ManyToManyField(related_query_name=b'lrisk', related_name='lrisks', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1')),
            ],
            options={
                'db_table': 'risk',
                'verbose_name_plural': '\u672c\u5730\u8bc4\u5206',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TRisk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('abstract', models.TextField(verbose_name='\u7b80\u4ecb', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True)),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='\u5173\u952e\u8bcd', blank=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
                ('articles', models.ManyToManyField(related_query_name=b'trisk', related_name='trisks', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
                ('weibo', models.ManyToManyField(related_query_name=b'trisk', related_name='trisks', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a')),
                ('weixin', models.ManyToManyField(related_query_name=b'trisk', related_name='trisks', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1')),
            ],
            options={
                'db_table': 'risk',
                'verbose_name_plural': '\u98ce\u9669\u8bc4\u5206',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='localtionscore',
            name='article',
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='risk',
            field=models.ForeignKey(default=1, verbose_name='\u98ce\u9669\u5feb\u8baf', to='yqj.Risk'),
            preserve_default=False,
        ),
    ]
