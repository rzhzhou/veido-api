# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u4f01\u4e1a\u540d')),
                ('locate_x', models.FloatField(null=True, verbose_name='\u7eac\u5ea6', blank=True)),
                ('locate_y', models.FloatField(null=True, verbose_name='\u7ecf\u5ea6', blank=True)),
                ('scale', models.CharField(max_length=255, verbose_name='\u89c4\u6a21')),
                ('ccc', models.BooleanField(default=False, verbose_name='ccc\u8ba4\u8bc1')),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='base.Area')),
            ],
            options={
                'db_table': 'enterprise',
                'verbose_name_plural': '\u4f01\u4e1a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnterpriseProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=255, verbose_name='\u522b\u540d')),
                ('enterprise', models.ForeignKey(verbose_name='\u4f01\u4e1a', to='riskmonitor.Enterprise')),
                ('product', models.ForeignKey(verbose_name='\u4ea7\u54c1', to='base.Product')),
            ],
            options={
                'db_table': 'enterprise_product',
                'verbose_name_plural': '\u4f01\u4e1a\u4ea7\u54c1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('level', models.BigIntegerField(verbose_name='\u884c\u4e1a\u5c42\u7ea7')),
                ('parent', models.ForeignKey(verbose_name='\u4e0a\u4e00\u7ea7', blank=True, to='riskmonitor.Industry', null=True)),
            ],
            options={
                'db_table': 'industry',
                'verbose_name_plural': '\u884c\u4e1a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u6307\u6807')),
                ('level', models.BigIntegerField(verbose_name='\u7b49\u7ea7')),
                ('parent', models.ForeignKey(verbose_name='\u4e0a\u4e00\u7ea7', blank=True, to='riskmonitor.Metrics', null=True)),
            ],
            options={
                'db_table': 'metrics',
                'verbose_name_plural': '\u6307\u6807',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetricsProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.CharField(max_length=255, verbose_name='\u6743\u91cd')),
                ('metrics', models.ForeignKey(verbose_name='\u6307\u6807', to='riskmonitor.Metrics')),
                ('product', models.ForeignKey(verbose_name='\u4ea7\u54c1', to='base.Product')),
            ],
            options={
                'db_table': 'metrics_product',
                'verbose_name_plural': '\u4ea7\u54c1\u6307\u6807',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
                ('group', models.ForeignKey(to='base.Group')),
                ('product', models.ForeignKey(default='', blank=True, to='base.Product', null=True)),
            ],
            options={
                'db_table': 'product_keyword',
                'verbose_name_plural': '\u4ea7\u54c1\u76d1\u6d4b\u5173\u952e\u8bcd',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.CharField(max_length=255, verbose_name='\u5206\u503c')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
            ],
            options={
                'db_table': 'score',
                'verbose_name_plural': '\u5206\u503c',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='industry',
            name='score',
            field=models.ForeignKey(verbose_name='\u5206\u503c', blank=True, to='riskmonitor.Score', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterpriseproduct',
            name='score',
            field=models.ForeignKey(verbose_name='\u5206\u503c', to='riskmonitor.Score'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprise',
            name='score',
            field=models.ForeignKey(verbose_name='\u5206\u503c', to='riskmonitor.Score'),
            preserve_default=True,
        ),
    ]
