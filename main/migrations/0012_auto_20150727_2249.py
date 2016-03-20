# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150727_0351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subreddit',
            name='auto_respond_active',
        ),
        migrations.RemoveField(
            model_name='subreddit',
            name='auto_respond_active_text',
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='auto_respond_closed_text',
            field=models.TextField(max_length=800, default='', blank=True),
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='auto_respond_new_text',
            field=models.TextField(max_length=800, default='', blank=True),
        ),
    ]
