# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskmonitor', '0002_auto_20151204_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u8bed\u6599\u8bcd')),
                ('enterprise', models.ForeignKey(verbose_name='\u4f01\u4e1a', blank=True, to='riskmonitor.Enterprise', null=True)),
                ('industry', models.ForeignKey(verbose_name='\u884c\u4e1a', blank=True, to='riskmonitor.Industry', null=True)),
                ('metrics', models.ForeignKey(verbose_name='\u6307\u6807', blank=True, to='riskmonitor.Metrics', null=True)),
                ('product', models.ForeignKey(verbose_name='\u4ea7\u54c1', blank=True, to='riskmonitor.Product', null=True)),
            ],
            options={
                'db_table': 'corpus',
                'verbose_name_plural': '\u8bed\u6599\u5e93',
            },
            bases=(models.Model,),
        ),
    ]
