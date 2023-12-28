from django.contrib import admin
from .models import *

class AddressAdmin(admin.ModelAdmin):
    list_display=['name','address','phone','district','pincode']
class CartOrderAdmin(admin.ModelAdmin):
    list_display=['user','total_amt','paid_status','order_date']
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display=['invoice_no','item','image_tag','qty','price','total']

# Register your models here.


admin.site.register(Address,AddressAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
