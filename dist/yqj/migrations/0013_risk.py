# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0012_auto_20150722_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('abstract', models.TextField(verbose_name='\u7b80\u4ecb', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True)),
                ('keywords', models.CharField(default='', max_length=255, verbose_name='\u5173\u952e\u8bcd', blank=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
                ('articles', models.ManyToManyField(related_query_name=b'risk', related_name='risks', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
                ('weibo', models.ManyToManyField(related_query_name=b'risk', related_name='risks', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a')),
                ('weixin', models.ManyToManyField(related_query_name=b'risk', related_name='risks', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1')),
            ],
            options={
                'db_table': 'risk',
                'verbose_name_plural': '\u98ce\u9669\u5feb\u8baf',
            },
            bases=(models.Model,),
        ),
    ]
