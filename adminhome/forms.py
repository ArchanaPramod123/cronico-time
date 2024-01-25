from payment.models import CartOrder
from django import forms
from .models import ProductOffer,CategoryOffer
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from home.models import category

class OrderForm(forms.ModelForm):
     class Meta:
        model = CartOrder
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})  # Apply attrs to the Select widget
        }

# class ProductOfferForm(forms.ModelForm):
#     class Meta:
#         model = ProductOffer
#         fields = ['title', 'product','end_date', 'discount','image']
#         widgets = {
#             'product': forms.Select(attrs={'class': 'form-control'}),
#             'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'discount': forms.NumberInput(attrs={'class': 'form-control'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
            
#         }

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['discount_percentage', 'start_date', 'end_date', 'active']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if not (0 <= discount_percentage <= 100):
            raise forms.ValidationError('Discount percentage must be between 0 and 100.')
        return discount_percentage
    def clean_active(self):
        active = self.cleaned_data['active']
        existing_product_offer = CategoryOffer.objects.filter(active=True).exists()

        if active and existing_product_offer:
            raise ValidationError('A Category offer is already active. Deactivate it before activating a Product offer.')

        return active


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['category', 'discount_percentage', 'start_date', 'end_date', 'active']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryOfferForm, self).__init__(*args, **kwargs)
        # Limit the choices for the 'category' field to available categories
        self.fields['category'].queryset = category.objects.all()
        
        
    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if not (0 <= discount_percentage <= 100):
            raise forms.ValidationError('Discount percentage must be between 0 and 100.')
        return discount_percentage
      
    def clean_active(self):
        active = self.cleaned_data['active']
        existing_product_offer = ProductOffer.objects.filter(active=True).exists()

        if active and existing_product_offer:
            raise ValidationError('A product offer is already active. Deactivate it before activating a category offer.')

        return active