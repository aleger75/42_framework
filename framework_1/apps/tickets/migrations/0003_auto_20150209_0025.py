# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import apps.tickets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_tickets_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tickets',
            options={'verbose_name_plural': 'Tickets', 'verbose_name': 'Tickets'},
        ),
        migrations.AlterField(
            model_name='tickets',
            name='body',
            field=models.TextField(verbose_name='Description of Issue'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Critical'), (2, 'High'), (3, 'Normal'), (4, 'Low'), (5, 'Very low')], default=3, help_text='Please select a priority carefully. If unsure, leave it as "Normal".', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='staff',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='staff', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='title',
            field=models.CharField(verbose_name='Summary of the problem', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='type',
            field=models.CharField(choices=[('--------', '--------'), ('ADM', 'ADM'), ('Autre', 'Autre'), ('Boite a idee', 'Boite a idee'), ('Compte', 'Compte'), ('Intra', 'Intra'), ('Logistique', 'Logistique'), ('Moulinette', 'Moulinette'), ('Pedago', 'Pedago'), ('Sujets', 'Sujets'), ('TIG', 'TIG'), ('Vogsphere', 'Vogsphere')], default='--------', help_text='Please choose the category closest to your issue.', validators=[apps.tickets.models.validate_type], max_length=100),
            preserve_default=True,
        ),
    ]
