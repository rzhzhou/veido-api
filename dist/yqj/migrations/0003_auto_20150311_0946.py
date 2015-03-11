# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0002_auto_20150311_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realteddata',
            name='uuid',
            field=models.CharField(max_length=36, verbose_name='uuid'),
            preserve_default=True,
        ),
    ]
