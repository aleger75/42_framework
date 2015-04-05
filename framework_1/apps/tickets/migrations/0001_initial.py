# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('priority', models.IntegerField(choices=[(1, 'Critical'), (2, 'High'), (3, 'Normal'), (4, 'Low'), (5, 'Very low')], default=3, max_length=1)),
                ('created', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='creator')),
                ('staff', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='staff')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
