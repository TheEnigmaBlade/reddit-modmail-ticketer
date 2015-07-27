# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150726_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='subreddit',
            name='hl_users',
            field=models.CharField(default='', max_length=209, blank=True),
        ),
    ]
