from .models import *
from django.db.models import Min,Max
from payment.models import CartItem
def get_filter(request):
    cats=Product.objects.distinct().values('category__category_name','category__id')
    brands=Product.objects.distinct().values('brand__brand_name','brand__id')
    colors=ProductAttribute.objects.distinct().values('color__color_name','color__id','color__color_code')
    min_max_price = ProductAttribute.objects.aggregate(Min("price"),Max('price'))

    # Get cart and wishlist counts
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_deleted=False)
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
        wishlist_count = wishlist_items.count()
    data = {
        'cats' : cats,
        'brands' : brands,
        'colors' : colors,
        'min_max_price':min_max_price,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,

    }
    return data

    
