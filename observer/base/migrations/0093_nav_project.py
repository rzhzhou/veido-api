# Generated by Django 2.2 on 2019-04-16 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0092_auto_20190402_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='nav',
            name='project',
            field=models.IntegerField(default=0, verbose_name='所属项目'),
        ),
    ]
