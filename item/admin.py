from django.contrib import admin
from .models import Category, Item, ItemImage, Order, Cart, CartItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_sale', 'sale_price', 'is_sold', 'created_at', 'created_by')
    list_filter = ('category', 'is_sold', 'is_sale', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ItemImageInline]
    list_editable = ('is_sold', 'is_sale', 'sale_price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'quantity', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('item__name', 'user__username', 'address')
    list_editable = ('status',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'completed')
    list_filter = ('completed', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity', 'total_price')
    search_fields = ('cart__user__username', 'item__name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
