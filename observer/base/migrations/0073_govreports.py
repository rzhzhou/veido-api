# Generated by Django 2.1.7 on 2019-02-25 07:19

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0072_auto_20190225_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Govreports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('content', tinymce.models.HTMLField(verbose_name='内容')),
                ('province_level', models.CharField(default='', max_length=255, verbose_name='级别')),
                ('year', models.CharField(default='', max_length=255, verbose_name='年份')),
                ('areas', models.ManyToManyField(to='base.Area')),
            ],
            options={
                'verbose_name_plural': '政府报告',
            },
        ),
    ]
