# Generated by Django 2.1.3 on 2019-04-16 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0093_keywordsstatistical'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordsstatistical',
            name='events',
            field=models.ForeignKey(blank=True, default=3, on_delete=django.db.models.deletion.CASCADE, to='base.Events', verbose_name='事件'),
        ),
    ]