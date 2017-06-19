$('#account-login').submit(function(event) {
  event.preventDefault();
  $.post('/accounts/login/',{
    'email': $("form#account-login input[name='email']").val(),
    'password': $("form#account-login input[name='password']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/";
    } else {
    $('#message-login').html(data.message)
      console.log(data)
    }
  })
})


$('#addproduct').submit(function(event) {
  event.preventDefault();  

  $.post('/admin/product/add/',{
    'pname': $("form#addproduct input[name='pname']").val(),
    'pdetail': $("form#addproduct input[name='pdetail']").val(),
    'pprice': $("form#addproduct input[name='pprice']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/product/list/";
    }else{
      $('#message-register').html(data.message)
    }
  })
})

$('#editproduct').submit(function(event) {
  event.preventDefault();  

  $.post('/admin/product/add/',{
    'pname': $("form#editproduct input[name='pname']").val(),
    'pdetail': $("form#editproduct input[name='pdetail']").val(),
    'pprice': $("form#editproduct input[name='pprice']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/product/list/";
    }else{
      $('#message-register').html(data.message)
    }
  })
})


$('#addsales').submit(function(event) {

  event.preventDefault();
  $.post('/admin/sales/add/',{
    'customer': $("#id_customer").find("option:selected").val(),
    'tds': $("form#addsales input[name='tds']").val(),
    'product': $("#id_product").find("option:selected").val(),
    'tamount': $("form#addsales input[name='tamount']").val(),
    'bamount': $("form#addsales input[name='bamount']").val(),
    'damount': $("form#addsales input[name='damount']").val(),
    'pamount': $("form#addsales input[name='pamount']").val(),
    'installdate': $("form#addsales input[name='installdate']").val(),
    'address': $("form#addsales input[name='address']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/sales/list/";
    }
  })
})

$('#addcustomer').submit(function(event) {

  event.preventDefault();
  $.post('/admin/customer/add/',{
    'name': $("form#addcustomer input[name='name']").val(),
    'email': $("form#addcustomer input[name='email']").val(),
    'city': $("form#addcustomer input[name='city']").val(),
    'phone': $("form#addcustomer input[name='phone']").val(),
    'address': $("form#addcustomer input[name='address']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/customer/list/";
    }
  })
})

$('#addservice').submit(function(event) {
   var cus_name = $("#id_user").val();
   var prod_name = $("#id_clg").val();
   if (cus_name && prod_name)
   {
    event.preventDefault();
    $.post('/admin/service/add/',{
      'name': cus_name,
      'product': prod_name,
      'sdetails': $("form#addservice input[name='sdetails']").val(),
      'attender': $("form#addservice input[name='attender']").val(),
      'samount': $("form#addservice input[name='samount']").val(),      
      'sdamount': $("form#addservice input[name='sdamount']").val(),
      'spamount': $("form#addservice input[name='spamount']").val(),
      'sbamount': $("form#addservice input[name='sbamount']").val(),
      'servicedate': $("form#addservice input[name='servicedate']").val(),
      'sstatus': $("#sstatus").val()
    })
    .done(function(data) {
      if ( data.status ) {
        window.location = "/admin/service/list/";
        }
    });
  }else{
    alert("Please choose customer and his project");
    return false;
  }  
});



$('#admin-login').submit(function(event) {
  event.preventDefault();
  $.post('/admin/login/',{
    'username': $("form#admin-login input[name='username']").val(),
    'password': $("form#admin-login input[name='password']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/dashboard";
    } else {
      $('#message-register').html(data.message)
      console.log('fail')
    }
  })
})


$('#account-register').submit(function(event) {
  event.preventDefault();
  $.post('/accounts/register/',{
    'email': $("form#account-register input[name='email']").val(),
    'password': $("form#account-register input[name='password']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/";
    } else {
      $('#message-register').html(data.message)
      console.log('fail')
    }
  })
})

$('#account-edit_profile').submit(function(event) {
  event.preventDefault();
  $.post('/accounts/settings/',{
    'email': $("form#account-edit_profile input[name='email']").val(),
    'first_name': $("form#account-edit_profile input[name='first_name']").val(),
    'last_name': $("form#account-edit_profile input[name='last_name']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/";
    } else {
      $('#message-edit_profile').html(data.message)
      console.log('fail')
    }
  })
})


$('#account-change_password').submit(function(event) {
  event.preventDefault();
  $.post('/accounts/change_password/',{
    'old_pwd': $("form#account-change_password input[name='old_pwd']").val(),
    'new_pwd1': $("form#account-change_password input[name='new_pwd1']").val(),
    'new_pwd2': $("form#account-change_password input[name='new_pwd2']").val()
  })
  .done(function(data) {  
    if ( data.status ) {
      window.location = "/";
    } else {
      $('#message-change_password').html(data.message)
      console.log('fail')
    }
  })
})

$('.free-ticket').on('click', function() {
  $('.table>tbody#update-here').append(
    "<tr>\
      <td></td>\
      <td><input type='text' class='form-control' name='ticket_name' placeholder='Name the ticket'></td>\
      <td><input type='number' class='form-control' name='ticket_count'  placeholder='100'></td>\
      <td><input type='text' class='form-control' value='free'  name='ticket_cost' placeholder='free' readonly='readonly'></td>\
      <td>\
      <button class='cut'><span class='glyphicon glyphicon-remove ' aria-hidden='true'></span></button></td>\
    </tr>");
})

