from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render,redirect
from home.models import *
from payment.models import *
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login,logout
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from home.forms import *
from .forms import OrderForm
from django.db.models import Count
from django.db.models.functions import TruncDate,TruncMonth, TruncYear
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import ProductOffer
from .forms import ProductOfferForm
# Create your views here.

#======================================= admin login and logout =================================================================================================================================

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=authenticate(request, email=email,password=password)
        if user is not None and user.is_active and user.is_superadmin and user.is_staff and user.is_admin :
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('admin_index')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'adminhome/adminlogin.html')
    return render(request, 'adminhome/adminlogin.html')

def admin_logout(request):
    logout(request)
    return render(request,'adminhome/adminlogin.html')

#========================================== admin index page ====================================================================================================================================================

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_index(request):
    if not request.user.is_superadmin:
        return redirect('admin_login')
 
    product_count=Product.objects.count()
    category_count=category.objects.count()
    orders=CartOrder.objects.all()
    last_orders= CartOrder.objects.order_by('-created_at')[:5]
    orders_count=orders.count()
    total_users_count = User.objects.count()
    total = 0
    for order in orders:
        if order.status == 'Delivered':
            total += order.order_total
            
        if (order.payment and order.payment.payment_method == 'Razorpay') or (order.payment and order.payment.payment_method == 'Wallet'):
            total += order.order_total
    revenue=int(total)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    print('Start Date:', start_date)
    print('End Date:', end_date)

    daily_order_counts = (
            CartOrder.objects
            .filter(created_at__range=(start_date, end_date))
            .values('created_at')
            .annotate(order_count=Count('id'))
            .order_by('created_at')
        )
    print(f'daily orrderr {daily_order_counts}')
    print('SQL Query:', daily_order_counts.query)
    dates = [entry['created_at'].strftime('%Y-%m-%d') for entry in daily_order_counts]
    counts = [entry['order_count'] for entry in daily_order_counts]
    print('Daily Chart Data:')
    print('Dates:', [entry['created_at'] for entry in daily_order_counts])
    print('Counts:', [entry['order_count'] for entry in daily_order_counts])
    print(dates)
    print(counts)
    
    monthly_order_counts = (
        CartOrder.objects
        .filter(created_at__year=datetime.now().year)  
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(order_count=Count('id'))
        .order_by('month')
    )
    monthlyDates = [entry['month'].strftime('%Y-%m') for entry in monthly_order_counts]
    monthlyCounts = [entry['order_count'] for entry in monthly_order_counts]

    
    yearly_order_counts = (
        CartOrder.objects
        .annotate(year=TruncYear('created_at'))
        .values('year')
        .annotate(order_count=Count('id'))
        .order_by('year')
    )
    yearlyDates = [entry['year'].strftime('%Y') for entry in yearly_order_counts]
    yearlyCounts = [entry['order_count'] for entry in yearly_order_counts]

    statuses = ['Delivered','Paid','Pending', 'New', 'Conformed', 'Cancelled', 'Return','Shipped']
    order_counts = [CartOrder.objects.filter(status=status).count() for status in statuses]

    
    context={
        'product_count':product_count,
        'category_count':category_count,
        'orders_count':orders_count,
        'dates': dates,
        'counts': counts,
        'monthlyDates':monthlyDates,
        'monthlyCounts':monthlyCounts,
        'yearlyDates':yearlyDates,
        'yearlyCounts':yearlyCounts,
        'last_orders': last_orders,
        'revenue':revenue,
        'total_users_count': total_users_count,
        'statuses': statuses,
        'order_counts': order_counts,
    }

   

    return render(request, 'adminhome/adminindex.html', context)

#==================================================admin view add edit the category ========================================================================================================

@login_required(login_url='admin_login')
def admin_category(request):
    data=category.objects.all()
    context={
        'data':data
    }
    return render(request, 'adminhome/category.html', context)

