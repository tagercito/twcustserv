# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0022_enquiry_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='email',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
    ]
