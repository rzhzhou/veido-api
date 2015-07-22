# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0005_auto_20150615_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth', models.CharField(max_length=255, verbose_name='\u7528\u6237\u540d')),
                ('group', models.ForeignKey(verbose_name='\u5206\u7ec4', to='yqj.Group')),
            ],
            options={
                'db_table': 'group_authuser',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocaltionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(null=True, verbose_name='\u5206\u6570', blank=True)),
                ('article', models.ForeignKey(verbose_name='\u65b0\u95fb', to='yqj.Article')),
                ('groupauthuser', models.ForeignKey(verbose_name='\u7528\u6237', to='yqj.GroupAuthUser')),
            ],
            options={
                'db_table': 'localtion_score',
                'verbose_name_plural': '\u672c\u5730\u8bc4\u5206',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, verbose_name='\u5bc6\u7801'),
            preserve_default=True,
        ),
    ]
