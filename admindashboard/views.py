from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,  login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from django.core.validators import validate_email
from admindashboard.models import Customers
from admindashboard.models import Product
from admindashboard.models import Sales
from admindashboard.models import Payment_History
from admindashboard.models import Service
from admindashboard.models import Enquiry
import json
from datetime import datetime

@csrf_exempt
def home(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:            
            return redirect('admindashboard:dashboard')            
    return render(request, 'adminlogin.html')

@csrf_exempt
def login_view(request):
    """
    This login functon is used for login to the system. The funny thing is
    json response so whenver the POST request comes in the syste checks and
    response with message and status.. why for home page also have popup
    login and sign up system
    """

    if request.method == "POST":
        usr = request.POST['username']
        pwd = request.POST['password']        

        user = authenticate(username=usr, password=pwd)                    
        if user is not None:
            if user.is_active:
                if user.is_superuser:                    
                    auth_login(request, user)                    
                    return JsonResponse(
                        {'status': True, 'message': "You are logged in"})            
                else:
                    return JsonResponse(
                        {'status': False, 'message': "You don't have a admin access"})            
                # auth_login(request, user)
            else:
                return JsonResponse(
                    {'status': False, 'message': 'User is not active'})        
        else:            
            return JsonResponse(
                {'status': False, 'message': 'Username or Password is Incorrect'})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def dashboard(request):   
    
    total_customer = Customers.objects.count()
    total_service= Service.objects.filter(service_status=0).count()
    total_open_service= Service.objects.filter(service_status=1).count()
    product_count = Product.objects.count()
    sales = 10
    orders = 0
    return render(request, 'admindashboard.html', {'total_customer': total_customer, 'total_service' : total_service,
        'total_open_service':total_open_service, 'product_count':product_count,'sales': sales, 'orders': orders})    

def logout_view(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('admindashboard:home'))

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def service_list(request):
    service_list = Service.objects.all()
    base_dict = []
    for row in service_list:
        temp = {}
        temp['id'] = row.id
        temp['customer_name'] = row.customer.name
        temp['customer_id'] =  row.customer.id
        temp['product_name'] = row.product.name
        temp['attender'] = row.attender
        temp['service_details'] = row.service_details
        temp['service_date'] = row.service_date
        temp['service_status'] = row.service_status
        base_dict.append(temp)

    return render(request, 'servicelist.html', {'base_dict': base_dict})        

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def addservice(request):

    customer_list = Customers.objects.all()

    sales = Sales.objects.all()

    sales_list = {}

    for sal in sales:
        if 'option_'+str(sal.customer_id) not in sales_list: 
            sales_list['option_'+str(sal.customer_id)] = '<option value="'+str(sal.id)+','+str(sal.product_id)+'">'+str(Product.objects.get(id=sal.product_id).name)+'</option>'
        else:
            sales_list['option_'+str(sal.customer_id)] += '<option value="'+str(sal.id)+','+str(sal.product_id)+'">'+str(Product.objects.get(id=sal.product_id).name)+'</option>'

    customer_sales = json.dumps(sales_list)    

    if request.method == "POST":        
        
        samount = request.POST['samount']
        customer = request.POST['name']        
        sales, product = request.POST['product'].split(',')
        spamount = request.POST['spamount']        
        sdetails = request.POST['sdetails']  
        attender = request.POST['attender']  
        servicedate = request.POST['servicedate']  
        sbamount = request.POST['sbamount']          
        sdamount = request.POST['sdamount']  
        sstatus = request.POST['sstatus']  
        
        pid = Product.objects.get(id=product)
        cid = Customers.objects.get(id=customer)
        sid = Sales.objects.get(id=sales)

        try:
            serviceid = request.POST['serviceid']
            service = Service.objects.get(id=serviceid)
        except:
            service = Service()

        service.customer = cid
        service.sales = sid
        service.product = pid        
        service.attender = attender
        service.service_details = sdetails
        service.service_date = servicedate
        service.service_status = sstatus
        service.save()


        try:
            payid = request.POST['payid']
            obj = Payment_History.objects.get(id=payid)
        except:
            obj = Payment_History()

        obj.payment_type = 2   
        obj.total_amount = samount
        obj.discount_amount = sdamount
        obj.paid_amount = spamount
        obj.balance_amount = sbamount        
        obj.customer = cid        
        obj.sales = sid
        obj.service = service
        obj.save()

        return JsonResponse(
                {'status': True, 'message': 'Service created'})

    return render(
        request, 'addservice.html', {'customer_list' : customer_list, 'customer_sales': customer_sales}) 


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def pending_sales(request):

    pending_sales = Payment_History.objects.filter(payment_type=1).filter(balance_amount__gt=0)
    base_dict = []

    for row in pending_sales:        
        temp = {}
        temp['id'] = row.id
        temp['customername'] = row.customer.name        
        temp['customer_id'] =  row.customer.id
        temp['productname'] = row.sales.product.name
        temp['Installationdate'] = row.sales.installation_date
        temp['productprice'] = row.sales.product.price
        temp['total_amount'] = row.total_amount
        temp['discount_amount'] = row.discount_amount
        temp['paid_amount'] = row.paid_amount
        temp['balance_amount'] = row.balance_amount        
        temp['payment_date'] = row.payment_date        

        base_dict.append(temp)
    return render(
        request, 'pendingsales.html', {'pending_sales':base_dict})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def pending_service(request):

    pending_service = Payment_History.objects.filter(payment_type=2).filter(balance_amount__gt=0).filter(sales_id__gt=0)
    base_dict = []

    for row in pending_service:                
        temp = {}
        temp['id'] = row.id
        temp['customername'] = row.customer.name        
        temp['customer_id'] =  row.customer.id
        temp['productname'] = row.sales.product.name
        temp['Installationdate'] = row.sales.installation_date
        temp['productprice'] = row.sales.product.price
        temp['total_amount'] = row.total_amount
        temp['discount_amount'] = row.discount_amount
        temp['paid_amount'] = row.paid_amount
        temp['balance_amount'] = row.balance_amount        
        temp['payment_date'] = row.payment_date        
        base_dict.append(temp)
    
    return render(
        request, 'pendingservice.html', {'pending_service':base_dict})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def product_list(request):
    product_list = Product.objects.all()
    return render(
        request, 'productlist.html', {'product_list' : product_list})        


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def editproduct(request, productid):

    product_list = Product.objects.filter(id=productid)

    pname = ''
    pdetail = ''
    price = ''
    for row in product_list:
        pname   = row.name
        pdetail = row.details
        price = row.price    

    return render(
        request, 'editproduct.html', {'pname' : pname, 'pdetail': pdetail, 'price': price})      


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def addproduct(request):
    if request.method == "POST":    
        
        pname = request.POST['pname']
        pdetail = request.POST['pdetail']
        pprice = request.POST['pprice']        

        product, created = Product.objects.get_or_create(name=pname)
        if created:
            product.details = pdetail
            product.price = pprice
            product.save()
            return JsonResponse(
                {'status': True, 'message': 'Product created'})
        else:
            product.details = pdetail
            product.price = pprice
            product.save()
            return JsonResponse(
                {'status': True, 'message': 'Product Edited'})            


    return render(
        request, 'addproduct.html')      



@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def addcustomer(request):
    if request.method == "POST":    
        
        name = request.POST['name']
        email = request.POST['email']        
        address = request.POST['address']        
        phone = request.POST['phone']        
        city = request.POST['city']        

        try:
            cid = request.POST['cid']
            customer = Customers.objects.get(id=cid)
        except:
            customer = Customers()    
                
        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.city = city
        customer.address = address
        customer.save()

        return JsonResponse(
                {'status': True, 'message': 'Customer Edited'})            


    return render(
        request, 'addcustomer.html')      

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def editcustomer(request, customerid):

    customer_list = Customers.objects.filter(id=customerid)

    email = ''
    name = ''
    address = ''
    phone = ''
    cid  = ''
    city = ''

    for row in customer_list:
        name   = row.name
        cid = row.id
        email = row.email
        address = row.address
        phone = row.phone
        city = row.city

    return render(
        request, 'editcustomer.html', {'city' : city, 'phone': phone, 'address': address,'email': email, 'name': name,
        'cid': cid})      


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def customer_list(request):

    customer_list = Customers.objects.all()

    base_dict = []
    for row in customer_list:
        temp = {}
        temp['id'] = row.id
        temp['customer_name'] =  row.name
        temp['customer_email'] =  row.email
        temp['customer_phone'] =  row.phone
        temp['customer_city'] =  row.city
        temp['customer_address'] =  row.address
        base_dict.append(temp)

    return render(
        request, 'customerlist.html', {'base_dict' : base_dict})        


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def sales_list(request):

    sales_list = Sales.objects.all()

    base_dict = []
    for row in sales_list:
        temp = {}
        temp['id'] = row.id
        temp['tds'] = row.tds
        temp['installation_date'] = row.installation_date
        temp['customer_name'] =  row.customer.name
        temp['customer_id'] =  row.customer.id
        temp['customer_phone'] =  row.customer.phone
        temp['customer_city'] =  row.customer.city
        temp['product_name'] =  row.product.name
        base_dict.append(temp)

    return render(
        request, 'saleslist.html', {'base_dict' : base_dict})        


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def editservice(request, serviceid):

    service_list = Service.objects.filter(id=serviceid)
    customer_list = Customers.objects.all()
    product_list = Product.objects.all()
    payhistory = Payment_History.objects.filter(service_id=serviceid)
    sales = Sales.objects.all()    

    customer_id = ''
    serviceid = ''
    servicedetails = ''
    product_id = 0
    attender = ''
    service_date = ''
    service_status = 0

    for row in service_list:        
        serviceid = row.id
        servicedetails = row.service_details
        attender = row.attender
        customer_id =  row.customer_id
        product_id =  row.product_id
        service_date =  row.service_date
        service_status = row.service_status

    total_amount = discount_amount = payid = paid_amount = balance_amount = 0

    for row in payhistory:
        total_amount = row.total_amount
        discount_amount = row.discount_amount
        paid_amount = row.paid_amount
        balance_amount = row.balance_amount
        payid = row.id

    try:
        service_date = service_date.strftime('%Y-%m-%d')
    except:
        pass

    sales_list = {}

    for sal in sales:
        if 'option_'+str(sal.customer_id) not in sales_list: 
            if str(sal.product_id)==product_id: 
                sales_list['option_'+str(sal.customer_id)] = '<option selected="selected" value="'+str(sal.id)+','+str(sal.product_id)+'">'+str(Product.objects.get(id=sal.product_id).name)+'</option>'
            else:
                sales_list['option_'+str(sal.customer_id)] = '<option value="'+str(sal.id)+','+str(sal.product_id)+'">'+str(Product.objects.get(id=sal.product_id).name)+'</option>'
        else:
            if str(sal.product_id)==product_id: 
                sales_list['option_'+str(sal.customer_id)] += '<option selected="selected" value="'+str(sal.id)+','+str(sal.product_id)+'">'+str(Product.objects.get(id=sal.product_id).name)+'</option>'
            else:
                sales_list['option_'+str(sal.customer_id)] += '<option value="'+str(sal.id)+','+str(sal.product_id)+'">'+str(Product.objects.get(id=sal.product_id).name)+'</option>'

    customer_sales = json.dumps(sales_list)    

    return render(
        request, 'editservice.html', {'product_list':product_list,'customer_list':customer_list,'product_id' : product_id,
         'attender': attender, 'customer_id': customer_id, 'servicedetails': servicedetails, 'serviceid': serviceid,
         'total_amount':total_amount,'payid':payid,'balance_amount':balance_amount,'service_date': service_date,
         'paid_amount':paid_amount, 'discount_amount': discount_amount, 'customer_sales':customer_sales,'service_status':service_status  })        


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def editsales(request, salesid):

    sales_list = Sales.objects.filter(id=salesid)
    customer_list = Customers.objects.all()
    product_list = Product.objects.all()
    payhistory = Payment_History.objects.filter(sales_id=salesid).filter(payment_type=1)

    customer_id = ''
    sid = ''
    tds = ''
    installation_date = ''
    customer_name = ''
    customer_phone = ''
    customer_city = ''
    product_name = ''

    for row in sales_list:        
        sid = row.id
        tds = row.tds
        installation_date = row.installation_date
        customer_id =  row.customer_id
        customer_phone =  row.customer.phone
        customer_city =  row.customer.city
        product_id =  row.product_id
    try:
        installation_date = installation_date.strftime('%Y-%m-%d')
    except:
        pass

    total_amount = discount_amount = payid = paid_amount = balance_amount = 0

    for row in payhistory:
        total_amount = row.total_amount
        discount_amount = row.discount_amount
        paid_amount = row.paid_amount
        balance_amount = row.balance_amount
        payid = row.id

    return render(
        request, 'editsales.html', {'product_list':product_list,'customer_list':customer_list,'product_id' : product_id,'customer_city': customer_city,
        'customer_phone': customer_phone, 'customer_id': customer_id, 'installation_date':installation_date,
         'tds': tds, 'sid': sid,'total_amount':total_amount,'payid':payid,'balance_amount':balance_amount,
         'paid_amount':paid_amount, 'discount_amount': discount_amount  })        

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def addsales(request):

    product_list = Product.objects.all()
    customer_list = Customers.objects.all()

    if request.method == "POST":   

        customer = request.POST['customer']
        product = request.POST['product']        
        tds = request.POST['tds']        
        tamount = request.POST['tamount']        
        bamount = request.POST['bamount']        
        damount = request.POST['damount']        
        pamount = request.POST['pamount']        
        installdate = request.POST['installdate']        

        cus = Customers.objects.get(id=customer)
        pid = Product.objects.get(id=product)

        try:
            sid = request.POST['sid']
            sal = Sales.objects.get(id=sid)
        except:
            sal = Sales()
        
        sal.customer = cus
        sal.tds = tds
        sal.installation_date = installdate
        sal.product = pid
        sal.save()

        try:
            payid = request.POST['payid']
            obj = Payment_History.objects.get(id=payid)
        except:
            obj = Payment_History()

        obj.product = pid
        obj.payment_type = 1    
        obj.total_amount = tamount
        obj.discount_amount = damount
        obj.paid_amount = pamount
        obj.balance_amount = bamount        
        obj.customer = cus        
        obj.sales = sal
        obj.service_id = 0
        obj.save()

        return JsonResponse(
                        {'status': True, 'message': "New Customer added"})            
    return render(request, 'addsales.html', {'product_list' : product_list,'customer_list':customer_list})

@csrf_exempt
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def addpayment(request):
    if request.method == "POST":   
  
        tamount = request.POST['tamount']        
        bamount = request.POST['bamount']        
        damount = request.POST['damount']        
        pamount = request.POST['pamount']        
        sales_id = request.POST['sales_id']     
        service_id = int(request.POST['service_id'])
        payment_type = request.POST['payment_type']     
        customer_id = request.POST['customer_id']     
        product_id = request.POST['product_id']     

        cus = Customers.objects.get(id=customer_id)
        pid = Product.objects.get(id=product_id)
        sal = Sales.objects.get(id=sales_id)

        obj = Payment_History()
        obj.product = pid
        obj.payment_type =  payment_type 
        obj.total_amount = tamount
        obj.discount_amount = damount
        obj.paid_amount = pamount
        obj.balance_amount = bamount        
        obj.customer = cus        
        obj.sales = sal

        try:
            service = Service.objects.get(id=service_id)
            obj.service = service
        except:
            service = service_id
            obj.service_id = service

        obj.save()
        
        return JsonResponse(
                {'status': True})   

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def customerdetails(request,customerid):

    sales = Sales.objects.filter(customer_id=customerid)

    payhistory = Payment_History.objects.filter(customer_id=customerid)
    servicedetails = Service.objects.filter(customer_id=customerid)
    customer_list = Customers.objects.filter(id=customerid)

    base_dict = []
    for row in customer_list:
        temp = {}
        temp['id'] = row.id
        temp['customer_name'] =  row.name
        temp['customer_email'] =  row.email
        temp['customer_phone'] =  row.phone
        temp['customer_city'] =  row.city
        temp['customer_address'] =  row.address
        base_dict.append(temp)    

    fulldata = []

    for row in sales:
        temp = {}
        temp['sales_id'] = row.id
        temp['productid'] = row.product_id
        temp['productname'] = row.product.name
        temp['productprice'] = row.product.price
        temp['customerid'] = row.customer_id
        temp['tds'] = row.tds
        temp['installation_date'] = row.installation_date
        
        total_amount = 0
        discount_amount = 0
        paid_amount = 0
        sales_balance_amount = 0

        payhistory_product = []
        for krow in payhistory:
            temp_pay = {}
            if krow.sales_id == row.id and krow.payment_type == 1:
                temp_pay['total_amount'] = krow.total_amount
                total_amount = float(krow.total_amount)
                discount_amount = float(krow.discount_amount)
                paid_amount += float(krow.paid_amount)

                temp_pay['discount_amount'] = krow.discount_amount
                temp_pay['paid_amount'] = krow.paid_amount
                temp_pay['balance_amount'] = krow.balance_amount
                temp_pay['payment_date'] = krow.payment_date
                payhistory_product.append(temp_pay)
        temp['payhistory_product'] = payhistory_product

        sales_balance_amount = float(total_amount) - float(discount_amount) - float(paid_amount)
        sales_id = row.id
        customer_id = row.customer_id
        product_id = row.product_id
        service_id = 0
        payment_type = 1        

        temp['sales_balance_amount'] = sales_balance_amount
        temp['sales_id'] = sales_id
        temp['customer_id'] = customer_id
        temp['service_id'] = service_id
        temp['payment_type'] = payment_type
        temp['total_amount'] = total_amount
        temp['discount_amount'] = discount_amount
        temp['paid_amount'] = paid_amount
        temp['product_id'] = product_id
        

        servicehistory = []
        for srow in servicedetails:
            if srow.sales_id == row.id:
                temp_service = {}
                temp_service['attender'] = srow.attender
                temp_service['service_details'] = srow.service_details
                temp_service['service_date'] = srow.service_date
                temp_service['service_status'] = srow.service_status
                temp_service['serviceid'] = srow.id

                service_balance_amount = 0
                service_total_amount = 0
                service_discount_amount = 0
                service_paid_amount = 0

                servicepayments = []

                for krow1 in payhistory:
                    temp_pay1 = {}
                    if krow1.service_id == srow.id and krow1.payment_type == 2:

                        service_total_amount = float(krow1.total_amount)
                        service_discount_amount = float(krow1.discount_amount)
                        service_paid_amount += float(krow1.paid_amount)

                        temp_pay1['total_amount'] = krow1.total_amount
                        temp_pay1['discount_amount'] = krow1.discount_amount
                        temp_pay1['paid_amount'] = krow1.paid_amount
                        temp_pay1['balance_amount'] = krow1.balance_amount
                        temp_pay1['payment_date'] = krow1.payment_date
                        servicepayments.append(temp_pay1)

                service_balance_amount = float(service_total_amount) - float(service_discount_amount) - float(service_paid_amount)
                service_sales_id = row.id
                service_customer_id = row.customer_id
                service_product_id = row.product_id
                service_service_id = srow.id
                service_payment_type = 2    

                temp_service['service_balance_amount'] = service_balance_amount
                temp_service['service_sales_id'] = service_sales_id
                temp_service['service_customer_id'] = service_customer_id
                temp_service['service_service_id'] = service_service_id
                temp_service['service_payment_type'] = service_payment_type
                temp_service['service_total_amount'] = service_total_amount
                temp_service['service_discount_amount'] = service_discount_amount
                temp_service['service_paid_amount'] = service_paid_amount
                temp_service['service_product_id'] = service_product_id

                temp_service['servicepayments'] = servicepayments
                servicehistory.append(temp_service)

        temp['servicehistory'] = servicehistory
        fulldata.append(temp)

    return render(
        request, 'customerdetails.html',{'base_dict' : base_dict,'sales_detail':sales,'payhistory':payhistory,
                                        'servicedetails':servicedetails,'fulldata':fulldata})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def enquiry_list(request):

    enquiry_list = Enquiry.objects.all()

    base_dict = []
    for row in enquiry_list:
        temp = {}
        temp['id'] = row.id
        temp['customer_otherdetails'] = row.otherdetails
        temp['enquiry_date'] = row.enquiry_date
        temp['customer_name'] =  row.customer.name
        temp['customer_phone'] =  row.customer.phone
        temp['customer_email'] =  row.customer.email
        temp['customer_address'] =  row.customer.address
        temp['customer_city'] =  row.customer.city        
        temp['enquiry_status'] = row.enquiry_status
        base_dict.append(temp)

    return render(
        request, 'enquiry_list.html', {'base_dict' : base_dict})        

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
def editenquiry(request, enquiryid):

    enquiry_list = Enquiry.objects.filter(id=enquiryid)
    customer_list = Customers.objects.all()

    customer_otherdetails = ''
    enquiry_date = ''
    enquiry_status = ''
    customer_id = ''
    eid = None
    for row in enquiry_list:            
        eid  = row.id
        customer_otherdetails = row.otherdetails
        enquiry_date = row.enquiry_date
        customer_id =  row.customer.id
        enquiry_status = row.enquiry_status

    return render(
        request, 'editenquiry.html', {'customer_otherdetails' : customer_otherdetails,
        'enquiry_date': enquiry_date,'enquiry_status': enquiry_status,
        'customer_list': customer_list,'customer_id': customer_id, 'eid': eid })        


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')    
@csrf_exempt
def addenquiry(request):
    if request.method == "POST":    

        customer = request.POST['customer']        
        otherdetails = request.POST['otherdetails']        
        enquiry_status = request.POST['estatus']  

        cid = Customers.objects.get(id=customer)      
        try:
            eid = request.POST['eid']
            enq = Enquiry.objects.get(id=eid)
        except:
            enq = Enquiry()    
        
        enq.customer = cid
        enq.otherdetails = otherdetails
        enq.enquiry_status = enquiry_status
        enq.save()

        return JsonResponse(
                {'status': True, 'message': 'Enquiry created'})

    customer_list = Customers.objects.all()

    return render(
        request, 'addenquiry.html', {'customer_list':customer_list})          