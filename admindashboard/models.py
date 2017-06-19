from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Customers(models.Model):
	name = models.CharField(max_length=120, null=True, blank=True)
	email = models.CharField(max_length=120, null=True, blank=True)
	address = models.CharField(max_length=520, null=True, blank=True)
	city = models.CharField(max_length=120, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True)

class Enquiry(models.Model):
	customer = models.ForeignKey(Customers)
	otherdetails = models.TextField(null=True, blank=True)
	enquiry_date = models.DateTimeField(auto_now_add=True)
	STATUS = (
	(1,'Open'),
	(0,'Closed'),
	)	
	enquiry_status = models.IntegerField(null=True, blank= True,choices= STATUS)

class Product(models.Model):
	name = models.CharField(max_length=120, null=True, blank=True)
	details = models.CharField(max_length=220, null=True, blank=True)	
	price = models.FloatField(max_length = 225, null=True, blank=True)

class Sales(models.Model):
	product = models.ForeignKey(Product)
	customer = models.ForeignKey(Customers)
	tds = models.CharField(max_length=120, null=True, blank=True)
	installation_date = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
	customer = models.ForeignKey(Customers)
	product = models.ForeignKey(Product)
	sales = models.ForeignKey(Sales)
	attender = models.CharField(max_length=120, null=True, blank=True)
	service_details = models.TextField(null=True, blank=True)
	service_date = models.DateTimeField(auto_now_add=True)
	STATUS = (
	(1,'Open'),
	(0,'Closed'),
	)	
	service_status = models.IntegerField(null=True, blank= True,choices= STATUS)

class Payment_History(models.Model):
	customer = models.ForeignKey(Customers)
	service = models.ForeignKey(Service)
	sales = models.ForeignKey(Sales)
	TYPES = (
	(1,'Sales'),
	(2,'Service'),
	)
	payment_type = models.IntegerField(null=True, blank= True,choices= TYPES)	
	total_amount = models.FloatField(max_length = 225, null=True, blank=True)
	discount_amount = models.FloatField(max_length = 225, null=True, blank=True)
	paid_amount = models.FloatField(max_length = 225, null=True, blank=True)
	balance_amount = models.FloatField(max_length = 225, null=True, blank=True)
	tax_amount = models.FloatField(max_length = 225, null=True, blank=True)
	actual_amount = models.FloatField(max_length = 225, null=True, blank=True)
	payment_date = models.DateTimeField(auto_now_add=True)