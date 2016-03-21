# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customerservice', '0023_thread_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='user_id',
        ),
        migrations.AddField(
            model_name='enquiry',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='w_user',
            field=models.ForeignKey(related_name='tweet_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(related_name='thread_messages', to='customerservice.Thread'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thread',
            name='assigned_to',
            field=models.ForeignKey(related_name='assigned_to_thread', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
