# Generated by Django 2.2 on 2019-05-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0108_historyindustries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='majorindustries',
            name='ccc',
        ),
        migrations.RemoveField(
            model_name='majorindustries',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='majorindustries',
            name='licence',
        ),
        migrations.AlterField(
            model_name='historyindustries',
            name='status',
            field=models.IntegerField(default=0, verbose_name='状态'),
        ),
    ]
