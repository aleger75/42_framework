# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='type',
            field=models.CharField(default='--------', max_length=100, choices=[('ADM', 'ADM'), ('Autre', 'Autre'), ('Boite a idee', 'Boite a idee'), ('Compte', 'Compte'), ('Intra', 'Intra'), ('Logistique', 'Logistique'), ('Moulinette', 'Moulinette'), ('Pedago', 'Pedago'), ('Sujets', 'Sujets'), ('TIG', 'TIG'), ('Vogsphere', 'Vogsphere')]),
            preserve_default=True,
        ),
    ]
