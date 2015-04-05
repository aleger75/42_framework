# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0003_auto_20150209_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('answer', models.TextField()),
                ('answer_date', models.DateTimeField(auto_now_add=True)),
                ('answer_creator', models.ForeignKey(related_name='answer_creator', to=settings.AUTH_USER_MODEL)),
                ('related', models.ForeignKey(to='tickets.Tickets')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tickets',
            name='resolved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickets',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
