# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-08 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('origin', '0002_industry_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='\u7f16\u7801'),
        ),
    ]
