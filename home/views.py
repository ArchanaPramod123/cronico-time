from django.shortcuts import render,redirect,get_object_or_404
# from .forms import SignUpForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import random
from payment.forms import AddressForm
from .context_processors import *
from django.contrib.auth import logout,login
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils.datastructures import MultiValueDictKeyError
from django.template.loader import render_to_string
from django.db.models import Sum
from adminhome.models import ProductOffer

from payment.models import Address,CartOrder,CartItem,ProductOrder,Payments,Wallet,WalletHistory
from .models import Product,category,User,ProductImages,ProductAttribute,Color,Wishlist,WishlistItems
# Create your views here.

#===============================user index==============================================================================================================================================================

def user_index(request):
    products = Product.objects.filter(featured=True).order_by('-id').distinct()
    product_offers=ProductOffer.objects.filter(is_active=True)
    for p in products:
       try:
           product_offer=ProductOffer.objects.get(product=p)
           if product_offer.is_active:
              pass
           else:
               p.product_offer = 0
               p.save()
           
       except:
           p.product_offer = 0
           p.save()
    
    context = {
        'products': products,   
    }
    if product_offers is not None:
        context['product_offers']=product_offers
    return render(request, 'userhome/index.html',context)

#==============================otp generate function-=====================================================================================================================================================================

def generate_otp():
    otp = str(random.randint(100000, 999999))
    timestamp = str(timezone.now())  #convert datetime to string
    return otp, timestamp

#=============================user signup======================================================================================================================================================================

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

#============================enter otp that we recive in the mail================================================================================================================================

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

#====================================if the otp expire resend the otp===============================================================================================================
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

#========================user signin to the system====================================================================================================================================================
    
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

#============================user signout==================================================================================================================================================================================================

def user_logout(request):
    logout(request)
    return redirect('user_login')

#=============================display the all prouct in shop================================================================================================================================

def shop(request, category_id=None):
    all_categories = category.objects.all()
    selected_category = None
    products = None
    product_count = None
    brands = Brand.objects.filter(is_active=True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')


    if category_id:
        selected_category = get_object_or_404(category, id=category_id)
        products = Product.objects.filter(
            category=selected_category,
            is_available=True,
            is_deleted=False,
            brand__is_active=True
        )
        product_count = products.count()

    else:
        products = Product.objects.filter(
            is_available=True,
            is_deleted=False,
            brand__is_active=True
        )

        if min_price is not None and max_price is not None:
            products = products.filter(productattribute__price__range=(min_price,max_price))
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'all_categories': all_categories,
        'selected_category': selected_category,
    }

    return render(request, 'userhome/shop.html', context)

#================================search======================================================================================================================================================================================

def search(request):
    q=request.GET['q']
    data = Product.objects.filter(product_name__icontains=q).order_by('-id')
    return render(request,'userhome/search.html',{'data':data})

#===============================click the product it view the product details========================================================================================================================

def product_details(request, product_id,category_id):
    user=request.user
    product = Product.objects.get(id=product_id)
    images = ProductImages.objects.filter(product=product)
    related_product=Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id','color__color_name','color__color_code','price','image').distinct()

    if request.method=="POST":
        if user.is_authenticated:
            print("request entered ")
            colour=request.POST.get('colorselect')
            qty=request.POST.get('quantity')
            product_colour=Color.objects.get(color_name=colour)
            products=ProductAttribute.objects.get(product=product,color=product_colour)
            item, created = CartItem.objects.get_or_create(user=user, product=products,defaults={'is_deleted': False})
            item.total=products.price*float(qty)
            print("Related Products:", related_product)

            #If the object was created, set the initial quantity
            if created:
                item.quantity = qty
            
            #already exists, update its quantity
            else:
                item.quantity += int(qty)
                item.save()
                item.total=products.price*item.quantity
        
            item.save()
            return redirect(cart_list)
        else:
            return redirect('user_login')

    
    context={
        'product': product,
        'related_product ': related_product,
        'colors' :colors,
        'images':images,
    }
    

    return render(request, 'userhome/product_details.html', context)
#======================================== cart-list page ==================================================================================================================================
@login_required(login_url='user_login')
def cart_list(request):
    user=request.user 
    items=CartItem.objects.filter(user=user, is_deleted=False)
  
    total = items.aggregate(total_sum=Sum('total'))['total_sum'] or 0
 
    return render(request,'userhome/cart.html',{'items':items,'total':total})
       
#========================================= delete cart item ================================================================================================================================================
@login_required(login_url='user_login')
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
    
    response_data = {'new_qty':new_quantity,'new_price':cart_item.total,'total':total_price}
    return JsonResponse(response_data)

@login_required(login_url='user_login')
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
    order_items = ProductOrder.objects.filter(user=request.user)
    # Retrieve or create the user's wallet
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0})
    
    # Retrieve wallet history
    wallethistory = WalletHistory.objects.filter(wallet=wallet)
    context={
        'user_address':user_address,
        'user_data' :request.user,
        'order_history': order_history,
        'order_items':order_items,
        'wallet':wallet,
        'wallethistory':wallethistory,
    }
    return render(request, 'userhome/user_account.html',context)
