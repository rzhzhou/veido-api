# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='realteddata',
            name='weixin',
            field=models.ManyToManyField(related_query_name=b'relateddatas', related_name='relateddata', to='yqj.Weixin', blank=True, null=True, verbose_name='\u5fae\u4fe1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='realteddata',
            name='weibo',
            field=models.ManyToManyField(related_query_name=b'relateddatas', related_name='relateddata', to='yqj.Weibo', blank=True, null=True, verbose_name='\u5fae\u535a'),
            preserve_default=True,
        ),
    ]
