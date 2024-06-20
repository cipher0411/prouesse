from django.contrib.auth import get_user_model
from django.db import models
from billing.models import ShippingAddress
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True, null=True)
    price = models.FloatField(default=0)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(),
        related_name='items',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0)

    def __str__(self):
        return self.name

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/item/', blank=True, null=True)

class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)  # Changed from customer to user
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Order {self.id} for {self.item.name}'

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='item_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    items = models.ManyToManyField(Item, related_name='carts')

    def __str__(self):
        return f'Cart of {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.item.price * self.quantity


