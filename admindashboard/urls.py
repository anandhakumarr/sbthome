from django.conf.urls import url
from admindashboard import views

urlpatterns = [
    url(r'^$', views.home, name='home'),    
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^sales/list/$', views.sales_list, name='sales_list'),
    url(r'^sales/add/$', views.addsales, name='addsales'),
    url(r'^enquiry/list/$', views.enquiry_list, name='enquiry_list'),
    url(r'^enquiry/add/$', views.addenquiry, name='addenquiry'),    
    url(r'^service/list/$', views.service_list, name='service_list'),
    url(r'^service/add/$', views.addservice, name='addservice'),
    url(r'^product/list/$', views.product_list, name='product_list'),
    url(r'^product/add/$', views.addproduct, name='addproduct'),
    url(r'^payment/add/$', views.addpayment, name='addpayment'),    
    url(r'^pending/service/$', views.pending_service, name='pending_service'),
    url(r'^pending/sales/$', views.pending_sales, name='pending_sales'),    
    url(r'^customerdetails/(?P<customerid>\w+)/$', views.customerdetails, name='customerdetails'),
    url(r'^product/edit/(?P<productid>\w+)/$', views.editproduct, name='editproduct'),
    url(r'^enquiry/edit/(?P<enquiryid>\w+)/$', views.editenquiry, name='editenquiry'),    
    url(r'^service/edit/(?P<serviceid>\w+)/$', views.editservice, name='editservice'),
    url(r'^sales/edit/(?P<salesid>\w+)/$', views.editsales, name='editsales'),
    url(r'^customer/list/$', views.customer_list, name='customer_list'),
    url(r'^customer/add/$', views.addcustomer, name='addcustomer'),
    url(r'^customer/edit/(?P<customerid>\w+)/$', views.editcustomer, name='editcustomer'),
]