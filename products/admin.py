from django.contrib import admin
from .models import Product, Pizza, Cart, CartItem

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price')
    list_filter = ('size',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'pizza', 'quantity', 'total_price')
    list_filter = ('pizza',)
    search_fields = ('cart__user__username', 'pizza__name')

admin.site.register(Product)