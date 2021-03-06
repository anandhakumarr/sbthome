# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-08 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('address', models.CharField(blank=True, max_length=520, null=True)),
                ('city', models.CharField(blank=True, max_length=120, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.IntegerField(blank=True, choices=[(1, 'Sales'), (0, 'Service')], null=True)),
                ('paid_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Customers')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('details', models.CharField(blank=True, max_length=220, null=True)),
                ('price', models.FloatField(blank=True, max_length=225, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tds', models.CharField(blank=True, max_length=120, null=True)),
                ('installation_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('discount_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('paid_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('balance_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('tax_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('actual_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attender', models.CharField(blank=True, max_length=120, null=True)),
                ('service_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('discount_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('paid_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('balance_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('tax_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('actual_amount', models.FloatField(blank=True, max_length=225, null=True)),
                ('service_details', models.CharField(blank=True, max_length=220, null=True)),
                ('service_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Customers')),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Sales')),
            ],
        ),
        migrations.AddField(
            model_name='payment_history',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admindashboard.Sales'),
        ),
    ]
