# Generated by Django 2.1.3 on 2018-12-19 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_corpus_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpus_categories',
            name='category_id',
            field=models.CharField(max_length=5, verbose_name='信息类别'),
        ),
    ]