# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0015_auto_20150401_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='keywords',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5173\u952e\u8bcd'),
            preserve_default=True,
        ),
    ]
