# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_subreddit_bots'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='bots',
            field=models.CharField(blank=True, default='AutoModerator', max_length=209),
        ),
    ]
