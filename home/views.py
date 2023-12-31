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
from django.db.models import Sum

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

#========================user signin to the system==================================================================
    
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
    user=request.user
    product = Product.objects.get(id=product_id)
    images = ProductImages.objects.filter(product=product)
    related_product=Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id','color__color_name','color__color_code','price','image').distinct()

    if request.method=="POST":
        colour=request.POST.get('colorselect')
        qty=request.POST.get('quantity')
        product_colour=Color.objects.get(color_name=colour)
        products=ProductAttribute.objects.get(product=product,color=product_colour)
        item, created = CartItem.objects.get_or_create(user=user, product=products,defaults={'is_deleted': False})
        item.total=products.price*float(qty)

        # If the object was created, set the initial quantity
        if created:
            item.quantity = qty
        
        # If the object already exists, update its quantity
        else:
            item.quantity += int(qty)
            item.save()
            item.total=products.price*item.quantity
       
        item.save()
        return redirect(cart_list)
    
    
    context={
        'product': product,
        'related_product ': related_product,
        'colors' :colors,
        'images':images,
    }
    

    return render(request, 'userhome/product_details.html', context)
#======================================== cart-list page =============================================================================================================

def cart_list(request):
    user=request.user 
    items=CartItem.objects.filter(user=user, is_deleted=False)
  
    total = items.aggregate(total_sum=Sum('total'))['total_sum'] or 0
 
    return render(request,'userhome/cart.html',{'items':items,'total':total})
     
#========================================= delete cart item ======================================================================================================================
def qty_update(request):
    user = request.user
    item_id = request.GET.get('item_id')
    new_quantity = int(request.GET.get('new_quantity'))
    print(item_id)
    print(new_quantity)
    cart_items = CartItem.objects.all().filter(is_deleted=False, user=user)
    


    cart_item = get_object_or_404(CartItem, id=item_id)
    now=timezone.now()

    # Update the quantity in the database
    cart_item.quantity = new_quantity
    cart_item.total = cart_item.product.price * new_quantity 
    cart_item.save()
    total_price = cart_items.aggregate(total=Sum('total'))['total']
    

    # You can optionally return some data in the response
    response_data = {'new_qty':new_quantity,'new_price':cart_item.total,'total':total_price}
    return JsonResponse(response_data)

def delete_cart_item(request):
    user = request.user
    item_id = request.GET.get('item_id')

    try:
        cart_item = CartItem.objects.get(id=item_id, user=user)
        cart_item.is_deleted = True
        cart_item.save()

        # Recalculate the total
        cart_items = CartItem.objects.filter(user=user, is_deleted=False)
        total = cart_items.aggregate(total_sum=Sum('total'))['total_sum'] or 0

        return JsonResponse({'success': True, 'total': total})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in the cart'})

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
@login_required(login_url='user_login')
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, users=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('user_account')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'userhome/edit_address.html', {'form': form, 'address': address})

@login_required(login_url='user_login')
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, users=request.user)
    
    if request.method == 'POST':
        address.delete()
        return redirect('user_account')
    
    return render(request, 'userhome/delete_address.html', {'address': address})
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

@login_required(login_url='user_login')
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
        logout(request)
        return redirect('user_login')
        # return redirect('user_account')  # Redirect to the user account page

    return render(request, 'userhome/change_password.html')




