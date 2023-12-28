from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm
from django.contrib import messages
from payment.models import *
from payment.views import *
from .models import *
from django.db import transaction
from .models import User, Product, Brand, category
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import random
from .context_processors import *
from django.contrib.auth import logout,login
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
from django.http import Http404
from django.http import JsonResponse
from django.urls import reverse
from payment.models import *
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils.datastructures import MultiValueDictKeyError
from django.template.loader import render_to_string

# Create your views here.

#===============================user index========================================================================================================================

def user_index(request):
    products = Product.objects.filter(featured=True).order_by('-id')
    context = {
        'products': products,   
    }
    return render(request, 'userhome/index.html',context)

#==============================otp generate function-===================================================================================================================

def generate_otp():
    otp = str(random.randint(100000, 999999))
    timestamp = str(timezone.now())  #convert datetime to string
    return otp, timestamp

#=============================user signup============================================================================================================================

def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username is already existing . please choose a different username')
            return render(request, 'userhome/usersignup.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is alrady existing so Please choose another')
            return render(request, 'userhome/usersignup.html')
        elif cpassword != password:
            messages.error(request, 'mismatch password')
            return render(request, 'userhome/usersignup.html')
        #generate OTP
        otp, timestamp = generate_otp()
        
        request.session['signup_otp'] = otp  #save OTP to the session
        request.session['otp_timestamp'] = timestamp  #save the timestamp to the session

        send_mail(
            'OTP verification',
            f'your OTP for signup is : {otp}',
            'timetrixcronico@gmail.com',
            [email],
            fail_silently=True
        )
        request.session['signup_details']={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': make_password(password),
        }
        return redirect(enter_otp)
    return render(request,'userhome/usersignup.html')

#============================enter otp that we recive in the mail==============================================================================================

def enter_otp(request):
    if request.method == 'POST':
        entered_otp=request.POST.get('otp')
        stored_otp=request.session.get('signup_otp')
        timestamp_str = request.session.get('otp_timestamp')

         # Check if OTP is expired
        expiration_time = datetime.fromisoformat(timestamp_str) + timedelta(minutes=1)
        current_time = timezone.now()

        if current_time > expiration_time:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return render(request, 'userhome/otp.html')

        if entered_otp == stored_otp:
            new_user=User(
                username=request.session['signup_details']['username'],
                email=request.session['signup_details']['email'],
                first_name=request.session['signup_details']['first_name'],
                last_name=request.session['signup_details']['last_name'],
                phone=request.session['signup_details']['phone'],
                password=request.session['signup_details']['password']
            )
            new_user.save()
            login(request, new_user)

            request.session.pop('signup_otp',None)
            request.session.pop('otp_timestamp', None)
            request.session.pop('signup_details',None)
            return redirect('user_index')
        else:
            messages.error(request,'Invalid OTP. Please try again.')

    expiration_time = datetime.fromisoformat(request.session.get('otp_timestamp')) + timedelta(minutes=1)
    remaining_time = max(timedelta(0), expiration_time - timezone.now())
    remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
    return render(request, 'userhome/otp.html',{'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds})

#====================================if the otp expire resend the otp======================================================================
def resend_otp(request):
    if 'signup_details' in request.session:
        otp, timestamp = generate_otp()

        request.session['signup_otp'] = otp
        request.session['otp_timestamp'] = timestamp

        send_mail(
            'Resent OTP verification',
            f'Your new OTP for signup is: {otp}',
            'timetrixcronico@gmail.com',
            [request.session['signup_details']['email']],
            fail_silently=True
        )
        messages.info(request, 'New OTP sent. Please check your email.')
        return redirect('enter_otp')
    else:
        messages.error(request, 'No signup session found.')
        return redirect('signup')

#========================user signin to the system=========================================
    
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        print(user)
        if user is not None and user.check_password(password):
            if user.is_active:
                login(request,user)
                return redirect('user_index')
            else:
                messages.error(request, 'Your account is not active')
        else:
            messages.error(request, 'Invalid username and password')   
    return render(request, 'userhome/userlogin.html')

#============================user signout===========================================================================================================================================================

def user_logout(request):
    logout(request)
    return redirect('user_login')

#=============================display the all prouct in shop================================================================================================================================

def shop(request, category_id=None):
    all_categories = category.objects.all()
    selected_category = None
    products = None
    product_count = None

    if category_id:
        selected_category = get_object_or_404(category, id=category_id)
        products = Product.objects.filter(category=selected_category, is_available=True,is_deleted=False)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True,is_deleted=False)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'all_categories': all_categories,
        'selected_category': selected_category,
    }
    return render(request, 'userhome/shop.html', context)

