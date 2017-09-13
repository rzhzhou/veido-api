# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-13 02:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0\u6536\u85cf',
            },
        ),
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searchkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
            ],
            options={
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b',
            },
        ),
        migrations.CreateModel(
            name='CustomKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newkeyword', models.CharField(max_length=255, verbose_name='\u5173\u952e\u8bcd')),
                ('review', models.CharField(default='', max_length=255, verbose_name='\u5ba1\u6838')),
                ('custom', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='yqj.Custom')),
            ],
            options={
                'verbose_name_plural': '\u6307\u5b9a\u76d1\u6d4b\u5173\u952e\u8bcd',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '\u8206\u60c5\u673a\u7528\u6237\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='GroupAuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth', models.CharField(max_length=255, verbose_name='\u7528\u6237\u540d')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group', verbose_name='\u5206\u7ec4')),
            ],
            options={
                'verbose_name_plural': '\u7528\u6237\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='LocaltionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='\u5206\u6570')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Article', verbose_name='\u6587\u7ae0')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group', verbose_name='\u5206\u7ec4')),
            ],
            options={
                'verbose_name_plural': '\u672c\u5730\u76f8\u5173\u5ea6',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='\u767b\u5f55\u540d')),
                ('password', models.CharField(max_length=255, verbose_name='\u5bc6\u7801')),
                ('salt', models.CharField(max_length=255)),
                ('isAdmin', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': '\u8206\u60c5\u673a\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='yqj.User')),
            ],
            bases=('yqj.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Area'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group'),
        ),
        migrations.AddField(
            model_name='customkeyword',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yqj.Group'),
        ),
        migrations.AddField(
            model_name='articlecollection',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yqj.User', verbose_name='\u7528\u6237'),
        ),
    ]
