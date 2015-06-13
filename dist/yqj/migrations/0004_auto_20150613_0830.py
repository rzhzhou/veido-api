# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0003_auto_20150613_0759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
    ]
