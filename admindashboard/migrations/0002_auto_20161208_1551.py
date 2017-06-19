# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-08 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_status',
            field=models.IntegerField(blank=True, choices=[(1, 'Open'), (0, 'Closed')], null=True),
        ),
        migrations.AlterField(
            model_name='payment_history',
            name='payment_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Sales'), (2, 'Service')], null=True),
        ),
    ]