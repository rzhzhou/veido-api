# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0004_articlecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='weibo',
            name='comment',
            field=models.IntegerField(default=123, verbose_name='\u8bc4\u8bba\u91cf', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weibo',
            name='praise',
            field=models.IntegerField(default=123, verbose_name='\u70b9\u8d5e\u6570', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weibo',
            name='tansmit',
            field=models.IntegerField(default=123, verbose_name='\u8f6c\u53d1\u91cf', blank=True),
            preserve_default=False,
        ),
    ]
