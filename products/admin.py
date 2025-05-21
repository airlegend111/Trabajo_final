from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from .models import Product, Pizza, Cart, CartItem
from users.models import Comment
from users.decorators import restricted_admin_required
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone

class RestrictedPizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price', 'created_by', 'modified_by', 'modified_at')
    list_filter = ('size', 'created_at', 'modified_at')
    search_fields = ('name', 'description')
    ordering = ('-modified_at',)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'size', 'price', 'image')
        }),
        ('Información de auditoría', {
            'fields': ('created_by', 'created_at', 'modified_by', 'modified_at'),
            'classes': ('collapse',),
            'description': 'Información sobre la creación y modificación de la pizza'
        })
    )
    
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva pizza
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_module_permission(self, request):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_add_permission(self, request):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
class RestrictedCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')
    
    def has_module_permission(self, request):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_add_permission(self, request):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()

class RestrictedCartAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class RestrictedCartItemAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

# Registrar los modelos con las clases de administración restringida
admin.site.register(Pizza, RestrictedPizzaAdmin)
admin.site.register(Comment, RestrictedCommentAdmin)
admin.site.register(Cart, RestrictedCartAdmin)
admin.site.register(CartItem, RestrictedCartItemAdmin)