#========================== edit,delete address ==========================================================================================================================================================================
@login_required(login_url='user_login')
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, users=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            # Set the user for the address before saving
            form.instance.users = request.user
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
#====================================cancel order=============================================================================================================================================================
@login_required(login_url='user_login')
def order_items(request, order_number):
    order = get_object_or_404(CartOrder, id=order_number)
    product_orders = ProductOrder.objects.filter(order=order)
    for item in product_orders:
        # Calculate subtotal for each product
        item.subtotal = item.product_price * item.quantity
    context = {
        'order': order,
        'product_orders': product_orders,
        'order_total': sum(item.subtotal for item in product_orders),  # Calculate total
    }

    return render(request, 'userhome/user_order_history.html', context)
#=========================================password change=====================================================================================================================================================================

@login_required(login_url='user_login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        print(f'Entered password: {current_password}')
        print(f'Stored password: {request.user.password}')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Incorrect current password. Please try again.')
            return redirect('change_password')
        
        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match. Please try again.')
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        logout(request)
        return redirect('user_logout') 

    return render(request, 'userhome/change_password.html')


#=================================== wallet ===============================================================================================================================================================================
@login_required(login_url='user_login')
def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        if wallet:
            print(wallet.balance)
    except:
        wallet = Wallet.objects.create(user=request.user, balance=0)
    return render(request,'paymenthome/wallet.html',{'wallet':wallet})

#============================= cancel and return order ========================================================================================================================================================================
@login_required(login_url='user_login')
def cancell(request,order_number):
    try:
        order = CartOrder.objects.get(id=order_number)
        wallet = Wallet.objects.get(user=request.user)

        if order.payment.payment_method == 'Wallet' or order.payment.payment_method == 'Razorpay':
            wallet.balance += order.order_total
            wallet.save()
            WalletHistory.objects.create(
                        wallet=wallet,
                        type='Credited',
                        amount=order.order_total
                        )

            refunded_message = f'Amount of {order.order_total} refunded successfully to your wallet.'
            messages.success(request, refunded_message)
    
            for product_order in order.productorder_set.all():
                product_attribute = product_order.variations
                product_attribute.stock += product_order.quantity
                product_attribute.save()


        order.status = 'Cancelled'
        order.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except Exception as e:
        print(e)
       
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='user_login')
def return_order(request,order_number):
    try:
        order = CartOrder.objects.get(id=order_number)
        wallet = Wallet.objects.get(user=request.user)

        wallet.balance += order.order_total
        wallet.save()
        WalletHistory.objects.create(
                    wallet=wallet,
                    type='Credited',
                    amount=order.order_total
                    )

        refunded_message = f'Amount of {order.order_total} refunded successfully to your wallet.'
        messages.success(request, refunded_message)

        # Restore stock for each ordered product
        for product_order in order.productorder_set.all():
            product_attribute = product_order.variations
            product_attribute.stock += product_order.quantity
            product_attribute.save()


        order.status = 'Return'
        order.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except CartOrder.DoesNotExist:
        pass

    except Wallet.DoesNotExist:
      
        pass

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#======================================== wishlist==================================================================================================================================

def wishlist(request):
    if not request.user.is_authenticated:
        messages.info(request,'login to access wishlist')
        return redirect('log:user_login')
    else:
        context = {}
        try:
            wishlist=Wishlist.objects.get(user=request.user)
            wishlist_items=WishlistItems.objects.filter(wishlist=wishlist)
            context={
                'wishlist_items':wishlist_items
            }
        except:
            pass
    return render(request,'userhome/wishlist.html',context)


def add_wishlist(request,product_id):
    if not request.user.is_authenticated:
        messages.info(request,'login to access wishlist')
        return redirect('signin')
    else:
        try:
            wishlist=Wishlist.objects.get(user=request.user)
           
        except:
            wishlist=Wishlist.objects.create(user=request.user)
            

        product=get_object_or_404(Product,id=product_id)

        if WishlistItems.objects.filter(wishlist=wishlist, product=product).exists():
            messages.info(request, 'Product is already in your wishlist')
        else:
            WishlistItems.objects.create(wishlist=wishlist, product=product)
            messages.success(request, 'Product added to your wishlist successfully')
        
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_wishlist(request,wishlist_item_id):

    item=get_object_or_404(WishlistItems, id=wishlist_item_id)
    item.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def filter_product(request):    
    try:
        categories = request.GET.getlist('category[]')
        print("Selected Categories:", categories)
        

        min_price= request.GET['min_price']
        max_price= request.GET['max_price'] 

        products = Product.objects.filter(status=True).order_by('-id').distinct()
        
        products=products.filter(price__gte=min_price)
        products=products.filter(price__lte=max_price)
        print("All Products:", products)
        print("Selected Categories:", categories)

        if len(categories) > 0:
            products = products.filter(category__id__in=categories).distinct()
            print("Filtered Product :", products)

        data = render_to_string('userhome/product_list.html', {"products": products})
        return JsonResponse({"data": data})
    except Exception as e:
        return JsonResponse({"error": str(e)})