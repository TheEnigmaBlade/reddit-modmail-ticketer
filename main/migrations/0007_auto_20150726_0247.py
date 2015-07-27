# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_message_parent_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageReply',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('sender', models.CharField(max_length=20)),
                ('sender_id', models.CharField(max_length=5)),
                ('parent_reply', models.ForeignKey(null=True, to='main.MessageReply', related_name='replies', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='parent_message',
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='messagereply',
            name='trunk_message',
            field=models.ForeignKey(to='main.Message', related_name='replies'),
        ),
    ]
