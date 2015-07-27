# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150726_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
    ]
