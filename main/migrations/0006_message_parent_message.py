# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_ticket_modified_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parent_message',
            field=models.ForeignKey(null=True, blank=True, related_name='replies', to='main.Message'),
        ),
    ]
