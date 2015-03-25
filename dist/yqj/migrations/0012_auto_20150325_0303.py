# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yqj', '0011_remove_inspection_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepublisher',
            old_name='serachmode',
            new_name='searchmode',
        ),
    ]
