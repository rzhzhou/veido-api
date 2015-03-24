# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0010_user_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='status',
        ),
    ]
