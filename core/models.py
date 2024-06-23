import secrets
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username




class otp_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True) 

    def is_otp_valid(self):
        if self.otp_created_at:
            now = timezone.now()
            time_difference = now - self.otp_created_at
            return time_difference <= timedelta(minutes=5)
        return False

    def __str__(self):
        return self.user.username
    
    


class Contact(models.Model):
    SERVICE_CHOICES = [
        ('Training', 'Training'),
        ('Ready to Wear Dress', 'Ready to Wear Dress'),
        ('Custom Made Dress', 'Custom Made Dress'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"
