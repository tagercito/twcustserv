# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0007_auto_20150228_0604'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 19, 23, 20, 408798), auto_now=True),
            preserve_default=False,
        ),
    ]
