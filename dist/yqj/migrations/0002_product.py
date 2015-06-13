# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.CharField(max_length=255, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81')),
                ('articles', models.ManyToManyField(related_query_name=b'products', related_name='product', to='yqj.Article', blank=True, null=True, verbose_name='\u6587\u7ae0')),
            ],
            options={
                'db_table': 'product',
                'verbose_name_plural': '\u4ea7\u54c1\u76d1\u6d4b',
            },
            bases=(models.Model,),
        ),
    ]
