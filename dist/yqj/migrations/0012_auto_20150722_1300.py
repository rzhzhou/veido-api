# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0011_auto_20150722_0333'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, verbose_name='\u5206\u6570')),
            ],
            options={
                'db_table': 'risk_score',
                'verbose_name_plural': '\u98ce\u9669\u8bc4\u5206\u5c55\u793a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tarticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255, verbose_name='\u4f5c\u8005')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898', blank=True)),
                ('url', models.URLField(verbose_name='\u7f51\u7ad9\u94fe\u63a5')),
                ('content', models.TextField(verbose_name='\u6b63\u6587', blank=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u4fe1\u606f\u6765\u6e90', blank=True)),
                ('pubtime', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('uuid', models.CharField(max_length=36)),
                ('feeling_factor', models.FloatField(default=-1, verbose_name='\u6b63\u8d1f\u9762')),
                ('website_type', models.CharField(max_length=20, verbose_name='\u8bc4\u5206', blank=True)),
                ('area', models.ForeignKey(verbose_name='\u5730\u57df', to='yqj.Area')),
                ('publisher', models.ForeignKey(verbose_name='\u6587\u7ae0\u53d1\u5e03\u8005', to='yqj.ArticlePublisher')),
            ],
            options={
                'db_table': 'article',
                'verbose_name_plural': '\u98ce\u9669\u8bc4\u5206',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='riskscore',
            name='article',
            field=models.ForeignKey(verbose_name='\u65b0\u95fb', to='yqj.Tarticle'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='article',
            name='localtion_score',
        ),
        migrations.AlterField(
            model_name='article',
            name='website_type',
            field=models.CharField(max_length=20, verbose_name='\u8bc4\u5206', blank=True),
            preserve_default=True,
        ),
    ]
