# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-31 06:23
from __future__ import unicode_literals

import uuid

import django.db.models.deletion
import django.utils.timezone
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zh_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4e2d\u6587\u540d\u79f0')),
                ('en_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u82f1\u6587\u540d\u79f0')),
                ('logo', models.URLField(verbose_name='\u56fe\u6807')),
            ],
            options={
                'db_table': 'brand',
                'verbose_name_plural': '\u54c1\u724c',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u4f01\u4e1a\u540d')),
                ('locate_x', models.FloatField(blank=True, null=True, verbose_name='\u7eac\u5ea6')),
                ('locate_y', models.FloatField(blank=True, null=True, verbose_name='\u7ecf\u5ea6')),
                ('scale', models.CharField(max_length=255, verbose_name='\u89c4\u6a21')),
                ('ccc', models.BooleanField(default=False, verbose_name='ccc\u8ba4\u8bc1')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u5730\u57df')),
            ],
            options={
                'db_table': 'enterprise',
                'verbose_name_plural': '\u4f01\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('level', models.BigIntegerField(verbose_name='\u884c\u4e1a\u5c42\u7ea7')),
                ('area', models.ManyToManyField(related_name='areas', related_query_name=b'area', to='base.Area', verbose_name='\u5730\u57df')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Industry', verbose_name='\u4e0a\u4e00\u7ea7')),
            ],
            options={
                'db_table': 'industry',
                'verbose_name_plural': '\u884c\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u6307\u6807')),
                ('level', models.BigIntegerField(verbose_name='\u7b49\u7ea7')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Metrics', verbose_name='\u4e0a\u4e00\u7ea7')),
            ],
            options={
                'db_table': 'metrics',
                'verbose_name_plural': '\u6307\u6807',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u751f\u4ea7\u4ea7\u54c1')),
                ('enterprise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Enterprise', verbose_name='\u4f01\u4e1a')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Industry', verbose_name='\u4ea7\u54c1')),
            ],
            options={
                'db_table': 'product',
                'verbose_name_plural': '\u751f\u4ea7\u4ea7\u54c1',
            },
        ),
        migrations.CreateModel(
            name='ProductKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Group')),
                ('product', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Product')),
            ],
            options={
                'db_table': 'product_keyword',
                'verbose_name_plural': '\u4ea7\u54c1\u76d1\u6d4b\u5173\u952e\u8bcd',
            },
        ),
        migrations.CreateModel(
            name='ProductMetrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.CharField(max_length=255, verbose_name='\u6743\u91cd')),
                ('metrics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Metrics', verbose_name='\u6307\u6807')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Product', verbose_name='\u4ea7\u54c1')),
            ],
            options={
                'db_table': 'metrics_product',
                'verbose_name_plural': '\u4ea7\u54c1\u6307\u6807',
            },
        ),
        migrations.CreateModel(
            name='RiskData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4f5c\u8005\u94fe\u63a5\u5730\u5740')),
                ('user_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4f5c\u8005\u540d')),
                ('content', models.TextField(blank=True, verbose_name='\u6b63\u6587')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('comment', models.CharField(max_length=255, verbose_name='\u662f\u5426\u81ea\u8425')),
                ('comment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u8bc4\u8bba\u5730\u5740')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('show_pic', models.TextField(blank=True, null=True, verbose_name='\u56fe\u7247\u8bc4\u8bba\u56fe')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='\u8bc4\u5206')),
                ('url', models.URLField(blank=True, null=True, verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=255, verbose_name='uuid')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u5730\u57df')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Brand', verbose_name='\u54c1\u724c')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Industry', verbose_name='\u884c\u4e1a')),
            ],
            options={
                'db_table': 'risk_data',
                'verbose_name_plural': '\u7535\u5546\u98ce\u9669\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='RiskNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', tinymce.models.HTMLField(blank=True, verbose_name='\u6b63\u6587')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('uuid', models.CharField(max_length=36)),
                ('feeling_factor', models.FloatField(default=-1, verbose_name='\u6b63\u8d1f\u9762')),
                ('reprinted', models.IntegerField(verbose_name='\u8f6c\u8f7d\u6570')),
                ('status', models.IntegerField(default=0, verbose_name='\u72b6\u6001')),
                ('area', models.ManyToManyField(related_name='rareas', related_query_name=b'rarea', to='base.Area', verbose_name='\u5730\u57df')),
                ('enterprise', models.ManyToManyField(related_name='enterprises', related_query_name=b'enterprise', to='riskmonitor.Enterprise', verbose_name='\u4f01\u4e1a')),
                ('industry', models.ManyToManyField(related_name='industrys', related_query_name=b'industry', to='riskmonitor.Industry', verbose_name='\u884c\u4e1a')),
            ],
            options={
                'ordering': ['-pubtime'],
                'db_table': 'risk_news',
                'verbose_name_plural': '\u98ce\u9669\u65b0\u95fb',
            },
        ),
        migrations.CreateModel(
            name='RiskNewsPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.URLField(verbose_name='\u7528\u6237\u5934\u50cf')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('brief', models.CharField(max_length=255, verbose_name='\u7b80\u4ecb')),
                ('searchmode', models.IntegerField(default=0, verbose_name='\u641c\u7d22\u65b9\u5f0f')),
            ],
            options={
                'db_table': 'risknewspublisher',
                'verbose_name_plural': '\u98ce\u9669\u65b0\u95fb\u53d1\u5e03\u8005',
            },
        ),
        migrations.CreateModel(
            name='ScoreEnterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=255, verbose_name='\u5206\u503c')),
                ('pubtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Enterprise', verbose_name='\u4f01\u4e1a')),
            ],
            options={
                'db_table': 'score_enterprise',
                'verbose_name_plural': '\u4f01\u4e1a\u5206\u503c',
            },
        ),
        migrations.CreateModel(
            name='ScoreIndustry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=255, verbose_name='\u5206\u503c')),
                ('pubtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('increment', models.IntegerField(default=0, verbose_name='\u589e\u91cf')),
                ('reducescore', models.IntegerField(default=0, verbose_name='\u6240\u51cf\u7684\u5206\u6570')),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Industry', verbose_name='\u884c\u4e1a')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'db_table': 'score_industry',
                'verbose_name_plural': '\u884c\u4e1a\u5206\u503c',
            },
        ),
        migrations.CreateModel(
            name='ScoreProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=255, verbose_name='\u5206\u503c')),
                ('pubtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Product', verbose_name='\u4ea7\u54c1')),
            ],
            options={
                'db_table': 'score_product',
                'verbose_name_plural': '\u4ea7\u54c1\u5206\u503c',
            },
        ),
        migrations.CreateModel(
            name='UserArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u5730\u57df')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'db_table': 'user_area',
                'verbose_name_plural': '\u7528\u6237\u5730\u57df\u5f31\u5173\u8054',
            },
        ),
        migrations.CreateModel(
            name='UserEnterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Enterprise', verbose_name='\u4f01\u4e1a')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'db_table': 'user_enterprise',
                'verbose_name_plural': '\u76d1\u6d4b\u4f01\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='UserIndustry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.Industry', verbose_name='\u884c\u4e1a')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'db_table': 'user_industry',
                'verbose_name_plural': '\u652f\u67f1\u884c\u4e1a',
            },
        ),
        migrations.AddField(
            model_name='risknews',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.RiskNewsPublisher', verbose_name='\u6587\u7ae0\u53d1\u5e03\u8005'),
        ),
    ]