# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_auto_20150210_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='staff',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True, related_name='staff'),
            preserve_default=True,
        ),
    ]
