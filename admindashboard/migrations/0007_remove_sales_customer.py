# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 07:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0006_sales_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='customer',
        ),
    ]
