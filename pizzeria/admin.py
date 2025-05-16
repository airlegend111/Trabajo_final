from django.contrib import admin
from .models import Pizza, ContactMessage

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Solo campos que existen en Pizza

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')