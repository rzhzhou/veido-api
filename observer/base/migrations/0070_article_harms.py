# Generated by Django 2.1.3 on 2019-02-26 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0069_auto_20190225_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='harms',
            field=models.ManyToManyField(to='base.Harm'),
        ),
    ]
