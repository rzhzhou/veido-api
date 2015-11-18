# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cacheconf',
            name='task',
            field=models.CharField(max_length=255, null=True, verbose_name='\u4efb\u52a1', blank=True),
            preserve_default=True,
        ),
    ]
