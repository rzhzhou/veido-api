# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('level', models.BigIntegerField(verbose_name='\u7b49\u7ea7')),
                ('parent', models.ForeignKey(verbose_name='\u4e0a\u4e00\u7ea7', blank=True, to='yqj.Area', null=True)),
            ],
            options={
                'db_table': 'area',
                'verbose_name_plural': '\u5730\u57df',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(verbose_name='\u6b63\u6587', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90', blank=True)),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('uuid', models.CharField(max_length=36)),
                ('area', models.ForeignKey(verbose_name='\u540d\u79f0', to='yqj.Area')),
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'article',
                'verbose_name_plural': '\u6587\u7ae0',
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='ArticlePublisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
            ],
            options={
                'db_table': 'articlepublisher',
                'verbose_name_plural': '\u6587\u7ae0\u53d1\u5e03\u8005',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=36, verbose_name='uuid')),
                ('articles', models.ManyToManyField(related_query_name=b'relateddatas', related_name='relateddata', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'relateddata',
                'verbose_name_plural': '\u5173\u8054\u6587\u7ae0',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('abstract', models.TextField(verbose_name='\u6b63\u6587', blank=True)),
                ('articles', models.ManyToManyField(related_query_name=b'topics', related_name='topic', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'topic',
                'verbose_name_plural': '\u805a\u7c7b\u4e8b\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Weibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(verbose_name='\u6b63\u6587', blank=True)),
                ('origin_source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u8f6c\u8f7d\u6765\u6e90', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90', blank=True)),
                ('website_type', models.CharField(max_length=255, verbose_name='\u7f51\u7ad9\u7c7b\u578b', blank=True)),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('praise', models.IntegerField(verbose_name='\u70b9\u8d5e\u6570', blank=True)),
                ('comment', models.IntegerField(verbose_name='\u8bc4\u8bba\u91cf', blank=True)),
                ('tansmit', models.IntegerField(verbose_name='\u8f6c\u53d1\u91cf', blank=True)),
                ('uuid', models.CharField(max_length=36)),
                ('area', models.ForeignKey(verbose_name='\u540d\u79f0', to='yqj.Area')),
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'weibo',
                'verbose_name_plural': '\u5fae\u535a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeiboPublisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
            ],
            options={
                'db_table': 'weibopublisher',
                'verbose_name_plural': '\u5fae\u535a\u53d1\u5e03\u8005',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Weixin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(verbose_name='\u6b63\u6587', blank=True)),
                ('origin_source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u8f6c\u8f7d\u6765\u6e90', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90', blank=True)),
                ('website_type', models.CharField(max_length=255, verbose_name='\u7f51\u7ad9\u7c7b\u578b', blank=True)),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('uuid', models.CharField(max_length=36)),
                ('area', models.ForeignKey(verbose_name='\u540d\u79f0', to='yqj.Area')),
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'weixin',
                'verbose_name_plural': '\u5fae\u4fe1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeixinPublisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
            ],
            options={
                'db_table': 'weixinpublisher',
                'verbose_name_plural': '\u5fae\u4fe1\u53d1\u5e03\u8005',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='weixin',
            name='publisher',
            field=models.ForeignKey(verbose_name='\u5fae\u4fe1\u53d1\u5e03\u8005', to='yqj.WeixinPublisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='weibo',
            name='publisher',
            field=models.ForeignKey(verbose_name='\u5fae\u535a\u53d1\u5e03\u8005', to='yqj.WeiboPublisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'topics', related_name='topic', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relateddata',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'relateddatas', related_name='relateddata', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relateddata',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'relateddatas', related_name='relateddata', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='publisher',
            field=models.ForeignKey(verbose_name='\u6587\u7ae0\u53d1\u5e03\u8005', to='yqj.ArticlePublisher'),
            preserve_default=True,
        ),
    ]
