# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0015_auto_20150804_0741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarticle',
            name='area',
        ),
        migrations.RemoveField(
            model_name='tarticle',
            name='publisher',
        ),
        migrations.DeleteModel(
            name='Tarticle',
        ),
        migrations.RemoveField(
            model_name='localtionscore',
            name='lrisk',
        ),
        migrations.RemoveField(
            model_name='riskscore',
            name='trisk',
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='risk',
            field=models.ForeignKey(default=0, verbose_name='\u98ce\u9669\u5feb\u8baf', to='yqj.Risk'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='riskscore',
            name='risk',
            field=models.ForeignKey(default=0, verbose_name='\u98ce\u9669\u5feb\u8baf', to='yqj.Risk'),
            preserve_default=False,
        ),
    ]
