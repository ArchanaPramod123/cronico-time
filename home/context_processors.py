from .models import *
def get_filter(request):
    cats=Product.objects.distinct().values('category__category_name','category__id')
    brands=Product.objects.distinct().values('brand__brand_name','brand__id')
    colors=ProductAttribute.objects.distinct().values('color__color_name','color__id','color__color_code')
    data = {
        'cats' : cats,
        'brands' : brands,
        'colors' : colors,
    }
    return data
