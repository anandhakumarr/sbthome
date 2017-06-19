# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 07:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0005_remove_sales_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='customer',
            field=models.ForeignKey(default=datetime.datetime(2016, 12, 10, 7, 16, 1, 802062, tzinfo=utc), on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Customers'),
            preserve_default=False,
        ),
    ]