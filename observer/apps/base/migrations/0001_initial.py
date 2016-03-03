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
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'article',
                'verbose_name_plural': '\u6587\u7ae0',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255, verbose_name='\u5206\u7c7b', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
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
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0', blank=True)),
                ('remark', models.CharField(max_length=255, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'db_table': 'category',
                'verbose_name_plural': '\u6587\u7ae0\u5206\u7c7b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('searchkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
            ],
            options={
                'db_table': 'custom',
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
            ],
            options={
                'db_table': 'custom_keyword',
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b\u5173\u952e\u8bcd',
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
                'db_table': 'yqj_group',
                'verbose_name_plural': '\u8206\u60c5\u673a\u7528\u6237\u7ec4',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupAuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth', models.CharField(max_length=255, verbose_name='\u7528\u6237\u540d')),
            ],
            options={
                'db_table': 'group_authuser',
                'verbose_name_plural': '\u7528\u6237\u7ed1\u5b9a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=255, verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
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
            name='LocaltionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u5206\u6570')),
            ],
            options={
                'db_table': 'localtion_score',
                'verbose_name_plural': '\u672c\u5730\u8bc4\u5206\u5c55\u793a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u4ea7\u54c1')),
            ],
            options={
                'db_table': 'product',
                'verbose_name_plural': '\u4ea7\u54c1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=36, verbose_name='uuid')),
                ('articles', models.ManyToManyField(related_query_name=b'relateddata', related_name='relateddatas', to='base.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'relateddata',
                'verbose_name_plural': '\u5173\u8054\u6587\u7ae0',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('abstract', models.TextField(verbose_name='\u7b80\u4ecb', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True)),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='\u5173\u952e\u8bcd', blank=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('pubtime', models.DateTimeField(null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4', blank=True)),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='base.Area')),
                ('articles', models.ManyToManyField(related_query_name=b'risk', related_name='risks', to='base.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'risk',
                'verbose_name_plural': '\u98ce\u9669\u5feb\u8baf',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RiskScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u5206\u6570')),
                ('risk', models.ForeignKey(verbose_name='\u98ce\u9669\u5feb\u8baf', to='base.Risk')),
            ],
            options={
                'db_table': 'risk_score',
                'verbose_name_plural': '\u98ce\u9669\u8bc4\u5206\u5c55\u793a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('abstract', models.CharField(max_length=255, verbose_name='\u6b63\u6587', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True)),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='\u5173\u952e\u8bcd', blank=True)),
                ('pubtime', models.DateTimeField(null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4', blank=True)),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='base.Area')),
                ('articles', models.ManyToManyField(related_query_name=b'topic', related_name='topics', to='base.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'ordering': ['-pubtime'],
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
                ('password', models.CharField(max_length=255, verbose_name='\u5bc6\u7801')),
                ('salt', models.CharField(max_length=255)),
                ('isAdmin', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'yqj_user',
                'verbose_name_plural': '\u8206\u60c5\u673a\u7528\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to='base.User', verbose_name='\u7528\u6237')),
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
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.User')),
            ],
            options={
            },
            bases=('base.user',),
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
                ('attitudes_count', models.IntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570', blank=True)),
                ('comments_count', models.IntegerField(default=0, verbose_name='\u8bc4\u8bba\u91cf', blank=True)),
                ('reposts_count', models.IntegerField(default=0, verbose_name='\u8f6c\u53d1\u91cf', blank=True)),
                ('uuid', models.CharField(max_length=36)),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='base.Area')),
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
                ('readnum', models.IntegerField(default=0, verbose_name='\u9605\u8bfb\u6570', blank=True)),
                ('likenum', models.IntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570', blank=True)),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='base.Area')),
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
            field=models.ForeignKey(verbose_name='\u5fae\u4fe1\u53d1\u5e03\u8005', to='base.WeixinPublisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='weibo',
            name='publisher',
            field=models.ForeignKey(verbose_name='\u5fae\u535a\u53d1\u5e03\u8005', to='base.WeiboPublisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(to='base.Area'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(to='base.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topiccollection',
            name='collection',
            field=models.ForeignKey(verbose_name='\u6536\u85cf', to='base.Collection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topiccollection',
            name='topic',
            field=models.ForeignKey(verbose_name='\u8d28\u91cf\u4e8b\u4ef6', to='base.Topic'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='topiccollection',
            unique_together=set([('topic', 'collection')]),
        ),
        migrations.AddField(
            model_name='topic',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'topic', related_name='topics', to='base.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'topic', related_name='topics', to='base.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='risk',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'risk', related_name='risks', to='base.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='risk',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'risk', related_name='risks', to='base.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relateddata',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'relateddata', related_name='relateddatas', to='base.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relateddata',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'relateddata', related_name='relateddatas', to='base.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
    ]
