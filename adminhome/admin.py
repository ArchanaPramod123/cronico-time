from django.contrib import admin
from .models import ProductOffer,CategoryOffer,Banner,Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display=['code','discount','active','active_date','expiry_date','created_date']
# Register your models here.
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(Banner)
admin.site.register(Coupon,CouponAdmin)

