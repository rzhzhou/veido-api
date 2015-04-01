# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0013_article_feeling_factor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='feeling_factor',
            field=models.FloatField(default=1, verbose_name='\u6b63\u8d1f\u9762'),
            preserve_default=True,
        ),
    ]
