from django.contrib import admin
from .models import Product, Pizza

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price')
    list_filter = ('size',)
    search_fields = ('name', 'description')
    ordering = ('name',)

admin.site.register(Product)