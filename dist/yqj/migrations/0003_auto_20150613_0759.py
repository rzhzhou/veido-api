# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'category', related_name='categorys', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='custom',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'custom', related_name='customs', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='custom',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'custom', related_name='customs', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='custom',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'custom', related_name='customs', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'product', related_name='products', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relateddata',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'relateddata', related_name='relateddatas', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relateddata',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'relateddata', related_name='relateddatas', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relateddata',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'relateddata', related_name='relateddatas', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='articles',
            field=models.ManyToManyField(related_query_name=b'topic', related_name='topics', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'topic', related_name='topics', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'topic', related_name='topics', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
    ]
