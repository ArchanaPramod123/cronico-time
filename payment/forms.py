from django import forms
from .models import *

class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model =Address
        fields = ['users','name','address','phone','district','pincode']
class PaymentMethodForm(forms.Form):
    payment_method = forms.CharField(max_length=100)
# class CartOrderForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model =CartOrder
#         fields = ['user','total_amt','paid_status','order_date','product_status']

# class CartOrderItemsForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model =CartOrderItems
#         fields = ['order','invoice_no','item','image','qty','price','total']




    
