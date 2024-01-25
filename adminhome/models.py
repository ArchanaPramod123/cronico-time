from decimal import Decimal
from django.db import models
from home.models import Product,category

from django.core.validators import MinValueValidator, MaxValueValidator

# # Create your models here.
# class ProductOffer(models.Model):
#     title = models.CharField(max_length=100)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productoffer_set')
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField()
#     discount = models.DecimalField( max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Discount percentage")
#     is_active = models.BooleanField(default=True)
#     image = models.ImageField(upload_to='static/image_admin/banner',  null=True, blank=True)

    
#     def __str__(self):
#         return f"{self.title} - {self.product.product_name}"
    

class ProductOffer(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.discount_percentage}% Discount"

    def save(self, *args, **kwargs):
        # Ensure discount_percentage is Decimal type
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
        # Ensure discount_percentage is Decimal type
        if not isinstance(self.discount_percentage, Decimal):
            self.discount_percentage = Decimal(str(self.discount_percentage))
        super().save(*args, **kwargs)
        
        


