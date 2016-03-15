# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0018_enquiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
