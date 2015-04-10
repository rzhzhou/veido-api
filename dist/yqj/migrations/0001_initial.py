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
                ('feeling_factor', models.FloatField(default=-1, verbose_name='\u6b63\u8d1f\u9762')),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
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
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0', blank=True)),
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
            name='ArticleCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255, verbose_name='\u5206\u7c7b', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('article', models.ForeignKey(verbose_name='\u6587\u7ae0', to='yqj.Article')),
            ],
            options={
                'db_table': 'article_collection',
                'verbose_name_plural': '\u6587\u7ae0\u6536\u85cf',
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
                ('searchmode', models.IntegerField(default=0, verbose_name='\u641c\u7d22\u65b9\u5f0f')),
            ],
            options={
                'db_table': 'articlepublisher',
                'verbose_name_plural': '\u6587\u7ae0\u53d1\u5e03\u8005',
            },
            bases=(models.Model,),
        ),
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
                ('name', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('manufacturer', models.CharField(max_length=255, null=True, verbose_name='\u8f6c\u8f7d\u6b21\u6570', blank=True)),
                ('qualitied', models.FloatField(null=True, verbose_name='\u5173\u6ce8\u5ea6', blank=True)),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('product', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
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
                ('abstract', models.TextField(verbose_name='\u7b80\u4ecb', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True)),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
                ('articles', models.ManyToManyField(related_query_name=b'topics', related_name='topic', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'topic',
                'verbose_name_plural': '\u805a\u7c7b\u4e8b\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'db_table': 'topic_collection',
                'verbose_name_plural': '\u8d28\u91cf\u4e8b\u4ef6\u6536\u85cf',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=20, verbose_name='\u767b\u5f55\u540d')),
                ('password', models.CharField(max_length=255, verbose_name='hash\u5bc6\u7801')),
                ('salt', models.CharField(max_length=255)),
                ('isAdmin', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='yqj.User', verbose_name='\u7528\u6237')),
                ('articles', models.ManyToManyField(related_query_name=b'collection', related_name='collections', to='yqj.Article', through='yqj.ArticleCollection', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'collection',
                'verbose_name_plural': '\u7528\u6237\u6536\u85cf',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='yqj.User')),
            ],
            options={
            },
            bases=('yqj.user',),
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
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
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
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
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
            model_name='user',
            name='area',
            field=models.ForeignKey(to='yqj.Area'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(to='yqj.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topiccollection',
            name='collection',
            field=models.ForeignKey(verbose_name='\u6536\u85cf', to='yqj.Collection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topiccollection',
            name='topic',
            field=models.ForeignKey(verbose_name='\u8d28\u91cf\u4e8b\u4ef6', to='yqj.Topic'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='topiccollection',
            unique_together=set([('topic', 'collection')]),
        ),
        migrations.AddField(
            model_name='topic',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'topics', related_name='topic', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='weixin',
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
            model_name='collection',
            name='events',
            field=models.ManyToManyField(related_query_name=b'collection', related_name='collections', to='yqj.Topic', through='yqj.TopicCollection', blank=True, null=True, verbose_name='\u8d28\u91cf\u4e8b\u4ef6'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecollection',
            name='collection',
            field=models.ForeignKey(verbose_name='\u6536\u85cf', to='yqj.Collection'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articlecollection',
            unique_together=set([('article', 'collection')]),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher',
            field=models.ForeignKey(verbose_name='\u6587\u7ae0\u53d1\u5e03\u8005', to='yqj.ArticlePublisher'),
            preserve_default=True,
        ),
    ]
