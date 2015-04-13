# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('articles', models.ManyToManyField(related_query_name=b'customs', related_name='custom', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
                ('group', models.ManyToManyField(related_query_name=b'customs', related_name='custom', to='yqj.Group', blank=True, null=True, verbose_name='\u6240\u5c5e\u7ec4')),
                ('weibo', models.ManyToManyField(related_query_name=b'customs', related_name='custom', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a')),
                ('weixin', models.ManyToManyField(related_query_name=b'customs', related_name='custom', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1')),
            ],
            options={
                'db_table': 'custom',
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b',
            },
            bases=(models.Model,),
        ),
    ]
