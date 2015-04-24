# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0003_auto_20150422_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='weixin',
            name='likenum',
            field=models.IntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weixin',
            name='readnum',
            field=models.IntegerField(default=0, verbose_name='\u9605\u8bfb\u6570', blank=True),
            preserve_default=False,
        ),
    ]
