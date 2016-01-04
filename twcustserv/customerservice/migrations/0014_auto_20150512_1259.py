# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0013_pull'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pull',
            name='message_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
