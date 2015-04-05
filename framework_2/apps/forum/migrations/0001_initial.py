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
            name='CategoryMeta',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categorymeta_ptr', models.OneToOneField(to='forum.CategoryMeta', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=('forum.categorymeta',),
        ),
        migrations.CreateModel(
            name='PostMeta',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
            ],
            options={
                'ordering': ['date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('postmeta_ptr', models.OneToOneField(to='forum.PostMeta', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=('forum.postmeta',),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('postmeta_ptr', models.OneToOneField(to='forum.PostMeta', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=('forum.postmeta',),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('categorymeta_ptr', models.OneToOneField(to='forum.CategoryMeta', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('parent_category', models.ForeignKey(to='forum.Category')),
            ],
            options={
            },
            bases=('forum.categorymeta',),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('category_related', models.ForeignKey(to='forum.CategoryMeta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postmeta',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='answer_related',
            field=models.ForeignKey(to='forum.Answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='thread_related',
            field=models.ForeignKey(to='forum.Thread'),
            preserve_default=True,
        ),
    ]
