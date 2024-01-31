from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddressForm
from home.models import *
from home.views import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
import logging
from django.db.models import Sum
from django.urls import reverse
from datetime import datetime
from django.views.decorators.cache import never_cache
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


#========================================== check out========================================================================================================================================
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def checkout(request):
    user=request.user 
    items=CartItem.objects.filter(user=user, is_deleted=False)
    user_addresses = Address.objects.filter(users=request.user)
    # total = items.aggregate(total_sum=Sum('total'))['total_sum']
    
    address_form = AddressForm(request.POST or None)
    # Retrieve the totals, total, and discounts from the cart_list view context
    totals = request.session.get('totals', 0)
    total = request.session.get('total', 0)
    discounts = request.session.get('discounts', 0)

    # Get wallet balance
    wallet = Wallet.objects.filter(user=user).first()
    wallet_balance = wallet.balance if wallet else 0
    print('Wallet balance:', wallet_balance)

    # Check if the wallet balance is sufficient for the order
    wallet_button_disabled = total > wallet_balance
    print(total)
    print(totals)
    print(discounts)

     # Check if the order_placed flag is present in the session
    if request.session.get('order_placed', False):
        # Clear the flag to allow normal navigation
        del request.session['order_placed']
        # messages.success(request, 'Order placed successfully!')
        return redirect('user_index')  # Replace 'index' with your actual index URL or name


    if request.method == 'POST':
        print("entered")
        if 'use_existing_address' in request.POST:
            selected_address_id = request.POST.get('existing_address')
            selected_address = get_object_or_404(Address, id=selected_address_id)
            # Update the address for all CartItems in the user's cart
            CartItem.objects.filter(user=user, is_deleted=False).update(address=selected_address)


            return render(request, 'paymenthome/payment.html', {
               
                'selected_address': selected_address,
                'items':items,
                'total':total,
                'totals':totals,
                'discounts': discounts,
                'wallet_balance': wallet_balance,
                'wallet_button_disabled': wallet_button_disabled,
            })
        
        elif address_form.is_valid():
            address_instance = address_form.save(commit=False)
            address_instance.user = request.user
            address_instance.save()

            # Update the address for all CartItems in the user's cart
            CartItem.objects.filter(user=user, is_deleted=False).update(address=address_instance)


            return render(request, 'paymenthome/payment.html', {
             
                'new_address': address_instance,
                'items':items,
                'total':total,
                'totals':totals,
                'discounts': discounts,
                'wallet_balance': wallet_balance,
                'wallet_button_disabled': wallet_button_disabled,
            })
    

    return render(request, 'paymenthome/checkout.html',{'user_addresses': user_addresses,'items':items,'total':total,'totals':totals,'discounts': discounts})
#==================================================payment =========================================================================================================================
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def payment(request):
    print("Entering payment")
    user=request.user 
    items=CartItem.objects.filter(user=user, is_deleted=False)
    user_addresses = Address.objects.filter(users=request.user)
    # total = items.aggregate(total_sum=Sum('total'))['total_sum'] # Rs. 200'
    totals = request.session.get('totals', 0)
    total = request.session.get('total', 0)
    discounts = request.session.get('discounts', 0)

     # Check if the order_placed flag is present in the session
    if request.session.get('order_placed', False):
        # Clear the flag to allow normal navigation
        del request.session['order_placed']
        # messages.success(request, 'Order placed successfully!')
        return redirect('user_index')  # Replace 'index' with your actual index URL or name


    if request.method == "POST":
        # Only attempt to get 'amount' from POST if the form is submitted
        amount = request.POST.get('total', 0)
        amount = int(amount)
    
        currency = 'INR'
        amount_in_paise = amount * 100  
 
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount_in_paise,
                                                           currency=currency,
                                                           payment_capture='0'))
 
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'
 
        # we need to pass these details to frontend.
        context = {
            'total': total,
            'items': items,
            'totals': totals,
            'discounts': discounts,
            'user_addresses': user_addresses,
        }
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount_in_paise
        context['currency'] = currency
        context['callback_url'] = callback_url
 
        return render(request, 'paymenthome/payment.html', context=context)

    # if request.method == "POST":
    #     amount=request.POST.get('total')
    
    # amount = int(amount)

    # currency = 'INR'
    # amount_in_paise = amount * 100  
 
    # # Create a Razorpay Order
    # razorpay_order = razorpay_client.order.create(dict(amount=amount_in_paise,
    #                                                    currency=currency,
    #                                                    payment_capture='0'))
 
    # # order id of newly created order.
    # razorpay_order_id = razorpay_order['id']
    # callback_url = 'paymenthandler/'
 
    # # we need to pass these details to frontend.
    # context = {
    #     'total': total,
    #     'items': items,
    #     'totals':totals,
    #     'discounts': discounts,
    #     'user_addresses': user_addresses,
        
    # }
    # context['razorpay_order_id'] = razorpay_order_id
    # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    # context['razorpay_amount'] = amount_in_paise
    # context['currency'] = currency
    # context['callback_url'] = callback_url
 
    # return render(request, 'paymenthome/payment.html', context=context)
 
