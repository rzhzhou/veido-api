# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0009_auto_20150722_0300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupauthuser',
            options={'verbose_name_plural': '\u7528\u6237\u7ed1\u5b9a'},
        ),
        migrations.AlterField(
            model_name='localtionscore',
            name='score',
            field=models.IntegerField(default=0, verbose_name='\u5206\u6570'),
            preserve_default=True,
        ),
    ]
