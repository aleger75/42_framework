# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_auto_20150210_0131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickets',
            name='resolved',
        ),
    ]
