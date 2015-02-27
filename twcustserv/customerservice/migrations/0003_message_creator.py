# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0002_thread_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='creator',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
