from django.db import models
from home.models import Product

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class ProductOffer(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productoffer_set')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    discount = models.DecimalField( max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Discount percentage")
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='static/image_admin/banner',  null=True, blank=True)

    
    def __str__(self):
        return f"{self.title} - {self.product.product_name}"
    



