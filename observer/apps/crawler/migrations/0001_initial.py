# Generated by Django 2.0 on 2017-12-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255, verbose_name='应用')),
                ('sub_app', models.CharField(blank=True, max_length=255, verbose_name='子应用')),
                ('file', models.CharField(max_length=255, verbose_name='文件名')),
                ('rank', models.IntegerField(verbose_name='等级')),
                ('url', models.URLField(verbose_name='链接')),
                ('data', models.TextField(blank=True, verbose_name='数据')),
                ('priority', models.IntegerField(verbose_name='优先级')),
                ('interval', models.IntegerField(verbose_name='周期')),
                ('timeout', models.IntegerField(verbose_name='超时时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('last_run', models.DateTimeField(verbose_name='上次执行结束时间')),
                ('next_run', models.DateTimeField(verbose_name='下次运行开始时间')),
                ('status', models.IntegerField(verbose_name='状态')),
            ],
            options={
                'ordering': ['-rank', 'next_run', '-priority'],
                'verbose_name_plural': '爬虫任务',
            },
        ),
        migrations.CreateModel(
            name='TaskConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255, verbose_name='应用')),
                ('sub_app', models.CharField(blank=True, max_length=255, verbose_name='子应用')),
                ('file', models.CharField(max_length=255, verbose_name='文件名')),
                ('rank', models.IntegerField(verbose_name='等级')),
                ('priority', models.IntegerField(verbose_name='优先级')),
                ('interval', models.IntegerField(verbose_name='周期')),
                ('timeout', models.IntegerField(verbose_name='超时时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.IntegerField(verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '爬虫任务配置',
            },
        ),
    ]