@login_required(login_url='admin_login')
def admin_category_insert(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        new_cat = category(category_name=category_name)
        new_cat.save()
        return redirect('admin_category')
    return render(request,'adminhome/category.html')

@login_required(login_url='admin_login')
def admin_category_edit(request,id):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        # slug = request.POST.get('slug')
        edit=category.objects.get(id=id)
        edit.category_name = category_name
        # edit.slug = slug
        edit.save()
        return redirect('admin_category')
    obj = category.objects.get(id=id)
    context = {
        "obj":obj
    }
    return render(request,'adminhome/category_edit.html', context)

#=============================================== Brand list,add,edit and block =============================================================================================================

@login_required(login_url='admin_login')
def admin_brand(request):
    data=Brand.objects.all()
    context={
        'data':data
    }
    return render(request, 'adminhome/brand.html', context)

@login_required(login_url='admin_login')
def admin_brand_insert(request):
    if request.method == 'POST':
        brand_name = request.POST.get('name')
        new_cat = Brand(brand_name=brand_name)
        new_cat.save()
        return redirect('admin_brand')
    return render(request,'adminhome/brand.html')

@login_required(login_url='admin_login')
def admin_brand_edit(request,id):
    if request.method == 'POST':
        brand_name = request.POST.get('name')
        edit=Brand.objects.get(id=id)
        edit.brand_name = brand_name
        edit.save()
        return redirect('admin_brand')
    obj = Brand.objects.get(id=id)
    context = {
        "obj":obj
    }
    return render(request,'adminhome/brand_edit.html', context)

@login_required(login_url='admin_login')
def brand_available(request, brand_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    if not request.user.is_superadmin:
        return redirect('admin_login')
    
    brand = get_object_or_404(Brand, id=brand_id)
    
    if brand.is_active:
        brand.is_active=False
       
    else:
        brand.is_active=True
    brand.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#=================================================== color list, add, edit ==========================================================================================================

@login_required(login_url='admin_login')
def admin_color(request):
    data=Color.objects.all()
    context={
        'data':data
    }
    return render(request, 'adminhome/color.html', context)

@login_required(login_url='admin_login')
def admin_color_insert(request):
    if request.method == 'POST':
        color_name = request.POST.get('name')
        color_code = request.POST.get('code')
        new_cat = Color(color_name=color_name,color_code=color_code)
        new_cat.save()
        return redirect('admin_color')
    return render(request,'adminhome/color.html')

@login_required(login_url='admin_login')
def admin_color_edit(request,id):
    if request.method == 'POST':
        color_name = request.POST.get('name')
        color_code = request.POST.get('code')
        edit=Color.objects.get(id=id)
        edit.color_name = color_name
        edit.color_code = color_code
        edit.save()
        return redirect('admin_color')
    obj = Color.objects.get(id=id)
    context = {
        "obj":obj
    }
    return render(request,'adminhome/color_edit.html', context)

#=========================================== admin add, list, edit, delete product =========================================================================================================

@login_required(login_url='admin_login')
def admin_product(request):
    item = Product.objects.filter(is_deleted=False)
    context = {
        "item":item
    }
    return render(request,'adminhome/product.html', context)

@login_required(login_url='admin_login')
def admin_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.save()
            images=request.FILES.getlist('images')
            for img in images:
                ProductImages.objects.create(product=product,images=img)
            return redirect('admin_product')
    else:
        form = ProductForm()    

    brands = Brand.objects.all()
    categories = category.objects.all()

    context = {
        'brands': brands,
        'categories': categories,
        'form' : form,
    }
    return render(request,'adminhome/product_add.html',context)

@login_required(login_url='admin_login')
def admin_product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    images = product.product_image.all()
    brands = Brand.objects.all()
    categories = category.objects.all()

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        images_form = ProductImagesForm(request.POST, request.FILES)

        # Check if the delete_image checkboxes are checked for any existing images
        for img in images:
            if f'delete_image_{img.id}' in request.POST:
                img.delete()

        # Continue with the product update logic
        if product_form.is_valid() and images_form.is_valid():
            product_form.save()

            # Save the images form separately to handle new images
            images_form.save()
            return redirect('admin_product')

    else:
        product_form = ProductForm(instance=product)
        images_form = ProductImagesForm()

    context = {
        'product': product,
        'brands': brands,
        'categories': categories,
        'images': images,
        'product_form': product_form,
        'images_form': images_form,
    }

    return render(request, 'adminhome/product_edit.html', context)

def admin_product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('admin_product')

    context = {'product': product}
    return render(request, 'adminhome/product_delete.html', context)
    
#=====================================varient list, add, edit and delete ===============================================================================================================================================================

@login_required(login_url='admin_login')
def admin_varient(request):
    cat=category.objects.all()
    item = ProductAttribute.objects.filter(is_deleted=False)
    context = {
        "item":item,
        "cat":cat
    }
    return render(request,'adminhome/varient.html', context)

@login_required(login_url='admin_login')
def admin_varient_add(request):
    if request.method == 'POST':
        form = ProductAttributeForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('admin_varient')
    else:
        form = ProductAttributeForm()    

    brands = Brand.objects.all()
    categories = category.objects.all()

    context = {
        'brands': brands,
        'categories': categories,
        'form' : form,
    }
    return render(request, 'adminhome/varient_add.html', context)

@login_required(login_url='admin_login')
def admin_varient_edit(request, id):
    product = get_object_or_404(ProductAttribute, id=id)

    if request.method == 'POST':
        product_form = ProductAttributeForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('admin_varient')

    else:
        product_form = ProductAttributeForm(instance=product)

    context = {
        'product_form': product_form,
        'product': product,
    }

    return render(request, 'adminhome/varient_edit.html', context)

def admin_varient_delete(request, id):
    product = get_object_or_404(ProductAttribute, id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('admin_varient')

    context = {'product': product}
    return render(request, 'adminhome/product_delete.html', context)

#==================================================admin can view the customers list======================================================================================================================================

@login_required(login_url='admin_login')
def customers(request):
    user = User.objects.all()
    context = {
        'user':user
    }
    return render(request, 'adminhome/customers.html',context)

#================================================== admin can block and unblock the user =======================================================================================================
  
@login_required(login_url='admin_login')
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Toggle the is_active field
    user.is_active = not user.is_active
    user.save()

    messages.success(request, f'{user.username} has been {"blocked" if not user.is_active else "unblocked"}.')

    return redirect('customers')
#================================================ order and order product in admin side  ==============================================================================================================================================
@login_required(login_url='admin_login')
def order(request):
    if not request.user.is_superadmin:
        return redirect('admin_login')
    
    status='all'
    order = CartOrder.objects.order_by('-created_at')
    form = OrderForm(request.POST or None)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            if status != 'all':
                order = order.filter(status=status)

    context = {
        'order':order,
        'form':form,
        'status':status
    }
    return render(request, 'adminhome/order.html',context)

@login_required(login_url='admin_login')
def orderitems(request,order_number):
    if not request.user.is_superadmin:
        return redirect('admin_login')
    try:
        order=CartOrder.objects.get(id=order_number)

    except Exception as e:
        print(e)
    order_items=ProductOrder.objects.filter(order=order)
    address=order.selected_address
    payment = Payments.objects.all()
    
    
    if request.method=="POST":
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orderitems', order_number = order.pk)
        else:
            messages.error(request, "choose status")
            return redirect('orderitems', order_number = order.pk)


    form=OrderForm(instance=order)
    
    context={
        'order':order,
        'address':address,
        'order_items':order_items,
        'form':form,
        'payment':payment
            }
    return render(request, 'adminhome/order_items.html',context)

#==================== show the status in the order page in admin ========================================================================================================================
def cancell_order(request,order_number):
    if not request.user.is_superadmin:
        return redirect('admin_login')
    
    try:
        order=CartOrder.objects.get(id=order_number)
    except Exception as e:
        print(e)
    
    order.status = 'Cancelled'
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#=============================================================================================================================================================================================================

def sales_report(request):
    if not request.user.is_superadmin:
        return redirect(admin_login)
    start_date_value = ""
    end_date_value = ""
    try:
        orders=CartOrder.objects.filter(is_ordered= True).order_by('-created_at')
    except:
        pass
    if request.method == 'POST':
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date
        if start_date and end_date:
          
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

           
            orders = orders.filter(created_at__range=(start_date, end_date))
   
    context={
        'orders':orders,
        'start_date_value':start_date_value,
        'end_date_value':end_date_value
    }

    return render(request,'adminhome/sales_report.html',context)

def add_product_offer(request):
    try:
        product_offers = ProductOffer.objects.all()
    except:
        pass
    if request.method == 'POST':
        form = ProductOfferForm(request.POST, request.FILES)
        if form.is_valid():
            product_offer = form.save()
            product = product_offer.product
             

            # Assuming each product can have multiple product attributes
            product_attributes = ProductAttribute.objects.filter(product=product)

            if product_attributes.exists():
                # Take the first product attribute for simplicity
                product_attribute = product_attributes.first()
                
                discount = product_offer.discount

                # Calculate discounted price for the product attribute
                discounted_price = product_attribute.price - ((discount / 100) * product_attribute.price)

                # Update the product attribute with the discounted price
                product_attribute.price = discounted_price
                product_attribute.save()

                # Save the product offer
                product_offer.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
           
    else:
        form = ProductOfferForm()
     
    return render(request, 'adminhome/product_offer.html',{'form': form , 'product_offers': product_offers})

def delete_offer(request,offer_id):
    product_offer = get_object_or_404(ProductOffer, pk=offer_id)
    product_offer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  