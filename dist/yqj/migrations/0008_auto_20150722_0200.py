# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0007_auto_20150721_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localtionscore',
            name='area',
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='group',
            field=models.ForeignKey(default=1, verbose_name='\u5206\u7ec4', to='yqj.Group'),
            preserve_default=False,
        ),
    ]
