# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-19 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20160510_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlog',
            name='frame',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
