# Generated by Django 2.0.7 on 2018-08-03 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20180802_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='industry_id',
            field=models.IntegerField(default=0, verbose_name='产品类别'),
        ),
    ]