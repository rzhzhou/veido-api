# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-03 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origin', '0013_auto_20160912_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='issues',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='\u98ce\u9669\u4e8b\u9879'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='product_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='\u98ce\u9669\u4ea7\u54c1\u540d\u79f0'),
        ),
    ]