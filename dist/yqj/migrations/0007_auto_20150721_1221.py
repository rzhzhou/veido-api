# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0006_auto_20150721_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localtionscore',
            name='groupauthuser',
        ),
        migrations.AddField(
            model_name='article',
            name='localtion_score',
            field=models.FloatField(null=True, verbose_name='\u8bc4\u5206', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='area',
            field=models.ForeignKey(default=1, verbose_name='\u5730\u57df', to='yqj.Area'),
            preserve_default=False,
        ),
    ]
