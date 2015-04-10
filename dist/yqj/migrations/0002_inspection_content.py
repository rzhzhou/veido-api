# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='content',
            field=models.TextField(verbose_name='\u6b63\u6587', blank=True),
            preserve_default=True,
        ),
    ]
