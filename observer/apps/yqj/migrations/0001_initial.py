# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-10 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('origin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(blank=True, verbose_name='\u6b63\u6587')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('uuid', models.CharField(max_length=36)),
                ('feeling_factor', models.FloatField(default=-1, verbose_name='\u6b63\u8d1f\u9762')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='ArticleCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=255, verbose_name='\u5206\u7c7b')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0\u6536\u85cf',
            },
        ),
        migrations.CreateModel(
            name='ArticlePublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
                ('searchmode', models.IntegerField(default=0, verbose_name='\u641c\u7d22\u65b9\u5f0f')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0\u53d1\u5e03\u8005',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='\u540d\u79f0')),
                ('remark', models.CharField(blank=True, max_length=255, verbose_name='\u5907\u6ce8')),
                ('articles', models.ManyToManyField(related_name='categorys', related_query_name=b'category', to='yqj.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searchkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('articles', models.ManyToManyField(related_name='customs', related_query_name=b'custom', to='yqj.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b',
            },
        ),
        migrations.CreateModel(
            name='CustomKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
                ('custom', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='yqj.Custom')),
            ],
            options={
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b\u5173\u952e\u8bcd',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '\u8206\u60c5\u673a\u7528\u6237\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='GroupAuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth', models.CharField(max_length=255, verbose_name='\u7528\u6237\u540d')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group', verbose_name='\u5206\u7ec4')),
            ],
            options={
                'verbose_name_plural': '\u7528\u6237\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255, verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('name', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u8f6c\u8f7d\u6b21\u6570')),
                ('qualitied', models.FloatField(blank=True, null=True, verbose_name='\u5173\u6ce8\u5ea6')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('product', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('province', models.CharField(max_length=255, verbose_name='\u7701')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5e02')),
                ('district', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5730\u533a')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u62bd\u68c0',
            },
        ),
        migrations.CreateModel(
            name='LocaltionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='\u5206\u6570')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group', verbose_name='\u5206\u7ec4')),
            ],
            options={
                'verbose_name_plural': '\u672c\u5730\u8bc4\u5206\u5c55\u793a',
            },
        ),
        migrations.CreateModel(
            name='RelatedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=36, verbose_name='uuid')),
                ('articles', models.ManyToManyField(related_name='relateddatas', related_query_name=b'relateddata', to='yqj.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'verbose_name_plural': '\u5173\u8054\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('abstract', models.TextField(blank=True, verbose_name='\u7b80\u4ecb')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53')),
                ('keywords', models.CharField(blank=True, default='', max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
                ('articles', models.ManyToManyField(related_name='risks', related_query_name=b'risk', to='yqj.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u98ce\u9669\u5feb\u8baf',
            },
        ),
        migrations.CreateModel(
            name='RiskScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='\u5206\u6570')),
                ('risk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Risk', verbose_name='\u98ce\u9669\u5feb\u8baf')),
            ],
            options={
                'verbose_name_plural': '\u98ce\u9669\u8bc4\u5206\u5c55\u793a',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('abstract', models.CharField(blank=True, max_length=255, verbose_name='\u6b63\u6587')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53')),
                ('keywords', models.CharField(blank=True, default='', max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
                ('articles', models.ManyToManyField(related_name='topics', related_query_name=b'topic', to='yqj.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u805a\u7c7b\u4e8b\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='TopicCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Topic', verbose_name='\u8d28\u91cf\u4e8b\u4ef6')),
            ],
            options={
                'verbose_name_plural': '\u8d28\u91cf\u4e8b\u4ef6\u6536\u85cf',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='\u767b\u5f55\u540d')),
                ('password', models.CharField(max_length=255, verbose_name='\u5bc6\u7801')),
                ('salt', models.CharField(max_length=255)),
                ('isAdmin', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': '\u8206\u60c5\u673a\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='Weibo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(blank=True, verbose_name='\u6b63\u6587')),
                ('origin_source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u8f6c\u8f7d\u6765\u6e90')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('website_type', models.CharField(blank=True, max_length=255, verbose_name='\u7f51\u7ad9\u7c7b\u578b')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('attitudes_count', models.IntegerField(blank=True, default=0, verbose_name='\u70b9\u8d5e\u6570')),
                ('comments_count', models.IntegerField(blank=True, default=0, verbose_name='\u8bc4\u8bba\u91cf')),
                ('reposts_count', models.IntegerField(blank=True, default=0, verbose_name='\u8f6c\u53d1\u91cf')),
                ('uuid', models.CharField(max_length=36)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u5fae\u535a',
            },
        ),
        migrations.CreateModel(
            name='WeiboPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
            ],
            options={
                'verbose_name_plural': '\u5fae\u535a\u53d1\u5e03\u8005',
            },
        ),
        migrations.CreateModel(
            name='Weixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(blank=True, verbose_name='\u6b63\u6587')),
                ('origin_source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u8f6c\u8f7d\u6765\u6e90')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('website_type', models.CharField(blank=True, max_length=255, verbose_name='\u7f51\u7ad9\u7c7b\u578b')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('uuid', models.CharField(max_length=36)),
                ('readnum', models.IntegerField(blank=True, default=0, verbose_name='\u9605\u8bfb\u6570')),
                ('likenum', models.IntegerField(blank=True, default=0, verbose_name='\u70b9\u8d5e\u6570')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u5fae\u4fe1',
            },
        ),
        migrations.CreateModel(
            name='WeixinPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
            ],
            options={
                'verbose_name_plural': '\u5fae\u4fe1\u53d1\u5e03\u8005',
            },
        ),
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yqj.User')),
            ],
            bases=('yqj.user',),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='yqj.User', verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name_plural': '\u7528\u6237\u6536\u85cf',
            },
        ),
        migrations.AddField(
            model_name='weixin',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.WeixinPublisher', verbose_name='\u5fae\u4fe1\u53d1\u5e03\u8005'),
        ),
        migrations.AddField(
            model_name='weibo',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.WeiboPublisher', verbose_name='\u5fae\u535a\u53d1\u5e03\u8005'),
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group'),
        ),
        migrations.AddField(
            model_name='topic',
            name='weibo',
            field=models.ManyToManyField(related_name='topics', related_query_name=b'topic', to='yqj.Weibo', verbose_name='\u5fae\u535a'),
        ),
        migrations.AddField(
            model_name='topic',
            name='weixin',
            field=models.ManyToManyField(related_name='topics', related_query_name=b'topic', to='yqj.Weixin', verbose_name='\u5fae\u4fe1'),
        ),
        migrations.AddField(
            model_name='risk',
            name='weibo',
            field=models.ManyToManyField(related_name='risks', related_query_name=b'risk', to='yqj.Weibo', verbose_name='\u5fae\u535a'),
        ),
        migrations.AddField(
            model_name='risk',
            name='weixin',
            field=models.ManyToManyField(related_name='risks', related_query_name=b'risk', to='yqj.Weixin', verbose_name='\u5fae\u4fe1'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='weibo',
            field=models.ManyToManyField(related_name='relateddatas', related_query_name=b'relateddata', to='yqj.Weibo', verbose_name='\u5fae\u535a'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='weixin',
            field=models.ManyToManyField(related_name='relateddatas', related_query_name=b'relateddata', to='yqj.Weixin', verbose_name='\u5fae\u4fe1'),
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='risk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Risk', verbose_name='\u98ce\u9669\u5feb\u8baf'),
        ),
        migrations.AddField(
            model_name='customkeyword',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group'),
        ),
        migrations.AddField(
            model_name='custom',
            name='weibo',
            field=models.ManyToManyField(related_name='customs', related_query_name=b'custom', to='yqj.Weibo', verbose_name='\u5fae\u535a'),
        ),
        migrations.AddField(
            model_name='custom',
            name='weixin',
            field=models.ManyToManyField(related_name='customs', related_query_name=b'custom', to='yqj.Weixin', verbose_name='\u5fae\u4fe1'),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.ArticlePublisher', verbose_name='\u6587\u7ae0\u53d1\u5e03\u8005'),
        ),
        migrations.AddField(
            model_name='topiccollection',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Collection', verbose_name='\u6536\u85cf'),
        ),
        migrations.AddField(
            model_name='collection',
            name='articles',
            field=models.ManyToManyField(related_name='collections', related_query_name=b'collection', through='yqj.ArticleCollection', to='yqj.Article', verbose_name='\u6587\u7ae0'),
        ),
        migrations.AddField(
            model_name='collection',
            name='events',
            field=models.ManyToManyField(related_name='collections', related_query_name=b'collection', through='yqj.TopicCollection', to='yqj.Topic', verbose_name='\u8d28\u91cf\u4e8b\u4ef6'),
        ),
        migrations.AddField(
            model_name='articlecollection',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Collection', verbose_name='\u6536\u85cf'),
        ),
        migrations.AlterUniqueTogether(
            name='topiccollection',
            unique_together=set([('topic', 'collection')]),
        ),
        migrations.AlterUniqueTogether(
            name='articlecollection',
            unique_together=set([('article', 'collection')]),
        ),
    ]