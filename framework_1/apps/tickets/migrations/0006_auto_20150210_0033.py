# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20150209_2217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-answer_date']},
        ),
        migrations.AlterModelOptions(
            name='tickets',
            options={'verbose_name': 'Tickets', 'verbose_name_plural': 'Tickets', 'ordering': ['priority', 'created']},
        ),
        migrations.AlterField(
            model_name='tickets',
            name='staff',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='staff'),
            preserve_default=True,
        ),
    ]
