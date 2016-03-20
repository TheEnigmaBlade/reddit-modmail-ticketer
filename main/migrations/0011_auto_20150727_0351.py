# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_subreddit_hl_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond_active_text',
            field=models.TextField(max_length=500, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond_closed_text',
            field=models.TextField(max_length=500, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond_new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subreddit',
            name='auto_respond_new_text',
            field=models.TextField(max_length=500, blank=True, default=''),
        ),
    ]
