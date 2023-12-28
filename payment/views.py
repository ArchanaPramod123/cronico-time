from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddressForm
from home.models import *
from home.views import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import logging



#========================================== check out========================================================================================================================================

@login_required(login_url='user_login')
def checkout(request):
    total_amt = 0
    user_addresses = Address.objects.filter(users=request.user)

    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])

    if not request.user.is_authenticated:
        return redirect('user_login')

    address_form = AddressForm(request.POST or None)

    if request.method == 'POST':
        if 'use_existing_address' in request.POST:
            selected_address_id = request.POST.get('existing_address')
            selected_address = get_object_or_404(Address, id=selected_address_id)

            return render(request, 'paymenthome/payment.html', {
                'cart_data': request.session['cartdata'],
                'totalitems': len(request.session['cartdata']),
                'total_amt': total_amt,
                'selected_address': selected_address,
            })

        elif address_form.is_valid():
            address_instance = address_form.save(commit=False)
            address_instance.user = request.user
            address_instance.save()

            return render(request, 'paymenthome/payment.html', {
                'cart_data': request.session['cartdata'],
                'totalitems': len(request.session['cartdata']),
                'total_amt': total_amt,
                'new_address': address_instance,
            })

        else:
            print(address_form.errors)

    return render(request, 'paymenthome/checkout.html', {
        'cart_data': request.session['cartdata'],
        'totalitems': len(request.session['cartdata']),
        'total_amt': total_amt,
        'address_form': address_form,
        'user_addresses': user_addresses,
    })

#==================================================payment =========================================================================================================================

@login_required(login_url='user_login')
def payment(request):
    total_amt = 0

    if 'cartdata' in request.session:
 
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])

        #order
            order = CartOrder.objects.create(
                user=request.user,
                total_amt=total_amt
            )

            #Order items
            for p_id, item in request.session.get('cartdata').items():
                product_attr = ProductAttribute.objects.filter(product=p_id).first()

                print('id:'+ p_id)

                item_s = CartOrderItems.objects.create(
                    order=order,
                    invoice_no=f'INV-{order.id}',
                    item=item['name'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price'])
                )

                #stock update
                product_attr.stock -= int(item['qty'])
                product_attr.save()

        # Clear the cart session
        del request.session['cartdata']

        # Redirect to the success page
        messages.success(request, 'Order placed successfully!')
        return redirect('payment_success')

    context = {
        'cart_data': request.session['cartdata'],
        'totalitems': len(request.session['cartdata']),
        'total_amt': total_amt,
        'item_s': item_s,
    }

    return render(request, 'paymenthome/payment.html', context)

#======================================== payment success or payment failed=======================================================================================================================

@login_required(login_url='user_login')
def payment_success(request):
    return render(request, 'paymenthome/payment-success.html')

@login_required(login_url='user_login')
def payment_failed(request):
    return render(request, 'paymenthome/payment-failed.html')

#===============================================================================================================================================================
