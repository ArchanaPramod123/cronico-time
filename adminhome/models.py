from django.utils import timezone
from decimal import Decimal
from django.db import models
from home.models import Product,category

from django.core.validators import MinValueValidator, MaxValueValidator


class ProductOffer(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.discount_percentage}% Discount"

    def save(self, *args, **kwargs):
        if not isinstance(self.discount_percentage, Decimal):
            self.discount_percentage = Decimal(str(self.discount_percentage))
        super().save(*args, **kwargs)
    
class CategoryOffer(models.Model):
    category=models.ForeignKey(category,on_delete=models.SET_NULL, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.discount_percentage}% Discount"

    def save(self, *args, **kwargs):
        if not isinstance(self.discount_percentage, Decimal):
            self.discount_percentage = Decimal(str(self.discount_percentage))
        super().save(*args, **kwargs)

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    description1 = models.TextField(blank=True, null=True)
    description2 = models.TextField(blank=True, null=True)
    description3 = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active =models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def update_status(self):
        today = timezone.now().date()
        return self.start_date <= today <=self.end_date
    
class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    discount = models.PositiveBigIntegerField(help_text='discount in percentage')
    active = models.BooleanField(default=True)
    active_date = models.DateField()
    expiry_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

        
        


