# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0002_auto_20150318_0235'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=20, verbose_name='\u767b\u5f55\u540d')),
                ('passwod', models.CharField(max_length=255, verbose_name='hash\u5bc6\u7801')),
                ('salt', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='yqj.User')),
            ],
            options={
            },
            bases=('yqj.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(to='yqj.Area'),
            preserve_default=True,
        ),
    ]
