# Generated by Django 2.1.4 on 2019-01-15 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0057_inspection2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inspection',
        ),
        migrations.DeleteModel(
            name='InspectionEnterprise',
        ),
    ]
