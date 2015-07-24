# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0008_auto_20150722_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localtionscore',
            name='article',
            field=models.OneToOneField(verbose_name='\u65b0\u95fb', to='yqj.Article'),
            preserve_default=True,
        ),
    ]
