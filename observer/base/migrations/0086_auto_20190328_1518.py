# Generated by Django 2.1.3 on 2019-03-28 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0085_auto_20190328_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventsmedia',
            old_name='article',
            new_name='articles',
        ),
    ]
