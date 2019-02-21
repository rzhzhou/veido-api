# Generated by Django 2.1.3 on 2019-01-04 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0045_auto_20190103_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpuscategories',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
            preserve_default=False,
        ),
    ]