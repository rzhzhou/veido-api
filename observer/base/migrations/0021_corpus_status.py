# Generated by Django 2.0.7 on 2018-08-07 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_article_industry_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpus',
            name='status',
            field=models.IntegerField(default=0, verbose_name='状态'),
        ),
    ]