# Generated by Django 2.1.7 on 2019-02-25 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0069_auto_20190225_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='govreports',
            name='areas',
        ),
        migrations.DeleteModel(
            name='GovReports',
        ),
    ]