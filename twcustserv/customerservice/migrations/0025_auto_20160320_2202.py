# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0024_auto_20160320_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='status',
            field=models.CharField(default=b'OP', max_length=2, choices=[(b'OP', b'Open'), (b'PE', b'Pending'), (b'CL', b'Closed')]),
            preserve_default=True,
        ),
    ]
