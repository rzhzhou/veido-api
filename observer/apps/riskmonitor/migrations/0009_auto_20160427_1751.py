# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 09:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskmonitor', '0008_auto_20160427_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='risknewspublisher',
            old_name='publisher',
            new_name='name',
        ),
    ]
