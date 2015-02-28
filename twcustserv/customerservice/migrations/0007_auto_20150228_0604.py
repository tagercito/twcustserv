# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0006_auto_20150227_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='status',
            field=models.CharField(default=b'OP', max_length=2, choices=[(b'OP', b'Open'), (b'PE', b'Pending'), (b'CL', b'Closed')]),
            preserve_default=True,
        ),
    ]
