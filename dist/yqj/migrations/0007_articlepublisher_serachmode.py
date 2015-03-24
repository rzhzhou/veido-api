# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0006_auto_20150320_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepublisher',
            name='serachmode',
            field=models.IntegerField(default=0, verbose_name='\u641c\u7d22\u65b9\u5f0f'),
            preserve_default=True,
        ),
    ]
