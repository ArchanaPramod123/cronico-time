from django.db import models
from django.utils import timezone

from home.models import User,Product,ProductAttribute



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
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total=models.BigIntegerField(null=True)
    timestamp = models.DateTimeField(default=timezone.now,null=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.product.product_name}"
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def get_total_price(self):
        if self.items.exists():
            return sum(item.get_subtotal() for item in self.items.all())
        else:
            return 0

    
class Wallet(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)
    
class WalletHistory(models.Model):
    wallet=models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type=models.CharField(null=True, blank=True, max_length=20)
    created_at=models.DateField(auto_now_add=True)
    amount=models.IntegerField()
    reason = models.CharField(max_length=255,blank=True,null=True)

    
class Payments(models.Model):
    payment_choices=(
        ('COD','COD'),
        ('Razorpay','Razorpay'),
        ('Wallet','Wallet'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.user.name}--{self.payment_method}"
        return self.user.first_name
    
class CartOrder(models.Model):
    STATUS =(
        ('New','New'),
        ('Paid','Paid'),
        ('Shipped','Shipped'),
        ('Conformed','Conformed'),
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return','Return')
    )
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payments,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20,default=None)
    order_total = models.FloatField(null=True, blank=True)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip =  models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at=models.DateTimeField(auto_now=True)
    selected_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Cart Order"
    
    def __str__(self):
        return self.order_number

class ProductOrder(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payments,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    product_price=models.FloatField(default=0)
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    variations =  models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.product.product_name
