# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='custom',
            field=models.ForeignKey(default='', blank=True, to='yqj.Custom', null=True),
            preserve_default=True,
        ),
    ]
