# Generated by Django 2.2 on 2019-04-16 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0094_remove_nav_nav_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='nav',
            name='nav_type',
            field=models.IntegerField(default=0, verbose_name='导航类型'),
        ),
    ]
