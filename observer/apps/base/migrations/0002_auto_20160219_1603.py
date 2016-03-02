# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskmonitor', '0001_initial'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='industry',
            field=models.ManyToManyField(related_query_name=b'industry', related_name='industrys', to='riskmonitor.Industry', blank=True, null=True, verbose_name='\u884c\u4e1a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='score',
            field=models.ForeignKey(verbose_name='\u5206\u503c', to='riskmonitor.Score'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='group',
            field=models.ForeignKey(verbose_name='\u5206\u7ec4', to='base.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='risk',
            field=models.ForeignKey(verbose_name='\u98ce\u9669\u5feb\u8baf', to='base.Risk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupauthuser',
            name='group',
            field=models.ForeignKey(verbose_name='\u5206\u7ec4', to='base.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customkeyword',
            name='custom',
            field=models.ForeignKey(default='', blank=True, to='base.Custom', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customkeyword',
            name='group',
            field=models.ForeignKey(to='base.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='custom',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'custom', related_name='customs', to='base.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='custom',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'custom', related_name='customs', to='base.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='custom',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'custom', related_name='customs', to='base.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'collection', related_name='collections', to='base.Article', through='base.ArticleCollection', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='events',
            field=models.ManyToManyField(related_query_name=b'collection', related_name='collections', to='base.Topic', through='base.TopicCollection', blank=True, null=True, verbose_name='\u8d28\u91cf\u4e8b\u4ef6'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'category', related_name='categorys', to='base.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecollection',
            name='article',
            field=models.ForeignKey(verbose_name='\u6587\u7ae0', to='base.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecollection',
            name='collection',
            field=models.ForeignKey(verbose_name='\u6536\u85cf', to='base.Collection'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articlecollection',
            unique_together=set([('article', 'collection')]),
        ),
        migrations.AddField(
            model_name='article',
            name='area',
            field=models.ForeignKey(verbose_name='\u5730\u57df', to='base.Area'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='publisher',
            field=models.ForeignKey(verbose_name='\u6587\u7ae0\u53d1\u5e03\u8005', to='base.ArticlePublisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='parent',
            field=models.ForeignKey(verbose_name='\u4e0a\u4e00\u7ea7', blank=True, to='base.Area', null=True),
            preserve_default=True,
        ),
    ]
