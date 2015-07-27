# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_ticket_is_flagged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_id',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='messagereply',
            name='sender',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='messagereply',
            name='sender_id',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
