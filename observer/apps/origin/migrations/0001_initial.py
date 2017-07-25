# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 01:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('level', models.BigIntegerField(verbose_name='\u7b49\u7ea7')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u4e0a\u4e00\u7ea7')),
            ],
            options={
                'verbose_name_plural': '\u5730\u57df',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u4f01\u4e1a\u540d')),
                ('product_name', models.CharField(default='', max_length=255, verbose_name='\u98ce\u9669\u4ea7\u54c1\u540d\u79f0')),
                ('issues', models.CharField(default='', max_length=255, verbose_name='\u98ce\u9669\u4e8b\u9879')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
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
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u4e0a\u4e00\u7ea7')),
            ],
            options={
                'verbose_name_plural': '\u884c\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='IndustryScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.BigIntegerField(verbose_name='\u5206\u503c')),
                ('time', models.DateField(verbose_name='\u65e5\u671f')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Area', verbose_name='\u5730\u57df')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a')),
            ],
            options={
                'verbose_name_plural': '\u884c\u4e1a\u5206\u503c',
            },
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('url', models.URLField(blank=True, null=True, verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(default='', verbose_name='\u6b63\u6587')),
                ('pubtime', models.DateTimeField(blank=True, null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('qualitied', models.FloatField(default=1.0, verbose_name='\u5408\u683c\u7387')),
                ('unitem', models.TextField(default='', verbose_name='\u4e0d\u5408\u683c\u9879')),
                ('brand', models.CharField(default='', max_length=255, verbose_name='\u5546\u6807')),
                ('product', models.CharField(default='', max_length=255, verbose_name='\u4ea7\u54c1\u79cd\u7c7b')),
                ('area', models.ManyToManyField(related_name='areas', related_query_name='area', to='origin.Area', verbose_name='\u62bd\u68c0\u5730\u57df')),
                ('enterprise_qualified', models.ManyToManyField(blank=True, related_name='enterprises_qualified', related_query_name='enterprise_qualified', to='origin.Enterprise', verbose_name='\u5408\u683c\u4f01\u4e1a')),
                ('enterprise_unqualified', models.ManyToManyField(blank=True, related_name='enterprises_unqualified', related_query_name='enterprise_unqualified', to='origin.Enterprise', verbose_name='\u4e0d\u5408\u683c\u4f01\u4e1a')),
                ('industry', models.ManyToManyField(to='origin.Industry', verbose_name='\u884c\u4e1a')),
            ],
            options={
                'ordering': ['-pubtime'],
                'verbose_name_plural': '\u98ce\u9669\u62bd\u68c0',
            },
        ),
        migrations.CreateModel(
            name='InspectionPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u62bd\u68c0\u5355\u4f4d')),
            ],
            options={
                'verbose_name_plural': '\u62bd\u68c0\u5355\u4f4d',
            },
        ),
        migrations.AddField(
            model_name='inspection',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.InspectionPublisher', verbose_name='\u62bd\u68c0\u5355\u4f4d'),
        ),
    ]
