# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerservice', '0014_auto_20150512_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enquiry', models.TextField()),
                ('file', models.FileField(null=True, upload_to=b'enquiry', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('field_type', models.CharField(max_length=50, choices=[(b'email', b'email'), (b'text', b'text'), (b'file', b'file')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='topicfield',
            name='form',
            field=models.ForeignKey(related_name='form_fields', to='customerservice.TopicForm'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='form',
            field=models.ForeignKey(blank=True, to='customerservice.TopicForm', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='topic',
            field=models.ForeignKey(related_name='topic_child', blank=True, to='customerservice.Topic', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enquiry',
            name='topic',
            field=models.ForeignKey(to='customerservice.Topic'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='bulletin',
            options={'verbose_name': 'Noticias', 'verbose_name_plural': 'Noticias'},
        ),
        migrations.AlterModelOptions(
            name='thread',
            options={'verbose_name': 'Tweets', 'verbose_name_plural': 'Tweets'},
        ),
    ]
