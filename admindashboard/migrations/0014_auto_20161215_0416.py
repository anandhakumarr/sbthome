# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-15 04:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0013_enquiry_enquiry_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='address',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='city',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='email',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='name',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='phone',
        ),
        migrations.AddField(
            model_name='enquiry',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Customers'),
            preserve_default=False,
        ),
    ]