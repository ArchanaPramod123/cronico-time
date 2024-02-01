from payment.models import CartOrder
from django import forms
from .models import ProductOffer,CategoryOffer,Banner,Coupon
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
    
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title','image','description1','description2','description3','start_date','end_date','is_active']
        widgets ={
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description1' : forms.Textarea(attrs={'class':'form-control','row':4}),
            'description2' : forms.Textarea(attrs={'class':'form-control','row':4}),
            'description3' : forms.Textarea(attrs={'class':'form-control','row':4}),
            'is_active' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'start_date' : forms.DateInput(attrs={'class':'form-control'}),
            'end_date' : forms.DateInput(attrs={'class':'form-control'}),

        }

class CouponForm(forms.Form):
    code = forms.CharField(max_length=50)