# Generated by Django 2.1.3 on 2019-03-04 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0072_auto_20190301_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='harm',
        ),
        migrations.AddField(
            model_name='harm',
            name='article',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Article', verbose_name='文章'),
        ),
    ]