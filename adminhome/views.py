from django.shortcuts import render,redirect
from home.models import *
from payment.models import *
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login,logout
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from home.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

#=======================================admin login=================================================================================================================================

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

#===================================================admin index page==================================================================================================================

@login_required(login_url='admin_login')
def admin_index(request):
    return render(request, 'adminhome/adminindex.html')

#==================================================admin view the category========================================================================================================

@login_required(login_url='admin_login')
def admin_category(request):
    data=category.objects.all()
    context={
        'data':data
    }
    return render(request, 'adminhome/category.html', context)

#================================================admin add new,edit category====================================================================================================================

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
        slug = request.POST.get('slug')
        edit=category.objects.get(id=id)
        edit.category_name = category_name
        edit.slug = slug
        edit.save()
        return redirect('admin_category')
    obj = category.objects.get(id=id)
    context = {
        "obj":obj
    }
    return render(request,'adminhome/category_edit.html', context)

#=============================================== Brand list,add,edit =============================================================================================================

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
    
#=====================================varient list, add, edit===============================================================================================================================================================

@login_required(login_url='admin_login')
def admin_varient(request):
    item = ProductAttribute.objects.filter(is_deleted=False)
    context = {
        "item":item
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

#========================================================= oder and order items================================================================================================================================================

@login_required(login_url='admin_login')
def order(request):
    order = CartOrder.objects.all()
    context = {
        'order':order
    }
    return render(request, 'adminhome/order.html',context)

@login_required(login_url='admin_login')
def orderitems(request):
    orderitems = CartOrderItems.objects.all()
    context = {
        'orderitems':orderitems
    }
    return render(request, 'adminhome/order_items.html',context)


#================================================== admin can block and unblock the user =======================================================================================================
  
@login_required(login_url='admin_login')
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Toggle the is_active field
    user.is_active = not user.is_active
    user.save()

    messages.success(request, f'{user.username} has been {"blocked" if not user.is_active else "unblocked"}.')

    return redirect('customers')




