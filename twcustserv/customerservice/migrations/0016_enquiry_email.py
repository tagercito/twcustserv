# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0015_auto_20160311_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='email',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
