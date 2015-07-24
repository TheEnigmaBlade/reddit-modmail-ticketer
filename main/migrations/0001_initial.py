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
            name='Message',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=6)),
                ('subject', models.CharField(max_length=300)),
                ('sender', models.CharField(max_length=20)),
                ('sender_id', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Redditor',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=20)),
                ('user', models.OneToOneField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=20)),
                ('enabled', models.BooleanField(default=True)),
                ('bots', models.CharField(max_length=209, default='AutoModerator', blank=True)),
                ('moderators', models.ManyToManyField(related_name='moderates_set', to='main.Redditor')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(default=0)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('message', models.OneToOneField(to='main.Message')),
                ('subreddit', models.ForeignKey(to='main.Subreddit')),
            ],
        ),
    ]
