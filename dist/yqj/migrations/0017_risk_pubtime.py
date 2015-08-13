# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0016_auto_20150813_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='risk',
            name='pubtime',
            field=models.DateTimeField(null=True, verbose_name='\u53d1\u5e03\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
