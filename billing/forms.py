from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['shipping_fullname', 'shipping_phone', 'shipping_email', 'shipping_address', 'city', 'shipping_postcode', 'shipping_country']
