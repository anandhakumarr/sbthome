# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-13 17:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0011_auto_20161213_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='enquiry_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 12, 13, 17, 2, 58, 150638, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