$('.paid-ticket').on('click', function() {
  $('.table>tbody#update-here').append(
    "<tr>\
      <td></td>\
      <td><input type='text' class='form-control' name='ticket_name'  placeholder='Name the ticket'></td>\
      <td><input type='number' class='form-control' name='ticket_count'></td>\
      <td><input type='text' class='form-control' name='ticket_cost' placeholder='/-'></td>\
      <td><a href='#'><span class='glyphicon glyphicon-remove' id='cut' aria-hidden='true'></span></a></td>\
    </tr>");
})

// gly to remove the appended ticket
$('#cut').on('click', function(event) {
  alert('remove');
})

function subEvents(){
  $('.sub-events').toggle();
}

// sub event click and submit function
$('#sub-event-submit').on('click', function() {
  event.preventDefault();
  // click captured now get the sub event and update the subevent models

  var sub_title = $('#sub_title').val();
  var sub_description = $('#sub_description_this').val();
  
  $.post('/sub-event', {sub_title: sub_title, sub_description: sub_description})
    .done(function(data) {
      console.log(data);
      $('.sub-events').hide();
      $('.show-sub-event').append('<div class="col-md-3">\
                <ul class="list-group">\
                  <li>\
                    <div class="panel panel-default">\
                      <div class="panel-body">\
                        <h3>'+ data.sub_title +'</h3>\
                      </div>\
                    </div>\
                  </li>\
                </ul>\
              </div>')
    });
})

//bookmark
$('.bookmarkit').on('click', function(){
  var that = $(this);
  var isbookmarked = that.hasClass('bookmarhighlight');
  var eid = that.attr('data_id');
  if(isbookmarked){
    $.post('/', {'eid':eid, "bookmark":0}).done(function(data){
      that.removeClass('bookmarhighlight');
      return data;
    });
  } else {
    $.post('/', {'eid':eid,"bookmark":1}).done(function(data){
      that.addClass('bookmarhighlight');
      return data;
    });
  }
});


$('#addenquiry').submit(function(event) {

  event.preventDefault();
  $.post('/admin/enquiry/add/',{
    'customer': $("#id_customer").find("option:selected").val(),
    'otherdetails': $("form#addenquiry input[name='otherdetails']").val(),
    'estatus': $("#estatus").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/enquiry/list/";
    }
  })
})


$('#editservice').submit(function(event) {
   var cus_name = $("#id_user").val();
   var prod_name = $("#id_clg").val();
   if (cus_name && prod_name)
   {
    event.preventDefault();
    $.post('/admin/service/add/',{
      'name': cus_name,
      'product': prod_name,
      'sdetails': $("form#editservice input[name='sdetails']").val(),
      'attender': $("form#editservice input[name='attender']").val(),
      'samount': $("form#editservice input[name='samount']").val(),      
      'sdamount': $("form#editservice input[name='sdamount']").val(),
      'spamount': $("form#editservice input[name='spamount']").val(),
      'sbamount': $("form#editservice input[name='sbamount']").val(),
      'servicedate': $("form#editservice input[name='servicedate']").val(),
      'sstatus': $("#sstatus").val(),
      'serviceid': $("form#editservice input[name='serviceid']").val(),
      'payid': $("form#editservice input[name='payid']").val()      
    })
    .done(function(data) {
      if ( data.status ) {
        window.location = "/admin/service/list/";
        }
    });
  }else{
    alert("Please choose customer and his project");
    return false;
  }  
});



$('#editsales').submit(function(event) {

  event.preventDefault();
  $.post('/admin/sales/add/',{
    'customer': $("#id_customer").find("option:selected").val(),
    'tds': $("form#editsales input[name='tds']").val(),
    'product': $("#id_product").find("option:selected").val(),
    'tamount': $("form#editsales input[name='tamount']").val(),
    'bamount': $("form#editsales input[name='bamount']").val(),
    'damount': $("form#editsales input[name='damount']").val(),
    'pamount': $("form#editsales input[name='pamount']").val(),
    'installdate': $("form#editsales input[name='installdate']").val(),
    'address': $("form#editsales input[name='address']").val(),
    'sid': $("form#editsales input[name='sid']").val(),
    'payid': $("form#editsales input[name='payid']").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/sales/list/";
    }
  })
})

$('#editenquiry').submit(function(event) {

  event.preventDefault();
  $.post('/admin/enquiry/add/',{
    'eid': $("form#editenquiry input[name='eid']").val(),
    'customer': $("#id_customer").find("option:selected").val(),    
    'otherdetails': $("form#editenquiry input[name='otherdetails']").val(),
    'estatus': $("#estatus").val()
  })
  .done(function(data) {
    if ( data.status ) {
      window.location = "/admin/enquiry/list/";
    }
  })
})


$('#editcustomer').submit(function(event) {
  event.preventDefault();
  $.post('/admin/customer/add/',{
    'name': $("form#editcustomer input[name='name']").val(),
    'email': $("form#editcustomer input[name='email']").val(),
    'city': $("form#editcustomer input[name='city']").val(),
    'phone': $("form#editcustomer input[name='phone']").val(),
    'cid': $("form#editcustomer input[name='cid']").val(),
    'address': $("form#editcustomer input[name='address']").val()
  })
  .done(function(data) {
    if ( data.status ) {      
      window.location = "/admin/customer/list/";
    }
  })
});
