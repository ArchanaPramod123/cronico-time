from django import forms
from .models import *

class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model =Address
        fields = ['name','address','phone','district','pincode']
class PaymentMethodForm(forms.Form):
    payment_method = forms.CharField(max_length=100)



    
