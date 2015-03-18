# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0003_auto_20150318_0734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='passwod',
            new_name='password',
        ),
    ]
