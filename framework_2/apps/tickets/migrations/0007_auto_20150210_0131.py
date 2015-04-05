# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_auto_20150210_0033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['answer_date']},
        ),
        migrations.AlterField(
            model_name='tickets',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
