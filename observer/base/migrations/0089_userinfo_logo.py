# Generated by Django 2.1.5 on 2019-04-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0088_nav_nav_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='logo',
            field=models.CharField(default='', max_length=225, verbose_name='logo'),
        ),
    ]