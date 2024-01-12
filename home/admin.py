from django.contrib import admin
from .models import *

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class CategoryAdmin(admin.ModelAdmin):
    list_display=['category_name']
class BrandAdmin(admin.ModelAdmin):
    list_display=['brand_name']
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display=['product_name','category','is_available']
class ColorAdmin(admin.ModelAdmin):
    list_display=['color_name','color_code']
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=['id','product','price','color','stock','image_tag']
class WishlistUserAdmin(admin.ModelAdmin):
    list_display = ('user',) 
    search_fields = ('user',)
class WishlistUserItemsAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product')
    search_fields = ('wishlist',)



# Register your models here.

admin.site.register(User)
admin.site.register(category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Color)
admin.site.register(ProductAttribute,ProductAttributeAdmin)
admin.site.register(Wishlist, WishlistUserAdmin)
admin.site.register(WishlistItems, WishlistUserItemsAdmin)


