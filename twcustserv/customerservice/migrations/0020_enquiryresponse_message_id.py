# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0019_enquiry_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiryresponse',
            name='message_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
