# billing/models.py

from django.db import models
from django.contrib.auth.models import User



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_fullname = models.CharField(max_length=255)
    shipping_phone = models.CharField(max_length=20)
    shipping_email = models.EmailField()
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.shipping_fullname} - {self.shipping_address}, {self.city}, {self.shipping_country}"
