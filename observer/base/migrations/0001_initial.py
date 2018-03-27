# Generated by Django 2.0.3 on 2018-03-21 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='行业编号')),
                ('name', models.CharField(max_length=100, verbose_name='行业名称')),
                ('level', models.IntegerField(verbose_name='行业等级')),
                ('desc', models.CharField(blank=True, default='', max_length=255, verbose_name='行业描述')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Industry', verbose_name='上一级')),
            ],
            options={
                'verbose_name_plural': '行业',
            },
        ),
    ]
