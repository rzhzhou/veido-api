# Generated by Django 2.0.3 on 2018-05-24 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_article_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='unitem',
        ),
        migrations.AddField(
            model_name='enterprise',
            name='unitem',
            field=models.CharField(default='', max_length=255, verbose_name='不合格项'),
            preserve_default=False,
        ),
    ]
