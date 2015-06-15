# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0004_auto_20150613_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
                ('custom', models.ForeignKey(default='', blank=True, to='yqj.Custom', null=True)),
                ('group', models.ForeignKey(to='yqj.Group')),
            ],
            options={
                'db_table': 'custom_keyword',
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b\u5173\u952e\u8bcd',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
                ('group', models.ForeignKey(to='yqj.Group')),
                ('product', models.ForeignKey(default='', blank=True, to='yqj.Product', null=True)),
            ],
            options={
                'db_table': 'product_keyword',
                'verbose_name_plural': '\u4ea7\u54c1\u76d1\u6d4b\u5173\u952e\u8bcd',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='custom',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='group',
        ),
        migrations.DeleteModel(
            name='Keyword',
        ),
    ]