#================================search==================================================================================================================================================

def search(request):
    q=request.GET['q']
    data = Product.objects.filter(product_name__icontains=q).order_by('-id')
    return render(request,'userhome/search.html',{'data':data})

#===============================click the product it view the product details=============================================================================================

def product_details(request, product_id,  category_id):
    print("product_id:", product_id)
    print("category_id:", category_id)
    product = Product.objects.get(id=product_id)
    images = ProductImages.objects.filter(product=product)
    related_product=Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id','color__color_name','color__color_code','price','image').distinct()
    context={
        'product': product,
        'related_product ': related_product,
        'colors' :colors,
        'images':images,
    }

    return render(request, 'userhome/product_details.html', context)


#=======================================add-to-car=======================================================================================

def add_to_cart(request):
    cart_p={}
    cart_p[str(request.GET['id'])]={
        'image':request.GET['image'],
        'name':request.GET['name'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }
    # print(cart_p)
    #data exist
    # if cart_pqty <= 0:
    #     return JsonResponse({'error': 'Please enter a valid quantity.'}, status=400)
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    #not exist
    else:
        request.session['cartdata']=cart_p
    # print(cart_p)
    # print(request.session['cartdata'])
    messages.success(request, 'Item added to the cart successfully.')
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

#======================================== cart-list page =============================================================================================================

def cart_list(request):
    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])

        return render(request, 'userhome/cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})  
    else:
        return render(request, 'userhome/cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt}) 
     
#========================================= delete cart item ======================================================================================================================
def delete_cart_item(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]  #delete the cart data
            request.session['cartdata']=cart_data #after remove the data is store in the session
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    #reloading the page
    t=render_to_string('userhome/cart_list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

#===================================update cart===============================================================================================================================
def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty #update the cart qty
            request.session['cartdata']=cart_data #after remove the data is store in the session
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    #reloading the page
    t=render_to_string('userhome/cart_list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})
#=======================================user account====================================================================================================================================
@login_required(login_url='user_login')
def user_account(request):
    user_address = Address.objects.filter(users=request.user)
    order_history = CartOrder.objects.filter(user=request.user).order_by('-id')

    context={
        'user_address':user_address,
        'user_data' :request.user,
        'order_history': order_history
    }
    return render(request, 'userhome/user_account.html',context)
#====================================cancel order========================================================================================================================================

@login_required(login_url='user_login')
def cancel_order(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = get_object_or_404(CartOrder, id=order_id, user=request.user)

        # Revert stock for each item in the order
        for order_item in order.cartorderitems_set.all():
            try:
                product_attr = ProductAttribute.objects.get(id=order_item.product.id)
                product_attr.stock += order_item.qty
                product_attr.save()
            except ProductAttribute.DoesNotExist:
                # Handle the case where the product attribute does not exist
                # For example, redirect to an error page or display a message
                messages.warning(request, f'Product not found for ID: {order_item.product.id}')

        # Delete the order
        order.delete()

        messages.success(request, 'Order canceled successfully!')
        return redirect('user_account')

    messages.error(request, 'Invalid request to cancel order.')
    return redirect('user_account')
#=========================================password change====================================
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        print(f'Entered password: {current_password}')
        print(f'Stored password: {request.user.password}')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'Incorrect current password. Please try again.')
            return redirect('change_password')

        # Check if new password and confirmation match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match. Please try again.')
            return redirect('change_password')

        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()

        # Update session to avoid logout
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('user_account')  # Redirect to the user account page

    return render(request, 'userhome/change_password.html')