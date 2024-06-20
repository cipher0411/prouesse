# billing/urls.py

from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('shipping/', views.shipping_details, name='shipping'),
    path('payment/<int:item_id>/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/<int:item_id>/', views.payment, name='payment'),
]

