# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0005_auto_20150320_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='area',
            field=models.ForeignKey(default=1, verbose_name='\u5730\u57df', to='yqj.Area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='source',
            field=models.CharField(max_length=255, verbose_name='\u9996\u53d1\u5a92\u4f53', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='area',
            field=models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlecategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u540d\u79f0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='abstract',
            field=models.TextField(verbose_name='\u7b80\u4ecb', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weibo',
            name='area',
            field=models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weixin',
            name='area',
            field=models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area'),
            preserve_default=True,
        ),
    ]
