# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_remove_tickets_resolved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tickets',
            options={'verbose_name': 'Tickets', 'ordering': ['-status', 'priority', 'created'], 'verbose_name_plural': 'Tickets'},
        ),
    ]
