# Generated by Django 2.1.7 on 2019-02-25 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0071_govreports'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='govreports',
            name='areas',
        ),
        migrations.DeleteModel(
            name='Govreports',
        ),
    ]
