# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20150209_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='status',
            field=models.BooleanField(verbose_name='Opened', default=True),
            preserve_default=True,
        ),
    ]
