# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0004_auto_20150318_0829'),
    ]

    operations = [
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
            name='TopicCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('collection', models.ForeignKey(verbose_name='\u6536\u85cf', to='yqj.Collection')),
                ('topic', models.ForeignKey(verbose_name='\u8d28\u91cf\u4e8b\u4ef6', to='yqj.Topic')),
            ],
            options={
                'db_table': 'topic_collection',
                'verbose_name_plural': '\u8d28\u91cf\u4e8b\u4ef6\u6536\u85cf',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='topiccollection',
            unique_together=set([('topic', 'collection')]),
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
    ]
