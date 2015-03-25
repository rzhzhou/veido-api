# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0012_auto_20150325_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='feeling_factor',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
