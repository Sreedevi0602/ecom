from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}), required= True)
    shipping_email = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required= True)
    shipping_phone = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required= True)
    shipping_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}), required= True)
    shipping_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}), required= False)
    shipping_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required= True)
    shipping_district = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}), required= True)
    shipping_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required= True)
    shipping_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN'}), required= True)
    shipping_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required= True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_phone', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_district', 'shipping_state', 'shipping_zipcode', 'shipping_country']

        exclude = ['user']

class PaymentForm(forms.Form):
    card_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on the Card'}), required= True)
    card_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}), required= True)
    card_exp_date = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expiration Date'}), required= True)
    card_cvv_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}), required= True)
    card_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}), required= True)
    card_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}), required= True)
    card_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required= True)
    card_district = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}), required= True)
    card_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required= True)
    card_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}), required= True)
    card_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required= True)

