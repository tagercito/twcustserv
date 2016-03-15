# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0020_enquiryresponse_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiryresponse',
            name='message_id',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
