# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0004_auto_20150227_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='user_id',
            field=models.CharField(default=2, max_length=140),
            preserve_default=False,
        ),
    ]
