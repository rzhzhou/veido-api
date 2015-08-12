# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0014_auto_20150804_0632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='localtionscore',
            options={'verbose_name_plural': '\u672c\u5730\u8bc4\u5206\u5c55\u793a'},
        ),
        migrations.AlterModelOptions(
            name='tarticle',
            options={'verbose_name_plural': '\u98cedf'},
        ),
        migrations.RemoveField(
            model_name='localtionscore',
            name='risk',
        ),
        migrations.RemoveField(
            model_name='riskscore',
            name='article',
        ),
        migrations.AddField(
            model_name='localtionscore',
            name='lrisk',
            field=models.ForeignKey(default=1, verbose_name='\u98ce\u9669\u5feb\u8baf', to='yqj.LRisk'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='riskscore',
            name='trisk',
            field=models.ForeignKey(default=1, verbose_name='\u65b0\u95fb', to='yqj.TRisk'),
            preserve_default=False,
        ),
    ]
