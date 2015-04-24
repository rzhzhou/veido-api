# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0002_custom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weibo',
            old_name='praise',
            new_name='attitudes_count',
        ),
        migrations.RenameField(
            model_name='weibo',
            old_name='comment',
            new_name='comments_count',
        ),
        migrations.RenameField(
            model_name='weibo',
            old_name='tansmit',
            new_name='reposts_count',
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(max_length=20, verbose_name='\u7c7b\u578b', blank=True),
            preserve_default=True,
        ),
    ]
