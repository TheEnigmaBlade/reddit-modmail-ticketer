# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150723_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, to='main.Redditor'),
        ),
    ]
