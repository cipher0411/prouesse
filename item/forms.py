from django import forms
from .models import Item, ItemImage
from django import forms
#from .models import ShippingAddress


INPUT_CLASSES = 'w-full py-2 px-6 rounded-xl border'

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = MultiFileInput(attrs={
            'class': INPUT_CLASSES,
            'multiple': True,
        })
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []
        return data

class NewItemForm(forms.ModelForm):
    images = MultiFileField(required=False)
    
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'is_sale', 'sale_price')
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditItemForm(forms.ModelForm):
    images = MultiFileField(required=False)
    
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'is_sale', 'sale_price', 'is_sold')
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }



# # item/forms.py
# class ShippingForm(forms.ModelForm):
#     class Meta:
#         model = ShippingAddress
#         fields = ['shipping_fullname', 'shipping_phone', 'shipping_email', 'shipping_address', 'city', 'shipping_postcode', 'shipping_country']
