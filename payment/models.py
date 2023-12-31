from django.db import models
from home.models import *


# Create your models here.
class Address(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.name
    
class CartOrder(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  total_amt = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
  paid_status = models.BooleanField(default=True)
  order_date = models.DateTimeField(auto_now_add=True)
  product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

  class Meta:
    verbose_name_plural = "Cart Order"
  # def __str__(self):
  #       return self.user


class CartOrderItems(models.Model):
  order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
  invoice_no = models.CharField(max_length=200)
  item = models.CharField(max_length=200)
  image = models.CharField(max_length=200)
  qty = models.IntegerField(default=0)
  price = models.FloatField()
  total = models.FloatField()
  class Meta:
    verbose_name_plural = "Cart Order Items"
  # def __str__(self):
  #       return self.invoice_no

  def image_tag(self):
    return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
