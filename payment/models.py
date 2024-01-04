from django.db import models
from django.utils import timezone

from home.models import User,CartItem,Product,ProductAttribute



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
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    def str(self):
        return f"Wallet for {self.user.username}"
    
class Payments(models.Model):
    payment_choices=(
        ('COD','COD'),
        ('Razorpay','Razorpay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        # return f"{self.user.name}--{self.payment_method}"
        return self.user.first_name
    
class CartOrder(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Rejected','Rejected'),
    )
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    # orderitem=models.ForeignKey(CartItem, on_delete=models.CASCADE,default=None)
    payment=models.ForeignKey(Payments,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20,default=None)
    order_total = models.FloatField(null=True, blank=True)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip =  models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now,)
    updated_at=models.DateTimeField(default=timezone.now,)
    selected_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    # discount=models.FloatField(null=True)
    paymenttype=models.CharField(max_length=100,null=True)
    class Meta:
        verbose_name_plural = "Cart Order"
    
    def _str_(self):
        return self.order_number
  
#   user = models.ForeignKey(User, on_delete=models.CASCADE)
#   orderitem=models.ForeignKey(CartItem, on_delete=models.CASCADE,default=None)
#   total_amt = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
#   status = models.CharField(max_length=50,choices=STATUS,default='New')
#   payment = models.ForeignKey(Payments, on_delete=models.SET_NULL, blank=True, null= True)
#   # paid_status = models.BooleanField(default=True)
#   # order_date = models.DateTimeField(auto_now_add=True)
#   address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
#   product_status = models.CharField(choices=STATUS, max_length=30, default="processing")
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

  # def __str__(self):
  #       return self.user
#   def __str__(self):
#         if self.order_number is not None:
#             return self.order_number
#         else:
#             return "No order number available"

class ProductOrder(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payments,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    product_price=models.FloatField(default=0)
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    variations =  models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, null=True)
    def _str_(self):
        return self.product.product_name

    
    # def str(self):
    #     return f"{self.product} - {self.quantity}"

# class CartOrderItems(models.Model):
#   order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
#   invoice_no = models.CharField(max_length=200)
#   item = models.CharField(max_length=200)
#   image = models.CharField(max_length=200)
#   qty = models.IntegerField(default=0)
#   price = models.FloatField()
#   total = models.FloatField()
#   class Meta:
#     verbose_name_plural = "Cart Order Items"
#   # def __str__(self):
#   #       return self.invoice_no

#   def image_tag(self):
#     return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
