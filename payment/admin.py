from django.contrib import admin
from .models import *

class AddressAdmin(admin.ModelAdmin):
    list_display=['name','address','phone','district','pincode']
class CartOrderAdmin(admin.ModelAdmin):
    list_display=['user','order_total','payment','status','selected_address','created_at','updated_at']
class PaymentsAdmin(admin.ModelAdmin):
    list_display=['user','payment_id','payment_method','amount_paid','status','created_at']
class ProductOrderAdmin(admin.ModelAdmin):
    list_display=['order','payment','user','product','quantity','product_price','ordered','created_at','updated_at','variations']
class UserWallet(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user',)
class UserWalletHistory(admin.ModelAdmin):
    list_display=('wallet','type','created_at','amount')
    search_fields=('Walet',)
# class CartOrderItemsAdmin(admin.ModelAdmin):
#     list_display=['invoice_no','item','image_tag','qty','price','total']

# Register your models here.




admin.site.register(Address,AddressAdmin)
admin.site.register(CartItem)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(Payments,PaymentsAdmin)
admin.site.register(ProductOrder,ProductOrderAdmin)
admin.site.register(Wallet,UserWallet)
admin.site.register(WalletHistory,UserWalletHistory)
# admin.site.register(CartOrderItems,CartOrderItemsAdmin)
