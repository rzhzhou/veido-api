# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-23 02:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riskmonitor', '0001_initial'),
        ('corpus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corpus',
            name='industry',
        ),
        migrations.AddField(
            model_name='corpus',
            name='user_industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riskmonitor.UserIndustry', verbose_name='\u884c\u4e1a'),
        ),
    ]