@csrf_exempt
def paymenthandler(request):
    print("Wnt to join")
    user = request.user 
    items = CartItem.objects.filter(user=user, is_deleted=False)
    user_addresses = Address.objects.filter(users=request.user)
    total = items.aggregate(total_sum=Sum('total'))['total_sum']

    print(total,"totallllllllllll")

    if request.method == "POST":
        print(request.POST.dict())
        amount = request.POST.get('total')
        print(amount, "amount")

        try:
            # get the required parameters from post request.

            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id,"paymentid")
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            print(razorpay_order_id,"razorpayid")
            signature = request.POST.get('razorpay_signature', '')
            print(signature,"signaturessss")

            # create a dictionary with the required parameters for signature verification
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
              # Include the amount parameter for verification

            }

            # verify the payment signature
            # result = razorpay_client.utility.verify_payment_signature(params_dict,settings.RAZOR_KEY_SECRET)
            if payment_id:
                # if the signature is valid, capture the payment
                # razorpay_client.payment.capture(payment_id,int(amount))

                # Call the online_place_order function upon successful payment
                print("Redirecting to order_success page")
                # online_place_order(request)
                return redirect(online_place_order)
                # render success page on successful capture of payment
                # return render(request, 'paymenthome/payment_success.html')
            else:
                # if signature verification fails, render the failure page
                return render(request, 'paymenthome/payment_failed.html')
        except Exception as e:
            # if there is an error, render the failure page
            print("Error in paymenthandler:", str(e))
            return render(request, 'paymenthome/payment_failed.html')
    else:
        # if other than POST request is made, return a bad request response
        return HttpResponseBadRequest()

def online_place_order(request):
    user = request.user 
    items = CartItem.objects.filter(user=user, is_deleted=False)
    # total = items.aggregate(total_sum=Sum('total'))['total_sum']
    request.session.get('applied_coupon_id', None)  
    request.session.get('totals', 0)
    total = request.session.get('total', 0)
    request.session.get('discounts', 0)

     # Check if the order_placed flag is present in the session
    if request.session.get('order_placed', False):
        # Clear the flag to allow normal navigation
        del request.session['order_placed']
        # messages.success(request, 'Order placed successfully!')
        return redirect('user_index')  # Replace 'index' with your actual index URL or name

    adress=Address.objects.filter(users=request.user).first()
    # if request.method == "POST":
     # Initialize an empty list to store coupons
    coupons = []

    for item in items:
        # Access coupon for each item
        coupon = item.coupon
        coupons.append(coupon)

    # Check if there are any items in the cart and get the first coupon if available
    if coupons:
        coupon = coupons[0]
    else:
        coupon = None
    
        
    short_id = str(random.randint(1000, 9999))
    yr = datetime.now().year
    dt = int(datetime.today().strftime('%d'))
    mt = int(datetime.today().strftime('%m'))
    d = datetime(yr, mt, dt).date()
    payment_id = f"PAYMENT-{timezone.now().strftime('%Y%m%d%H%M%S')}"

    current_date = d.strftime("%Y%m%d")
    short_id = str(random.randint(1000, 9999))
    order_numbers = current_date + short_id 

    var=CartOrder.objects.create(
        user=request.user,
        # payment='Razorpay',
        order_number=order_numbers,
        coupen=coupon,
        order_total= total,
        selected_address=adress,
        ip=request.META.get('REMOTE_ADDR')    
        )
    var.save()
    payment_instance=Payments.objects.create(
        user=request.user,
        payment_id=payment_id,
        payment_method='Razorpay',
        amount_paid= total,
        status='paid',
                
        )
        
    var.payment=payment_instance
    var.save()
    cart=CartItem.objects.filter(user=request.user)
            
    for item in cart:
        orderedproduct=ProductOrder()
        item.product.stock-=item.quantity
        item.product.save()
        orderedproduct.order=var
        orderedproduct.payment=payment_instance
        orderedproduct.user=request.user
        orderedproduct.product=item.product.product
        orderedproduct.quantity=item.quantity
        orderedproduct.product_price=item.product.price
        product_attribute = ProductAttribute.objects.get(product=item.product.product, color=item.product.color)
        orderedproduct.variations = product_attribute
        orderedproduct.ordered=True
        orderedproduct.save()
        item.delete() 
    request.session.pop('applied_coupon_id', None)    
    request.session.pop('totals', 0)
    total = request.session.pop('total', 0)
    request.session.pop('discounts', 0) 

    return redirect('order_success')

