from payment.models import CartOrder
from django import forms
from .models import ProductOffer

class OrderForm(forms.ModelForm):
     class Meta:
        model = CartOrder
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})  # Apply attrs to the Select widget
        }

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['title', 'product','end_date', 'discount','image']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            
        }