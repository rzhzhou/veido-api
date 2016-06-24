# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0002_auto_20160624_1102'),
        ('origin', '0006_auto_20160624_1102'),
        ('riskmonitor', '0015_auto_20160520_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enterprise',
            name='area',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='parent',
        ),
        migrations.AlterField(
            model_name='consumeindex',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AlterField(
            model_name='manageindex',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AlterField(
            model_name='product',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='origin.Enterprise', verbose_name='\u4f01\u4e1a'),
        ),
        migrations.AlterField(
            model_name='product',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u4ea7\u54c1'),
        ),
        migrations.AlterField(
            model_name='riskdata',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AlterField(
            model_name='risknews',
            name='enterprise',
            field=models.ManyToManyField(related_name='enterprises', related_query_name=b'enterprise', to='origin.Enterprise', verbose_name='\u4f01\u4e1a'),
        ),
        migrations.AlterField(
            model_name='risknews',
            name='industry',
            field=models.ManyToManyField(related_name='industrys', related_query_name=b'industry', to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AlterField(
            model_name='scoreenterprise',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Enterprise', verbose_name='\u4f01\u4e1a'),
        ),
        migrations.AlterField(
            model_name='scoreindustry',
            name='industry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AlterField(
            model_name='societyindex',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.AlterField(
            model_name='userenterprise',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Enterprise', verbose_name='\u4f01\u4e1a'),
        ),
        migrations.AlterField(
            model_name='userindustry',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='origin.Industry', verbose_name='\u884c\u4e1a'),
        ),
        migrations.DeleteModel(
            name='Enterprise',
        ),
        migrations.DeleteModel(
            name='Industry',
        ),
    ]
