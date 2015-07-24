# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_subreddit_bots'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='date_edited',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
