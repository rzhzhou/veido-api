# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-09 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskmonitor', '0002_auto_20170608_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaindustry',
            name='status',
            field=models.CharField(default='', max_length=255, verbose_name='\u72b6\u6001'),
        )
    ]