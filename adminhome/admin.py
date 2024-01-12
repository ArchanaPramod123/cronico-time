from django.contrib import admin
from .models import ProductOffer

class ProductOfferAdmin(admin.ModelAdmin):
    list_display=['title','product','start_date','end_date','discount','is_active','image']

# Register your models here.
admin.site.register(ProductOffer,ProductOfferAdmin)