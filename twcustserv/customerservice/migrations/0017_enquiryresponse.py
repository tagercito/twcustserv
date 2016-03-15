# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customerservice', '0016_enquiry_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnquiryResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('sender', models.CharField(max_length=140, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('thread', models.ForeignKey(to='customerservice.Enquiry')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
