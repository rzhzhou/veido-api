# Generated by Django 2.1.5 on 2019-01-23 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0064_auto_20190121_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='nav',
            name='component',
            field=models.CharField(default='', max_length=50, verbose_name='组件'),
        ),
        migrations.AlterField(
            model_name='nav',
            name='href',
            field=models.CharField(default='', max_length=50, verbose_name='链接'),
        ),
    ]