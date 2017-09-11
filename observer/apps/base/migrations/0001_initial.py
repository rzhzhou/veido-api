# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-11 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativePenalties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u8005')),
                ('case_name', models.CharField(default='', max_length=255, verbose_name='\u6848\u4ef6\u540d\u79f0')),
                ('illegal_behavior', models.CharField(default='', max_length=255, verbose_name='\u8fdd\u6cd5\u884c\u4e3a')),
                ('punishment_basis', models.CharField(default='', max_length=255, verbose_name='\u5904\u7f5a\u4f9d\u636e')),
                ('punishment_result', models.CharField(default='', max_length=255, verbose_name='\u5904\u7f5a\u7ed3\u679c')),
                ('penalty_organ', models.CharField(max_length=255, verbose_name='\u5904\u7f5a\u673a\u5173')),
                ('credit_code', models.CharField(default='', max_length=255, verbose_name='\u7edf\u4e00\u793e\u4f1a\u4fe1\u7528\u4ee3\u7801')),
                ('area', models.CharField(default='', max_length=255, verbose_name='\u5730\u57df')),
                ('enterprise', models.CharField(default='', max_length=255, verbose_name='\u5904\u7f5a\u4f01\u4e1a')),
                ('industry', models.CharField(default='', max_length=255, verbose_name='\u884c\u4e1a')),
            ],
            options={
                'verbose_name_plural': '\u884c\u653f\u5904\u7f5a',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('level', models.BigIntegerField(verbose_name='\u7b49\u7ea7')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u4e0a\u4e00\u7ea7')),
            ],
            options={
                'verbose_name_plural': '\u5730\u57df',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('source', models.CharField(blank=True, max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90')),
                ('reprinted', models.IntegerField(verbose_name='\u8f6c\u8f7d\u6570')),
                ('feeling_factor', models.FloatField(default=-1, verbose_name='\u6b63\u8d1f\u9762')),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('risk_keyword', models.CharField(blank=True, max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('invalid_keyword', models.CharField(blank=True, max_length=255, verbose_name='\u65e0\u6548\u5173\u952e\u8bcd')),
                ('status', models.IntegerField(default=0, verbose_name='\u72b6\u6001')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u5730\u57df')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('remark', models.CharField(blank=True, max_length=255, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riskword', models.TextField(default='', max_length=255, verbose_name='\u98ce\u9669\u8bed\u6599\u8bcd')),
                ('invalidword', models.TextField(default='', max_length=255, verbose_name='\u65e0\u6548\u8bcd')),
            ],
            options={
                'verbose_name_plural': '\u8bed\u6599\u5e93',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u4f01\u4e1a\u540d')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u5730\u57df')),
            ],
            options={
                'verbose_name_plural': '\u4f01\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='\u7f16\u7801')),
                ('level', models.BigIntegerField(verbose_name='\u884c\u4e1a\u5c42\u7ea7')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='\u4e0a\u4e00\u7ea7')),
            ],
            options={
                'verbose_name_plural': '\u884c\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(blank=True, null=True, verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('qualitied', models.FloatField(default=1.0, verbose_name='\u5408\u683c\u7387')),
                ('unitem', models.TextField(default='', verbose_name='\u4e0d\u5408\u683c\u9879')),
                ('brand', models.CharField(default='', max_length=255, verbose_name='\u5546\u6807')),
                ('product', models.CharField(default='', max_length=255, verbose_name='\u4ea7\u54c1\u79cd\u7c7b')),
                ('publisher', models.CharField(max_length=255, verbose_name='\u62bd\u68c0\u5355\u4f4d')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area', verbose_name='\u62bd\u68c0\u5730\u57df')),
                ('enterprise_qualified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualitieds', to='base.Enterprise', verbose_name='\u5408\u683c\u4f01\u4e1a')),
                ('enterprise_unqualified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unqualifieds', to='base.Enterprise', verbose_name='\u4e0d\u5408\u683c\u4f01\u4e1a')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='\u884c\u4e1a')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u98ce\u9669\u62bd\u68c0',
            },
        ),
        migrations.AddField(
            model_name='corpus',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ArticleCategory', verbose_name='\u6587\u7ae0\u7c7b\u522b'),
        ),
        migrations.AddField(
            model_name='article',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Enterprise', verbose_name='\u4f01\u4e1a'),
        ),
        migrations.AddField(
            model_name='article',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='\u884c\u4e1a'),
        ),
    ]
