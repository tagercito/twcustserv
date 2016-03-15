# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0017_enquiryresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 11, 14, 29, 6, 900870), auto_now=True),
            preserve_default=False,
        ),
    ]
