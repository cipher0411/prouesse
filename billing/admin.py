from django.contrib import admin
from .models import ShippingAddress

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'shipping_fullname', 'shipping_phone', 'shipping_email', 'shipping_address', 'city', 'shipping_postcode', 'shipping_country')
    search_fields = ('user__username', 'shipping_fullname', 'shipping_address', 'city', 'shipping_postcode', 'shipping_country')
    list_filter = ('city', 'shipping_country')

admin.site.register(ShippingAddress, ShippingAddressAdmin)
