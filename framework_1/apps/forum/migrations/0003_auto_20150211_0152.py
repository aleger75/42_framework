# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150211_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymeta',
            name='slug',
            field=models.SlugField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
