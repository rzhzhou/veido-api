# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-13 06:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskmonitor', '0003_auto_20160413_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskinspection',
            name='area',
        ),
        migrations.RemoveField(
            model_name='riskinspection',
            name='enterprise',
        ),
        migrations.RemoveField(
            model_name='riskinspection',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='riskinspection',
            name='publisher',
        ),
        migrations.DeleteModel(
            name='RiskInspection',
        ),
        migrations.DeleteModel(
            name='RiskInspectionPublisher',
        ),
    ]