#================================================== payment in COD =========================================================================================================================

def place_order(request):
    print('helooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
    user = request.user 
    items = CartItem.objects.filter(user=user, is_deleted=False)
    # total = items.aggregate(total_sum=Sum('total'))['total_sum']
    request.session.get('applied_coupon_id', None)  
    request.session.get('totals', 0)
    total = request.session.get('total', 0)
    request.session.get('discounts', 0)
     # Check if the order_placed flag is present in the session
    if request.session.get('order_placed', False):
        # Clear the flag to allow normal navigation
        del request.session['order_placed']
        # messages.success(request, 'Order placed successfully!')
        return redirect('user_index')  # Replace 'index' with your actual index URL or name

    adress=Address.objects.filter(users=request.user).first()
    print(total,"totallllllllllllllllllllllllllllllllllllllllllllll")
    print("we;come to insieeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    short_id = str(random.randint(1000, 9999))
    yr = datetime.now().year
    dt = int(datetime.today().strftime('%d'))
    mt = int(datetime.today().strftime('%m'))
    d = datetime(yr, mt, dt).date()
    payment_id = f"PAYMENT-{timezone.now().strftime('%Y%m%d%H%M%S')}"

    current_date = d.strftime("%Y%m%d")
    short_id = str(random.randint(1000, 9999))
    order_numbers = current_date + short_id 
    # Initialize an empty list to store coupons
    coupons = []

    for item in items:
        # Access coupon for each item
        coupon = item.coupon
        coupons.append(coupon)

    # Check if there are any items in the cart and get the first coupon if available
    if coupons:
        coupon = coupons[0]
    else:
        coupon = None

    var=CartOrder.objects.create(
        user=request.user,
        # payment='Razorpay',
        order_number=order_numbers,
        order_total= total,
        coupen=coupon,
        selected_address=adress,
        ip=request.META.get('REMOTE_ADDR')    
    )
    var.save()
    payment_instance=Payments.objects.create(
        user=request.user,
        payment_id=payment_id,
        payment_method='COD',
        amount_paid= total,
        status='Pending',
                
    )
        
    var.payment=payment_instance
    var.save()
            
    cart=CartItem.objects.filter(user=request.user)
            
    for item in cart:
        orderedproduct=ProductOrder()
        item.product.stock-=item.quantity
        item.product.save()
        orderedproduct.order=var
        orderedproduct.payment=payment_instance
        orderedproduct.user=request.user
        orderedproduct.product=item.product.product
        orderedproduct.quantity=item.quantity
        orderedproduct.product_price=item.product.price
        product_attribute = ProductAttribute.objects.get(product=item.product.product, color=item.product.color)
        orderedproduct.variations = product_attribute
        orderedproduct.ordered=True
        orderedproduct.save()
        item.delete()  
    # Check if the key exists before popping it from the session
    if 'applied_coupon_id' in request.session:
        request.session.pop('applied_coupon_id')     
    request.session.pop('totals')
    total = request.session.pop('total')
    request.session.pop('discounts')
        
    return redirect('order_success')

#============================= wallet order place=========================================================================================================================================
def wallet_place_order(request):
    print("wallettttttttttttttttttt")
    try:
        print("insideeeee walletttttttttttttttttttttttttt")
        user = request.user
        items = CartItem.objects.filter(user=user, is_deleted=False)
        # total = items.aggregate(total_sum=Sum('total'))['total_sum']
        request.session.get('applied_coupon_id', None)  
        request.session.get('totals', 0)
        total = request.session.get('total', 0)
        request.session.get('discounts', 0)
         # Check if the order_placed flag is present in the session
        if request.session.get('order_placed', False):
            # Clear the flag to allow normal navigation
            del request.session['order_placed']
            # messages.success(request, 'Order placed successfully!')
            return redirect('user_index')  # Replace 'index' with your actual index URL or name

        address = Address.objects.filter(users=request.user).first()
         # Initialize an empty list to store coupons
        coupons = []

        for item in items:
            # Access coupon for each item
            coupon = item.coupon
            coupons.append(coupon)

        # Check if there are any items in the cart and get the first coupon if available
        if coupons:
            coupon = coupons[0]
        else:
            coupon = None

        try:
            print("inside the wallet tryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            wallet = Wallet.objects.get(user=request.user)
            if total <= wallet.balance:
                short_id = str(random.randint(1000, 9999))
                yr = datetime.now().year
                dt = int(datetime.today().strftime('%d'))
                mt = int(datetime.today().strftime('%m'))
                d = datetime(yr, mt, dt).date()
                current_date = d.strftime("%Y%m%d")
                short_id = str(random.randint(1000, 9999))
                order_numbers = current_date + short_id

                var = CartOrder.objects.create(
                    user=request.user,
                    order_number=order_numbers,
                    order_total=total,
                    coupen=coupon,
                    selected_address=address,
                    ip=request.META.get('REMOTE_ADDR')
                )
                var.save()

                payment_instance = Payments.objects.create(
                    user=request.user,
                    payment_id=f"PAYMENT-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    payment_method='Wallet', 
                    amount_paid=total,
                    status='paid',
                )

                var.payment = payment_instance
                var.save()

                cart = CartItem.objects.filter(user=request.user)

                for item in cart:
                    orderedproduct = ProductOrder()
                    item.product.stock -= item.quantity
                    item.product.save()
                    orderedproduct.order = var
                    orderedproduct.payment = payment_instance
                    orderedproduct.user = request.user
                    orderedproduct.product = item.product.product
                    orderedproduct.quantity = item.quantity
                    orderedproduct.product_price = item.product.price
                    product_attribute = ProductAttribute.objects.get(product=item.product.product, color=item.product.color)
                    orderedproduct.variations = product_attribute
                    orderedproduct.ordered = True
                    orderedproduct.save()
                    item.delete()

                wallet.balance -= total
                wallet.save()

                WalletHistory.objects.create(
                    wallet=wallet,
                    type='Debit',
                    amount=total,
                    reason='Order Placement'
                )
                request.session.pop('applied_coupon_id',None)   
                request.session.pop('totals', 0)
                total = request.session.pop('total', 0)
                request.session.pop('discounts', 0)

                return redirect('order_success')

            else:
                print("else in teyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                messages.error(request, 'Wallet balance is less than the total amount')
                # payment_url = reverse('payment') + '?from_wallet=true'
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                # return redirect('payment')
                # return render(request, 'paymenthome/checkout.html', {
                #     'error_message': 'Wallet balance is less than the total amount',
                # })
            
        except Wallet.DoesNotExist:
            print("except in the try")
            messages.error(request, 'Wallet not found for the user')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except Exception as e:
        print("an error occureeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        print(f"An error occurred: {e}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @cache_page()    
@login_required(login_url='user_login')
def order_success(request):
    order = CartOrder.objects.filter(user=request.user).order_by('-id').first()
    print(order) 
    product_orders = ProductOrder.objects.filter(order=order)
    
    
    request.session['order_placed'] = True
    context = {
        'order':order,
        'order_number': order.order_number,
        'order_status': order.status,
        'product_orders': product_orders,
    }
    return render(request,'paymenthome/orderdetail.html',context)


#=================== invoice after the user order place ====================================================================================================================================================
def invoice(request,order_id,total=0):
    try:
        order=CartOrder.objects.get(id=order_id)
        orders=ProductOrder.objects.filter(order=order)

    except:
        pass
    coupon = order.coupen
    grand_total = order.order_total
    for item in orders:
        item.subtotal=item.quantity * item.product_price
        total += item.subtotal
    context={
        'order':order,
        'orders':orders,
        'grand_total':grand_total,
        'coupon':coupon,
    }

    return render(request,'paymenthome/invoice.html',context) 

#=========================================== THE END ============================================================================================================================================================

 

