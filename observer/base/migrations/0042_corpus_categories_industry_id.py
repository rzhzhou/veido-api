# Generated by Django 2.1.3 on 2018-12-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_merge_20181227_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpus_categories',
            name='industry_id',
            field=models.IntegerField(default=0, verbose_name='产品类别'),
        ),
    ]
